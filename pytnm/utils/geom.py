import os
from pyproj import CRS, Transformer
# from arcpy import Array
# from arcpy import Describe
# from arcpy import GetCellValue_management
# from arcpy import Polyline
# from arcpy import Polygon
# from arcpy import Point
# from arcpy.da import SearchCursor, UpdateCursor


def project_point(x, y, from_spatial_reference, to_spatial_reference):
    """  """
    new_point = Point(x, y)
    new_point_geom = PointGeometry(new_point, from_spatial_reference)
    projected_point = new_point_geom.projectAs(to_spatial_reference).firstPoint
    new_x = projected_point.X
    new_y = projected_point.Y
    return (new_x, new_y)

# def _get_z_value(coords, raster):
#     coords_string = "{} {}".format(*coords)
#     eval_cell_value = GetCellValue_management(raster, coords_string)
#     try:
#         cell_value = float(eval_cell_value.getOutput(0))
#     except ValueError:
#         return 0
#     return round(cell_value, 1)

# def _update_poly_z(geom, raster, z_factor=1):
#     geom_sr = geom.spatialReference  
#     desc_raster = Describe(raster)    
#     raster_sr = desc_raster.spatialReference 
#     array = Array()
#     for part in geom: # TODO: account for multipart geometry
#         for pnt in part:
#             projected_coords = project_point(pnt.X, pnt.Y, geom_sr, raster_sr)
#             new_z = round(_get_z_value(projected_coords, raster) * z_factor, 1)
#             # new_z = round(pnt.Z * z_factor, 1)
#             pnt.Z = new_z
#             array.add(pnt)
#     return array

# def _round_poly_vertices(geom):
#     array = Array()
#     for part in geom: # TODO: account for multipart geometry
#         for pnt in part:
#             pnt.X = round(pnt.X, 2)
#             pnt.Y = round(pnt.Y, 2)
#             pnt.Z = round(pnt.Z, 2)
#             array.add(pnt)                    
#     return array

# def _convert_z_vertices(geom, z_factor):
#     """Converts z-coordinates to different unit

#     Args:
#         geom ([type]): [description]
#         z_factor ([type]): [description]

#     Returns:
#         [type]: [description]
#     """
#     array = Array()
#     for part in geom: # TODO: account for multipart geometry
#         for pnt in part:
#             pnt.X = pnt.X
#             pnt.Y = pnt.Y
#             pnt.Z = pnt.Z * z_factor
#             array.add(pnt)                    
#     return array

# def _update_z_poly_vertices(geom, xys_to_update):
#     Updates z vales for given coordinate lists, for making z values congruent for identical xy locations
#     array = Array()
#     for part in geom: # TODO: account for multipart geometry
#         for pnt in part:
#             for xyz in xys_to_update:
#                 if pnt.X == xyz[0] and pnt.Y == xyz[1]: 
#                     pnt.X = xyz[0]
#                     pnt.Y = xyz[1]
#                     pnt.Z = xyz[2]
#                 else:
#                     pass
#             array.add(pnt)                    
#     return array

# def _update_point_z(geom, raster, z_factor=1):
#     geom_sr = geom.spatialReference  
#     desc_raster = Describe(raster)    
#     raster_sr = desc_raster.spatialReference
#     pnt = geom.firstPoint # TODO: account for multipart geometry
#     projected_coords = project_point(pnt.X, pnt.Y, geom_sr, raster_sr)
#     new_z = round(_get_z_value(projected_coords, raster) * z_factor, 1)
#     pnt.Z = new_z                  
#     return pnt

# def update_feature_z(fc, raster, z_factor=1, sql=None):
#     desc_fc = Describe(fc)
#     fc_sr = desc_fc.spatialReference
#     with UpdateCursor(fc, ["SHAPE@"], sql) as cursor:
#         for row in cursor:
#             geom = row[0]
#             if geom.type == "polyline":
#                 array = _update_poly_z(geom, raster, z_factor)           
#                 new_geom = Polyline(array, fc_sr, True)
#             elif geom.type == "polygon":
#                 array = _update_poly_z(geom, raster, z_factor)           
#                 new_geom = Polygon(array, fc_sr, True)
#             elif geom.type == "point":
#                 new_geom = _update_point_z(geom, raster, z_factor)
#             else:
#                 try:
#                     raise ValueError('Function requires polyline, polygon, or point feature class')
#                 except ValueError as exc:
#                     print(exc)
#             cursor.updateRow([new_geom])

# def round_coordinates(shp):
#     with UpdateCursor(shp, 'SHAPE@') as ucursor:        
#         for row in ucursor:
#             geom = row[0]
#             array = _round_poly_vertices(geom)
#             new_geom = Polyline(array, None, True)
#             ucursor.updateRow([new_geom])

# def convert_z_coords(shp, z_factor=3.2808399):
#     with UpdateCursor(shp, 'SHAPE@') as ucursor:        
#         for row in ucursor:
#             geom = row[0]
#             array = _convert_z_vertices(geom, z_factor)
#             new_geom = Polyline(array, None, True)
#             ucursor.updateRow([new_geom])

def update_max_z(shp, xys_to_update):
    """Updates z vales for given coordinate lists, for making z values congurent for identical xy locations
    """
    transformer = Transformer.from_crs(from_spatial_reference, to_spatial_reference)
    return transformer.transform(x, y)


