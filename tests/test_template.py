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
        assert exists(receivers) == True