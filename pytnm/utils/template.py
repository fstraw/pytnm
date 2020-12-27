import os
import shapefile
# from arcpy import CreateFeatureclass_management as cf
# from arcpy import AddField_management as af
# from arcpy import env

# env.overwriteOutput = True

# https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf
# NULL = 0
# POINT = 1
# POLYLINE = 3
# POLYGON = 5
# MULTIPOINT = 8
# POINTZ = 11
# POLYLINEZ = 13
# POLYGONZ = 15
# MULTIPOINTZ = 18
# POINTM = 21
# POLYLINEM = 23
# POLYGONM = 25
# MULTIPOINTM = 28
# MULTIPATCH = 31
    
def create_receivers(input_folder):
    f = "receiver"
    fn = os.path.join(input_folder, f)
    writer = shapefile.Writer(os.path.join(input_folder, f), shapeType=shapefile.POINTZ)
    writer.field("rec_id", "C", size=10)
    writer.field("x", "N")
    writer.field("y", "N")
    writer.field("z", "N")
    writer.field("du", "N")
    writer.field("bldg_hgt", "N")
    writer.field("land_use", "C", size=100)
    writer.field("nac_cat", "C", size=1)
    writer.field("nac_lvl", "N")
    writer.field("ext_use", "C", size=1)
    writer.field("displace", "C", size=1)
    writer.field("bldg_row", "N")
    writer.field("exist_snd", "N")
    writer.field("nobld_snd", "N")
    writer.field("bld_snd", "N")
    writer.field("ex_imp", "C", size=1)
    writer.field("nobld_imp", "C", size=1)
    writer.field("bld_imp", "C", size=1)
    writer.field("bar_name", "C", size=10)
    writer.field("bar_reduct", "N")
    writer.field("project", "C", size=25)
    return F"{fn}.shp"

def create_existing_roadway(input_folder):
    f = "existing_roadway"
    writer = shapefile.Writer(os.path.join(input_folder, f), shapeType=shapefile.POLYLINEZ)
    writer.field("road_name", "C", size=32)
    writer.field("exist_traf", "N")
    writer.field("nobld_traf", "N")
    writer.field("div_lanes", "N")
    writer.field("speed", "N")
    writer.field("ex_total", "N")
    writer.field("nb_total", "N")
    writer.field("auto_ex", "N")
    writer.field("med_ex", "N")
    writer.field("heavy_ex", "N")
    writer.field("auto_nobld", "N")
    writer.field("med_nobld", "N")
    writer.field("heavy_nobld", "N")
    writer.field("heavy_pct", "N")
    writer.field("medium_pct", "N")
    writer.field("project", "C", size=100)

def create_proposed_roadway(input_folder):
    f = "proposed_roadways"
    writer = shapefile.Writer(os.path.join(input_folder, f), shapeType=shapefile.POLYLINEZ)
    writer.field("road_name", "C", size=32)
    writer.field("bld_traf", "N")
    writer.field("div_lanes", "N")
    writer.field("speed", "N")
    writer.field("bld_total", "N")
    writer.field("auto_bld", "N")
    writer.field("med_bld", "N")
    writer.field("heavy_bld", "N")
    writer.field("heavy_pct", "N")
    writer.field("medium_pct", "N")
    writer.field("project", "C", size=100)

def create_barrier(input_folder):
    f = "barrier"
    writer = shapefile.Writer(os.path.join(input_folder, f), shapeType=shapefile.POLYLINEZ)
    writer.field("name", "C", size=32)
    writer.field("feasible", "C", size=1)
    writer.field("reasonable", "C", size=1)
    writer.field("pert_inc", "N")
    writer.field("pert_num", "N")
    writer.field("init_hgt", "N")
    writer.field("project", "C", size=100)

def create_terrain_line(input_folder):
    f = "terrain_line"
    writer = shapefile.Writer(os.path.join(input_folder, f), shapeType=shapefile.POLYLINEZ)
    writer.field("name", "C", size=32)
    writer.field("project", "C", size=100)

def create_study_area(input_folder):
    f = "study_area"
    writer = shapefile.Writer(os.path.join(input_folder, f), shapeType=shapefile.POLYGONZ)
    writer.field("name", "C", size=32)
    writer.field("project", "C", size=100)

def create_study_receivers(input_folder):
    f = "study_receiver"
    writer = shapefile.Writer(os.path.join(input_folder, f), shapeType=shapefile.POINTZ)
    writer.field("rec_id", "C", size=10)
    writer.field("x", "N")
    writer.field("y", "N")
    writer.field("z", "N")
    writer.field("project", "C", size=100)

def create_field_measurements(input_folder):
    f = "field_measurement"
    writer = shapefile.Writer(os.path.join(input_folder, f), shapeType=shapefile.POINTZ)
    writer.field("rec_id", "C", size=10)
    writer.field("x", "N")
    writer.field("y", "N")
    writer.field("z", "N")
    writer.field("dba", "N")
    writer.field("project", "C", size=100)

def create_ground_area(input_folder):
    f = "ground_zone"
    writer = shapefile.Writer(os.path.join(input_folder, f), shapeType=shapefile.POLYGONZ)
    writer.field("name", "C", size=32)
    writer.field("type", "C", size=32)
    writer.field("project", "C", size=100)

def create_tree_zone(input_folder):
    f = "tree_zone"
    writer = shapefile.Writer(os.path.join(input_folder, f), shapeType=shapefile.POLYGONZ)
    writer.field("name", "C", size=32)
    writer.field("avg_hgt", "N")
    writer.field("project", "C", size=100)

def create_building_row(input_folder):
    f = "builing_row"
    writer = shapefile.Writer(os.path.join(input_folder, f), shapeType=shapefile.POLYLINEZ)
    writer.field("name", "C", size=32)
    writer.field("avg_hgt", "N")
    writer.field("bldg_pct", "N")

if __name__ == '__main__':
    pass