# def _get_z_value(coords, raster):
#     coords_string = "{} {}".format(*coords)
#     eval_cell_value = GetCellValue_management(raster, coords_string)
#     try:
#         cell_value = float(eval_cell_value.getOutput(0))
#     except ValueError:
#         return 0
#     return round(cell_value, 1)

# def _update_poly_z(geom, raster, z_factor=1):
#     geom_sr = geom.spatialReference  
#     desc_raster = Describe(raster)    
#     raster_sr = desc_raster.spatialReference 
#     array = Array()
#     for part in geom: # TODO: account for multipart geometry
#         for pnt in part:
#             projected_coords = project_point(pnt.X, pnt.Y, geom_sr, raster_sr)
#             new_z = round(_get_z_value(projected_coords, raster) * z_factor, 1)
#             # new_z = round(pnt.Z * z_factor, 1)
#             pnt.Z = new_z
#             array.add(pnt)
#     return array

# def _round_poly_vertices(geom):
#     array = Array()
#     for part in geom: # TODO: account for multipart geometry
#         for pnt in part:
#             pnt.X = round(pnt.X, 2)
#             pnt.Y = round(pnt.Y, 2)
#             pnt.Z = round(pnt.Z, 2)
#             array.add(pnt)                    
#     return array

# def _update_z_poly_vertices(geom, xys_to_update):
#     """Updates z vales for given coordinate lists, for making z values congruent for identical xy locations
#     """
#     array = Array()
#     for part in geom: # TODO: account for multipart geometry
#         for pnt in part:
#             for xyz in xys_to_update:
#                 if pnt.X == xyz[0] and pnt.Y == xyz[1]: 
#                     pnt.X = xyz[0]
#                     pnt.Y = xyz[1]
#                     pnt.Z = xyz[2]
#                 else:
#                     pass
#             array.add(pnt)                    
#     return array

# def _update_point_z(geom, raster, z_factor=1):
#     geom_sr = geom.spatialReference  
#     desc_raster = Describe(raster)    
#     raster_sr = desc_raster.spatialReference
#     pnt = geom.firstPoint # TODO: account for multipart geometry
#     projected_coords = project_point(pnt.X, pnt.Y, geom_sr, raster_sr)
#     new_z = round(_get_z_value(projected_coords, raster) * z_factor, 1)
#     pnt.Z = new_z                  
#     return pnt

# def update_feature_z(fc, raster, z_factor=1, sql=None):
#     desc_fc = Describe(fc)
#     fc_sr = desc_fc.spatialReference
#     with UpdateCursor(fc, ["SHAPE@"], sql) as cursor:
#         for row in cursor:
#             geom = row[0]
#             if geom.type == "polyline":
#                 array = _update_poly_z(geom, raster, z_factor)           
#                 new_geom = Polyline(array, fc_sr, True)
#             elif geom.type == "polygon":
#                 array = _update_poly_z(geom, raster, z_factor)           
#                 new_geom = Polygon(array, fc_sr, True)
#             elif geom.type == "point":
#                 new_geom = _update_point_z(geom, raster, z_factor)
#             else:
#                 try:
#                     raise ValueError('Function requires polyline, polygon, or point feature class')
#                 except ValueError as exc:
#                     print(exc)
#             cursor.updateRow([new_geom])

# def round_coordinates(shp):
#     with UpdateCursor(shp, 'SHAPE@') as ucursor:        
#         for row in ucursor:
#             geom = row[0]
#             array = _round_poly_vertices(geom)
#             new_geom = Polyline(array, None, True)
#             ucursor.updateRow([new_geom])

# def update_max_z(shp, xys_to_update):
#     """Updates z vales for given coordinate lists, for making z values congurent for identical xy locations

#     Args:
#         shp ([type]): [description]
#     """
#     with UpdateCursor(shp, 'SHAPE@') as ucursor:        
#         for row in ucursor:
#             geom = row[0]
#             array = _update_z_poly_vertices(geom, xys_to_update)
#             new_geom = Polyline(array, None, True)
#             ucursor.updateRow([new_geom])

# def get_all_vertices(shp):
#     vertices = []
#     with SearchCursor(shp, 'SHAPE@') as scursor:
#         for row in scursor:
#             geom = row[0]
#             for part in geom:
#                 for pnt in part:
#                     xyz = [pnt.X, pnt.Y, pnt.Z]
#                     vertices.append(xyz)
#     return vertices

# def identical_pnts(coords):
#     identical_pnts = []
#     for point in coords:
#         identical = 0
#         x = round(point[0], 2)
#         y = round(point[1], 2)
#         for pnt in coords:
#             if round(pnt[0], 2) == x and round(pnt[1], 2) == y:
#                 identical += 1 # all points should be identical to themselves, so one will be minimum
#         if identical > 1:
#             identical_pnts.append(point)
#     return sorted(identical_pnts)

# def identical_set(coords): #produces duplicates but whatever
#     """Returns set of max z values per given identical xy

#     Args:
#         coords (List): List of identical xy coordinates
#     """
#     max_coords = []
#     for coord in coords:
#         identicals = [xy for xy in coords if xy[0] == coord[0] and xy[1] == coord[1]]
#         max_z = max([xyz[2] for xyz in identicals])
#         for identical in identicals:
#             if identical[2] == max_z:
#                 max_coords.append(identical)
#                 break
#             else:
#                 pass
#     return max_coords 


# if __name__ == '__main__':
#     x = 123
#     y = 456
#     print(project_point(x, y, 3857, 4326))