import os
import shapefile2
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
    writer = shapefile2.Writer(os.path.join(input_folder, f), shapeType=shapefile2.POINTZ)
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

def create_existing_roadway(input_folder):
    f = "existing_roadway"
    writer = shapefile2.Writer(os.path.join(input_folder, f), shapeType=shapefile2.POLYLINEZ)
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
    writer = shapefile2.Writer(os.path.join(input_folder, f), shapeType=shapefile2.POLYLINEZ)
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

# def create_proposed_roadway(input_folder):
#     proposed_roadways = cf(out_path=input_folder,
#         out_name="proposed_roadway",
#         geometry_type="POLYLINE",
#         template=None,
#         has_m="ENABLED",
#         has_z="ENABLED",
#         spatial_reference=None
#     )
#     af(in_table=proposed_roadways, 
#         field_name="road_name", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=32,
#         field_alias="road_name",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=proposed_roadways, 
#         field_name="bld_traf", 
#         field_type="SHORT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="bld_traf",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=proposed_roadways, 
#         field_name="div_lanes", 
#         field_type="SHORT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="div_lanes",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=proposed_roadways, 
#         field_name="speed", 
#         field_type="SHORT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="speed",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=proposed_roadways, 
#         field_name="bld_total", 
#         field_type="SHORT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="bld_total",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=proposed_roadways, 
#         field_name="auto_bld", 
#         field_type="SHORT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="auto_bld",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=proposed_roadways, 
#         field_name="medium_bld", 
#         field_type="SHORT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="medium_bld",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=proposed_roadways, 
#         field_name="heavy_bld", 
#         field_type="SHORT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="heavy_bld",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=proposed_roadways, 
#         field_name="med_pct", 
#         field_type="FLOAT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="med_pct",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=proposed_roadways, 
#         field_name="hvy_pct", 
#         field_type="FLOAT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="hvy_pct",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )

# def create_barrier(input_folder):
#     barrier = cf(out_path=input_folder,
#         out_name="barrier",
#         geometry_type="POLYLINE",
#         template=None,
#         has_m="ENABLED",
#         has_z="ENABLED",
#         spatial_reference=None
#     )
#     af(in_table=barrier, 
#         field_name="name", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=32,
#         field_alias="name",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=barrier, 
#         field_name="feasible", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=1,
#         field_alias="feasible",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=barrier, 
#         field_name="reasonable", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=1,
#         field_alias="reasonable",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=barrier, 
#         field_name="pert_inc", 
#         field_type="SHORT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="pert_inc",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=barrier, 
#         field_name="pert_num", 
#         field_type="SHORT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="pert_num",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=barrier, 
#         field_name="init_hgt", 
#         field_type="DOUBLE",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="init_hgt",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
# def create_terrain_line(input_folder):
#     terrain_line = cf(out_path=input_folder,
#         out_name="terrain_line",
#         geometry_type="POLYLINE",
#         template=None,
#         has_m="ENABLED",
#         has_z="ENABLED",
#         spatial_reference=None
#     )
#     af(in_table=terrain_line, 
#         field_name="name", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=32,
#         field_alias="name",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )

# def create_study_area(input_folder):
#     study_area = cf(out_path=input_folder,
#         out_name="study_area",
#         geometry_type="POLYGON",
#         template=None,
#         has_m="ENABLED",
#         has_z="ENABLED",
#         spatial_reference=None
#     )
#     af(in_table=study_area, 
#         field_name="name", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=10,
#         field_alias="name",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )

# def create_study_receivers(input_folder):
#     receivers = cf(out_path=input_folder,
#         out_name="study_receiver",
#         geometry_type="POINT",
#         template=None,
#         has_m="ENABLED",
#         has_z="ENABLED",
#         spatial_reference=None
#     )
#     af(in_table=receivers, 
#         field_name="rec_id", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=10,
#         field_alias="rec_id",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=receivers, 
#         field_name="x", 
#         field_type="DOUBLE",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="x",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=receivers, 
#         field_name="y", 
#         field_type="DOUBLE",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="y",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=receivers, 
#         field_name="z", 
#         field_type="DOUBLE",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="z",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )

# def create_field_measurements(input_folder):
#     receivers = cf(out_path=input_folder,
#         out_name="field_measurement",
#         geometry_type="POINT",
#         template=None,
#         has_m="ENABLED",
#         has_z="ENABLED",
#         spatial_reference=None
#     )
#     af(in_table=receivers, 
#         field_name="rec_id", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=10,
#         field_alias="rec_id",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=receivers, 
#         field_name="x", 
#         field_type="DOUBLE",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="x",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=receivers, 
#         field_name="y", 
#         field_type="DOUBLE",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="y",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=receivers, 
#         field_name="z", 
#         field_type="DOUBLE",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="z",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=receivers, 
#         field_name="dba", 
#         field_type="DOUBLE",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="dba",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=receivers, 
#         field_name="project", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=10,
#         field_alias="project",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
# def create_ground_zone(input_folder):
#     ground_zone = cf(out_path=input_folder,
#         out_name="ground_zone",
#         geometry_type="POLYGON",
#         template=None,
#         has_m="ENABLED",
#         has_z="ENABLED",
#         spatial_reference=None
#     )
#     af(in_table=ground_zone, 
#         field_name="name", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=10,
#         field_alias="name",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=ground_zone, 
#         field_name="type", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=15,
#         field_alias="type",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
# def create_tree_zone(input_folder):
#     tree_zone = cf(out_path=input_folder,
#         out_name="tree_zone",
#         geometry_type="POLYGON",
#         template=None,
#         has_m="ENABLED",
#         has_z="ENABLED",
#         spatial_reference=None
#     )
#     af(in_table=tree_zone, 
#         field_name="name", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=10,
#         field_alias="name",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=tree_zone, 
#         field_name="avg_hgt", 
#         field_type="DOUBLE",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="avg_hgt",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
# def create_building_row(input_folder):
#     building_row = cf(out_path=input_folder,
#         out_name="building_row",
#         geometry_type="POLYLINE",
#         template=None,
#         has_m="ENABLED",
#         has_z="ENABLED",
#         spatial_reference=None
#     )
#     af(in_table=building_row, 
#         field_name="name", 
#         field_type="TEXT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=10,
#         field_alias="name",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=building_row, 
#         field_name="avg_hgt", 
#         field_type="DOUBLE",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="avg_hgt",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )
#     af(in_table=building_row, 
#         field_name="bldg_pct", 
#         field_type="SHORT",
#         field_precision=None,
#         field_scale=None, 
#         field_length=None,
#         field_alias="bldg_pct",
#         field_is_nullable="NULLABLE",
#         field_is_required="NON_REQUIRED",
#         field_domain=None
#     )

# if __name__ == '__main__':
#     pass

create_receivers(r"C:\Users\brbatt\projects\pytnm\tests")