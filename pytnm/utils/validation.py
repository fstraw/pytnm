# import arcpy


# def get_count_of_unique_vals(fc, fields):
#     countList = []
#     with arcpy.da.SearchCursor(fc,fields) as cursor:        
#         for row in sorted(cursor):            
#             if not row[0] in countList:
#                 countList.append(row[0])
#     return countList

# def validatespatialreference(fc):
#     desc = arcpy.Describe(fc)
#     mxd = arcpy.mapping.MapDocument("CURRENT")
#     df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
#     if desc.spatialReference.name == "Unknown":
#         arcpy.AddWarning("Projection of input {} not defined. \
# 		Setting projection of input polyline to match current data frame...".format(desc.name))
#         arcpy.DefineProjection_management(fc, df.spatialReference)
#     else:
#         arcpy.AddMessage("Projection of input {} is {}. Proceeding...".format(desc.name,desc.spatialReference.name))

# def validate_roadway_fields(roadfc, condition):
#     flds = [f.name for f in arcpy.ListFields(roadfc)]
#     if not ("bld_total" in flds or "ex_total" in flds or "nb_total" in flds):
#         raise ValueError("Feature class must include fields: bld_total, ex_total, nb_total")
#     if condition == "BUILD":
#         return ("road_name", "speed", "auto_bld", "medium_bld", "heavy_bld", "SHAPE@")
#     elif condition == "EXISTING":
#         return ("road_name", "speed", "auto_ex", "medium_ex", "heavy_ex", "SHAPE@")
#     elif condition == "NO_BUILD":
#         return ("road_name", "speed", "auto_nb", "medium_nb", "heavy_nb", "SHAPE@")  