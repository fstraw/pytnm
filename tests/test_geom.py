import pytest

# from pytnm.utils.geom import project_point

# dir_path = os.path.dirname(os.path.realpath(__file__))
# os.chdir(dir_path)    
# test_receiver = "../../tests/test_files/DATA/receiver.shp"
# test_existing_roadway = "../../tests/test_files/DATA/existing_roadway.shp"
# test_barrier = "../../tests/test_files/DATA/barrier.shp"
# raster = r"C:\Users\brbatt\Documents\elevation_NED10M_ga121_3765948_01\elevation\ned10m33084h4.tif"
# update_feature_z(test_barrier, raster)

# class TestRoadwaySeparator:
#     def test_project_point_returns_tuple(self):
#         x = 123
#         y = 456
#         # expected output from transformation
#         expected_output = (0.0040963176920953475, 0.0011049277994670114)
#         converted_coords = project_point(x, y, 3857, 4326)
#         assert converted_coords == expected_output