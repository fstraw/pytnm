# -*- coding: utf-8 -*-
"""
Created on Wed Feb 04 09:10:09 2015

@author: bbatt
"""

import arcpy
import os

arcpy.env.overwriteOutput = True
road = arcpy.mapping.Layer(arcpy.GetParameterAsText(0)).dataSource
condition = arcpy.GetParameterAsText(1)
receiverfile = arcpy.mapping.Layer(arcpy.GetParameterAsText(2)).dataSource
rast = arcpy.mapping.Layer(arcpy.GetParameterAsText(3)).dataSource
boolZ = arcpy.GetParameter(5)
try:
    barrierfile = arcpy.mapping.Layer(arcpy.GetParameterAsText(6)).dataSource
    barlyrname = arcpy.mapping.Layer(arcpy.GetParameterAsText(6)).name
except:
    barrierfile = None
    barlyrname = None
f = open(os.path.join(arcpy.GetParameterAsText(4), "{}.dat".format(condition)),"wb")

#ws = arcpy.env.workspace
#road = r"C:\Users\bbatt\Documents\!ICE1401\DATA\e87_to_append.shp"
#condition = "Build"
#receiverfile = r"C:\Users\bbatt\Documents\!ICE1401\DATA\Receiverss.shp"
#barrierfile = r"C:\Users\bbatt\Documents\!ICE1401\DATA\Barrier_Detailed_zs.shp"
#rast = r"U:\Shared\DEM\SC_Spart_Cher_10m.tif"
#f = open(os.path.join(r"C:\Users\bbatt\Documents\!ICE1401", "{}d.dat".format(condition)),"wb")
#boolZ = True

arcpy.AddMessage("\nWorkspace: {}\n".format(arcpy.env.workspace))
arcpy.AddMessage("Road: {}\n".format(road))
arcpy.AddMessage("Condition: {}\n".format(condition))
arcpy.AddMessage("Receiver: {}\n".format(receiverfile))
#arcpy.AddMessage("Barrier: {}\n".format(barrierfile))
arcpy.AddMessage("DEM Raster: {}\n".format(rast))
arcpy.AddMessage("Output: {}\n".format(condition))
arcpy.AddMessage("Calculate Z Values?: {}\n".format(boolZ))


def write_header(f):
    f.write("1,3\n")

def get_count_of_unique_vals(fc, fields):
    countList = []
    with arcpy.da.SearchCursor(fc,fields) as cursor:        
        for row in sorted(cursor):            
            if not row[0] in countList:
                countList.append(row[0])
    return countList                

def improvedpoint(x, y, fcsr, rastersr):
    #Assumes data source is in meters (USDA NAIP)git ciom
    point = arcpy.Point(x,y)    
    pnttrans = arcpy.PointGeometry(point,fcsr).projectAs(rastersr).firstPoint
    cellvalue = arcpy.GetCellValue_management(rast, "{} {}".format(
                                                pnttrans.X, pnttrans.Y))
    if boolZ == True:
        result = round(float(cellvalue.getOutput(0)) * 3.2808399, 1) #convert to feet
    else:
        result = 0
    return result

"""
write_pnts(file, string)

"""

def improvedwritepnts(geom, fcsr, rastersr, ftype="Road"):
    i = 0
    if not ftype.upper() == "BARRIER":
        hdr = "'L' /\n"
        f.write(hdr)
    else:
        hdr = "'A' /\n"
        barincscount = 1
        barpert = 2
        barinc = 9
        barinitheight = 7
    for part in geom:
        for pnt in part:
            if ftype.upper() == "ROAD":
                x, y, z = round(pnt.X, 1), round(pnt.Y, 1), round(pnt.Z, 1)
                strPnt = "'Point{}' {} {} {} 0\n".format(i, x, y, z)
            elif ftype.upper() == "BARRIER":
                x, y, z = round(pnt.X,1), round(pnt.Y, 1), round(pnt.Z, 1)
                if barincscount == 1:
                    strPnt = "'Point{}' {} {} {} {} {} {}\n".format(i, x, y, z + barinitheight, z, barpert, barinc)
                    barincscount -= 1
                else:
                    strPnt = "'Point{}' {} {} {} {}\n".format(i, x, y, z + barinitheight, z)
            f.write(strPnt)
            i+=1
    f.write(hdr)
  
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

