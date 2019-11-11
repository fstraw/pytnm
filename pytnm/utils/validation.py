import arcpy


def get_count_of_unique_vals(fc, fields):
    countList = []
    with arcpy.da.SearchCursor(fc,fields) as cursor:        
        for row in sorted(cursor):            
            if not row[0] in countList:
                countList.append(row[0])
    return countList

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