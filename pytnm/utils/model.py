# -*- coding: utf-8 -*-
import os
import arcpy

from validation import validate_roadway_fields


def write_header(f):
    f.write("1,3\n")
                

def improvedpoint(x, y, fcsr, rastersr):
    """
    Retrieves value from raster, given an X, Y coordinate
    """
    point = arcpy.Point(x,y)    
    pnttrans = arcpy.PointGeometry(point,fcsr).projectAs(rastersr).firstPoint
    cellvalue = arcpy.GetCellValue_management(rast, "{} {}".format(
                                                pnttrans.X, pnttrans.Y))
    if boolZ == True:
        result = round(float(cellvalue.getOutput(0)) * 3.2808399, 1) #convert to feet
    else:
        result = 0
    return result

def roadway_separator():
    hdr = "'L' /\n"
    return hdr

def barrier_separator():
    hdr = "'A' /\n"
    return hdr

def _write_roadway_points(line_geom):
    point_strings = ""
    point_strings += roadway_separator()
    for part in line_geom:
        for pnt_number, pnt in enumerate(part):
            x = round(pnt.X, 1) 
            y = round(pnt.Y, 1)
            z = round(pnt.Z, 1)            
            point_strings += "'Point{}' {} {} {} 0\n".format(pnt_number, x, y, z)
        point_strings += roadway_separator()
        return point_strings

def _write_roadway_attrs(roadway_feature_class, condition):
    """Creates string of roadway attributes
    
    Arguments:
        roads_feature_class {String} -- Path to feature class
        condition {String} -- Existing, NoBuild, or Build. Determines fields to use from geospatial template
    """
    flds = validate_roadway_fields(roadway_feature_class, condition.upper()) 
    with arcpy.da.SearchCursor(roadway_feature_class, flds) as cursor:
        roadway_string = ""
        for row in cursor:
            road = row[0]
            speed = row[1]
            auto = round(row[2], 0)
            medium = round(row[3], 0)
            heavy = round(row[4], 0)
            geometry = row[5]
            roadway_string += "{}\n".format(road)
            roadway_string += "CARS {} {}\n".format(auto, speed)
            roadway_string += "MT {} {}\n".format(medium, speed)
            roadway_string += "HT {} {}\n".format(heavy, speed)
            roadway_string += _write_roadway_points(geometry)
        return roadway_string

def _write_barrier_points(line_geom):
    point_strings = ""
    # set constants for barrier defaults    
    NUMBER_OF_PERTURBATIONS = 2
    PERTURBATION_INCREMENT = 9
    BARRIER_INITIAL_HEIGHT = 7
    for part in line_geom:
        for pnt_number, pnt in enumerate(part):
            x = round(pnt.X, 1)
            y = round(pnt.Y, 1)
            z = round(pnt.Z, 1)
            barrier_height = z + BARRIER_INITIAL_HEIGHT
            if pnt_number == 0:
                point_strings += "'Point{}' {} {} {} {} {} {}\n".format(
                    pnt_number, x, y, barrier_height, z, NUMBER_OF_PERTURBATIONS, PERTURBATION_INCREMENT)                
            else:
                point_strings += "'Point{}' {} {} {} {}\n".format(pnt_number, x, y, barrier_height, z)
        point_strings += barrier_separator()
        return point_strings

def _write_barrier_attrs(barrier_feature_class):
    """Creates string of barrier attributes
    
    Arguments:
        barrier_feature_class {String} -- Path to feature class        
    """    
    with arcpy.da.SearchCursor(barrier_feature_class, ("name", "SHAPE@")) as cursor:
        barrier_string = ""
        for row in cursor:
            name = row[0]
            geometry = row[1]
            barrier_string += "{}\n".format(name)
            barrier_string += _write_barrier_points(geometry)
        return barrier_string

def improvedrecpnts(fc, fcsr, rastersr):
    reccount = arcpy.GetCount_management(fc).getOutput(0)
    f.write("5,{}\n".format(reccount))
    f.write("RECEIVERS\n")
    arcpy.SetProgressor("step", "Processing Receivers...", 0, int(reccount), 1)
    with arcpy.da.SearchCursor(fc, ["Rec_ID", "SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:            
            recid = round(row[0],1)            
            x, y = round(row[1],1), round(row[2],1)
            if "{}".format(recid).endswith("0"):
                bldgheight = 5
            elif "{}".format(recid).endswith("1"):
                bldgheight = 5
            elif "{}".format(recid).endswith("2"):
                bldgheight = 15
            elif "{}".format(recid).endswith("3"):
                bldgheight = 25
            elif "{}".format(recid).endswith("4"):
                bldgheight = 35
            elif "{}".format(recid).endswith("5"):
                bldgheight = 45
            z = improvedpoint(round(row[1],1),round(row[2],1),fcsr,rastersr) + bldgheight  
            arcpy.SetProgressorLabel("Processing Receiver {0}...".format(recid))
            f.write("{} {} {} {}\n".format(recid, x, y, z))
            arcpy.SetProgressorPosition()
        arcpy.ResetProgressor()

def calculateroadwayz(fc, rast):
    cursor = arcpy.UpdateCursor(fc)
    shapeName = arcpy.Describe(fc).shapeFieldName
    for row in cursor:
        geom = row.getValue(shapeName)
        newGeom = arcpy.Array()
        for part in geom:
            newPart = arcpy.Array()
            for pnt in part:
                if pnt != None:
                    newPnt = arcpy.Point(pnt.X, pnt.Y, improvedpoint(pnt.X, pnt.Y, arcpy.Describe(fc).spatialReference, arcpy.Describe(rast).spatialReference))
                    newPart.add(newPnt)
            newGeom.add(newPart)
        newShape = arcpy.Polyline(newGeom)
        row.setValue(shapeName, newShape)
        cursor.updateRow(row)
    del row, cursor
    
    with arcpy.da.SearchCursor(fc, "SHAPE@") as cursor:
        for row in cursor:
            for part in row[0]:
                for pnt in part:                
                    print(pnt.X, pnt.Y, pnt.Z)

def add_z_to_points(fc, rast, zfactor):
    """ Add Z value to Z-enabled point feature class"""
    desc = arcpy.Describe(fc)
    fcspatref = desc.spatialReference
    if not desc.hasZ:
        raise ValueError('Input feature class must be Z-enabled!')
    if fcspatref == "Unknown":
        raise ValueError("Projection of {} is undefined! Define projection and try again.".format(desc.name))
    with arcpy.da.UpdateCursor(fc, ('SHAPE@X', 'SHAPE@Y', 'SHAPE@Z')) as ucursor:
        for row in ucursor:
            x = row[0]
            y = row[1]
            z = improvedpoint(x, y, fcspatref, rast, zfactor)
            newpnt = arcpy.Point(x, y, z)
            newpntGeom = arcpy.PointGeometry(newpnt)
            row[2] = z
            ucursor.updateRow(row)

if __name__ == '__main__':
    test_existing_roadway = "../../tests/test_files/DATA/existing_roadway.shp"
    test_barrier = "../../tests/test_files/DATA/barrier.shp"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)    
    test_road_geom = [row[0] for row in arcpy.da.SearchCursor(test_existing_roadway, "SHAPE@")][0]
    test_barrier_geom = [row[0] for row in arcpy.da.SearchCursor(test_barrier, "SHAPE@")][0]
    # print(_write_roadway_points(test_road_geom))
    # print(_write_barrier_points(test_barrier_geom))
    print(_write_roadway_attrs(test_existing_roadway, 'Existing'))
    print(_write_barrier_attrs(test_barrier))
