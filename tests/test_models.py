# import pytest
# import pytnm.utils.stamina as s


# test_existing_roadway = "../../tests/test_files/DATA/existing_roadway.shp"
# test_barrier = "../../tests/test_files/DATA/barrier.shp"
# test_receiver = "../../tests/test_files/DATA/receiver.shp"
# dir_path = os.path.dirname(os.path.realpath(__file__))
# os.chdir(dir_path)    
# test_road_geom = [row[0] for row in SearchCursor(test_existing_roadway, "SHAPE@")][0]
# test_barrier_geom = [row[0] for row in SearchCursor(test_barrier, "SHAPE@")][0]
# print(write_stamina_file(r"C:\TNM25\Program", "EXISTING", test_existing_roadway, test_barrier, test_receiver))

# class TestRoadwaySeparator:
#     def test_returns_header_string(self):
#         fixture = "'L' /\n"
#         separator = s.roadway_separator()
#         assert separator == fixture

# class TestBarrierSeparator:
#     def test_returns_header_string(self):
#         fixture = "'A' /\n"
#         separator = s.barrier_separator()
#         assert separator == fixture