# Identify roadway polyline feature,
# and the raster from which to pull 
# values. Does not require z-enable feature

def validatespatialreference(fc):
    desc = arcpy.Describe(fc)
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
    if desc.spatialReference.name == "Unknown":
        arcpy.AddWarning("Projection of input {} not defined. \
		Setting projection of input polyline to match current data frame...".format(desc.name))
        arcpy.DefineProjection_management(fc, df.spatialReference)
    else:
        arcpy.AddMessage("Projection of input {} is {}. Proceeding...".format(desc.name,desc.spatialReference.name))

def validatefields(roadfc, condition):
    flds = [f.name for f in arcpy.ListFields(roadfc)]
    if not ("Bld_Tot" in flds or "Ex_Tot" in flds or "NoBld_Tot" in flds):
        raise ValueError("Valid inputs include: rseg_existing or rseg_build")
    if condition == "Build":
        return ("Rd_Name", "Speed", "Auto_Bld", "Medium_Bld", "Heavy_Bld", "SHAPE@")
    elif condition == "Existing":
        return ("Rd_Name", "Speed", "Auto_Ex", "Medium_Ex", "Heavy_Ex", "SHAPE@")
    elif condition == "NoBuild":
        return ("Rd_Name", "Speed", "Auto_NoBld", "Med_NoBld", "Heav_NoBld", "SHAPE@")    

def improvedbarrier(fc, rast):
    fcdesc, rastdesc = arcpy.Describe(fc), arcpy.Describe(rast)
    fcsr, rastersr = fcdesc.spatialReference, rastdesc.spatialReference
    barriercount = arcpy.GetCount_management(fc).getOutput(0)
    f.write("3,{}\n".format(barriercount))
    arcpy.SetProgressor("step", "Processing Barriers...", 0, int(barriercount), 1)
    with arcpy.da.SearchCursor(fc, ["Id", "SHAPE@"]) as cursor:
        for row in cursor:
            barrier, geometry = row[0], row[1]
            arcpy.SetProgressorLabel("Processing Barrier {0}...".format(barrier))
            f.write("Barrier {}\n".format(barrier))
            improvedwritepnts(geometry, fcsr, rastersr, "BARRIER")
            arcpy.SetProgressorPosition()
        arcpy.ResetProgressor()
        
def improvedroadway(fc, rast):
    fcdesc, rastdesc = arcpy.Describe(fc), arcpy.Describe(rast)
    fcsr, rastersr = fcdesc.spatialReference, rastdesc.spatialReference
    roadcount = arcpy.GetCount_management(fc).getOutput(0)
    write_header(f)
    f.write("2,{}\n".format(roadcount))
    arcpy.SetProgressor("step", "Processing Roadways...", 0, int(roadcount), 1)
    with arcpy.da.SearchCursor(fc, validatefields(fc, condition)) as cursor:
        for row in cursor:
            road, speed, auto, medium, heavy, geometry = row[0], row[1], round(row[2], 0), round(row[3], 0), round(row[4], 0), row[5]
            arcpy.SetProgressorLabel("Processing {0}...".format(road))
            f.write("{}\n".format(road))
            f.write("CARS {} {}\n".format(auto, speed))
            f.write("MT {} {}\n".format(medium, speed))
            f.write("HT {} {}\n".format(heavy, speed))
            improvedwritepnts(geometry, fcsr, rastersr)
            arcpy.SetProgressorPosition()
        arcpy.ResetProgressor()
        if barrierfile:
            improvedbarrier(barrierfile, rast)
        else:
            pass
        improvedrecpnts(receiverfile, fcsr, rastersr)
        f.write("7/\n")
        f.close()

#Experimental code to place Z coordinates from raster surface
#directly into Z-enabled feature class.
#have to use old UpdateCursor (bleh)
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
    validatespatialreference(road)
    validatespatialreference(receiverfile)
    validatespatialreference(rast)
    improvedroadway(road, rast)
