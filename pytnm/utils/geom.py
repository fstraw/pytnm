import os
import arcpy


def project_point(x, y, from_spatial_reference, to_spatial_reference):
    new_point = arcpy.Point(x, y)
    new_point_geom = arcpy.PointGeometry(new_point, from_spatial_reference)
    projected_point = new_point_geom.projectAs(to_spatial_reference).firstPoint
    new_x = projected_point.X
    new_y = projected_point.Y
    return (new_x, new_y)

def get_z_value(coords, raster, z_factor=None):
    coords_string = "{} {}".format(*coords)
    eval_cell_value = arcpy.GetCellValue_management(raster, coords_string)
    cell_value = float(eval_cell_value.getOutput(0))
    if z_factor:
        cell_value *= z_factor
    return round(cell_value, 1)

def update_feature_z(fc, raster):
    desc_fc = arcpy.Describe(fc)
    desc_raster = arcpy.Describe(raster)
    fc_sr = desc_fc.spatialReference
    raster_sr = desc_raster.spatialReference 
    with arcpy.da.UpdateCursor(fc, ["SHAPE@"]) as cursor:
        for row in cursor:
            geom = row[0]
            array = arcpy.Array()
            for part in geom:
                for pnt in part:
                    projected_coords = project_point(pnt.X, pnt.Y, fc_sr, raster_sr)
                    new_z = get_z_value(projected_coords, raster)
                    pnt.Z = new_z                  
                    array.add(pnt)            
            newpolyline = arcpy.Polyline(array, fc_sr, True)
            cursor.updateRow([newpolyline])

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)    
    test_receiver = "../../tests/test_files/DATA/receiver.shp"
    test_existing_roadway = "../../tests/test_files/DATA/existing_roadway.shp"
    test_barrier = "../../tests/test_files/DATA/barrier.shp"
    raster = r"C:\Users\brbatt\Documents\elevation_NED10M_ga121_3765948_01\elevation\ned10m33084h4.tif"
    update_feature_z(test_barrier, raster)



