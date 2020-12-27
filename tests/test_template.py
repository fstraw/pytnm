from os.path import exists
import pytest

import pytnm.utils.template as t

# dir_path = os.path.dirname(os.path.realpath(__file__))
# os.chdir(dir_path)    
# test_receiver = "../../tests/test_files/DATA/receiver.shp"
# test_existing_roadway = "../../tests/test_files/DATA/existing_roadway.shp"
# test_barrier = "../../tests/test_files/DATA/barrier.shp"
# raster = r"C:\Users\brbatt\Documents\elevation_NED10M_ga121_3765948_01\elevation\ned10m33084h4.tif"
# update_feature_z(test_barrier, raster)

INPUT_FOLDER = "./"

class TestCreateReceivers:
    def test_creates_receiver_shapefile(self):
        receivers = t.create_receivers(INPUT_FOLDER)
        assert exists(receivers)

class TestCreateExistingRoadway:
    def test_creates_existing_roadway_shapefile(self):
        existing_roadway = t.create_existing_roadway(INPUT_FOLDER)
        assert exists(existing_roadway)

class TestCreateProposedRoadway:
    def test_creates_proposed_roadway_shapefile(self):
        proposed_roadway = t.create_proposed_roadway(INPUT_FOLDER)
        assert exists(proposed_roadway)

class TestCreateBarrier:
    def test_creates_barrier_shapefile(self):
        barrier = t.create_barrier(INPUT_FOLDER)
        assert exists(barrier)

class TestCreateTerrainLine:
    def test_creates_terrain_line_shapefile(self):
        terrain_line = t.create_terrain_line(INPUT_FOLDER)
        assert exists(terrain_line)

class TestCreateStudyArea:
    def test_creates_study_area_shapefile(self):
        study_area = t.create_study_area(INPUT_FOLDER)
        assert exists(study_area)

class TestCreateStudyReceivers:
    def test_creates_study_receivers_shapefile(self):
        study_receivers = t.create_study_receivers(INPUT_FOLDER)
        assert exists(study_receivers)

class TestCreateFieldMeasurements:
    def test_creates_field_measurement_shapefile(self):
        field_measurement = t.create_field_measurements(INPUT_FOLDER)
        assert exists(field_measurement)

class TestCreateGroundArea:
    def test_creates_ground_area_shapefile(self):
        ground_area = t.create_ground_area(INPUT_FOLDER)
        assert exists(ground_area)

class TestCreateTreeZone:
    def test_creates_tree_zone_shapefile(self):
        tree_zone = t.create_tree_zone(INPUT_FOLDER)
        assert exists(tree_zone)

class TestCreateBuildingRow:
    def test_creates_building_row_shapefile(self):
        building_row = t.create_building_row(INPUT_FOLDER)
        assert exists(building_row)