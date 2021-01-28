import os
import shapefile

def roadway_separator():
    """Syntax for separating individual roadways in STAMINA format
    
    Returns:
        [String] -- [roadway separator]
    """
    separator = "'L' /\n"
    return separator

def barrier_separator():
    """Syntax for separating individual barriers in STAMINA format
    
    Returns:
        [String] -- [barrier separator]
    """
    separator = "'A' /\n"
    return separator

def _write_roadway_points(line_geom):
    """Converts Polyline to STAMINA syntax 
    
    Arguments:
        line_geom {[arcpy.Polyline]} -- [polyline geometry]
    
    Returns:
        [string] -- [roadway points]
    """
    point_strings = ""
    point_strings += roadway_separator()
    elevation_list = line_geom.z # z values read separately from xy data
    for point_number, point in enumerate(line_geom.points):
        x = round(point[0], 1) 
        y = round(point[1], 1)
        z = round(elevation_list[point_number], 1)            
        point_strings += "'Point{}' {} {} {} 0\n".format(point_number, x, y, z)
    return point_strings

def validate_roadway_field(condition):
    if condition == "BUILD":
        return ("auto_bld", "medium_bld", "heavy_bld")
    elif condition == "EXISTING":
        return ("auto_ex", "medium_ex", "heavy_ex")
    elif condition == "NO_BUILD":
        return ("auto_nb", "medium_nb", "heavy_nb")
    else:
        raise ValueError("Feature class must include fields: bld_total, ex_total, nb_total")

def _write_roadways(roadway_feature_class, condition):
    """Writes roadway feature class to STAMINA syntax
    
    Arguments:
        roads_feature_class {String} -- Path to feature class
        condition {String} -- Existing, NoBuild, or Build. Determines fields to use from geospatial template
    Returns:
        [string] -- [roadways]
    """

    roadway_count = len([row for row in shapefile.Reader(roadway_feature_class)])
    with shapefile.Reader(roadway_feature_class) as roadways:
        roadway_string = "2,{}\n".format(roadway_count)
        flds = validate_roadway_field(condition)
        for row in roadways.shapeRecords():
            road = row.record["road_name"]
            speed = row.record["speed"]
            auto = round(row.record[flds[0]], 0)
            medium = round(row.record[flds[1]], 0)
            heavy = round(row.record[flds[2]], 0)
            roadway_string += "{}\n".format(road)
            roadway_string += "CARS {} {}\n".format(auto, speed)
            roadway_string += "MT {} {}\n".format(medium, speed)
            roadway_string += "HT {} {}\n".format(heavy, speed)
            roadway_string += _write_roadway_points(row.shape)
            roadway_string += roadway_separator()
        return roadway_string 

def _write_barrier_points(line_geom, barrier_info=None):
    """Converts Polyline to STAMINA syntax
    
    Arguments:
        line_geom {arcpy.Polyline]} -- [polyline geometry]
    
    Returns:
        [String] -- [barrier points]
    """
    point_strings = ""
    # set constants for barrier defaults TODO: parameterize
    PERTURBATION_INCREMENT = 2 
    NUMBER_OF_PERTURBATIONS = 15    
    BARRIER_INITIAL_HEIGHT = 0
    if barrier_info:
        PERTURBATION_INCREMENT = barrier_info["pert_inc"]
        NUMBER_OF_PERTURBATIONS = barrier_info["pert_num"]    
        BARRIER_INITIAL_HEIGHT = barrier_info["init_hgt"] #TODO: cannot be null, need to account for it
    elevation_list = line_geom.z # z values read separately from xy data
    for point_number, point in enumerate(line_geom.points):
        x = round(point[0], 1) 
        y = round(point[1], 1)
        z = round(elevation_list[point_number], 1) 
        barrier_height = z + BARRIER_INITIAL_HEIGHT
        if point_number == 0:
            point_strings += "'Point{}' {} {} {} {} {} {}\n".format(
                point_number, x, y, barrier_height, z, PERTURBATION_INCREMENT, NUMBER_OF_PERTURBATIONS)                
        else:
            point_strings += "'Point{}' {} {} {} {}\n".format(point_number, x, y, barrier_height, z)
    point_strings += barrier_separator()
    return point_strings

def _write_barriers(barrier_feature_class):
    """Creates string of barrier attributes
    
    Arguments:
        barrier_feature_class {String} -- Path to feature class        
    """
    barrier_count = len([row for row in shapefile.Reader(barrier_feature_class)])
    with shapefile.Reader(barrier_feature_class) as barriers:
        barrier_string = "3,{}\n".format(barrier_count)
        for row in barriers.shapeRecords():
            barrier_info = {
                "pert_inc": row.record["pert_inc"],
                "pert_num": row.record["pert_num"],
                "init_hgt": row.record["init_hgt"]
                }
            name = row.record["name"]
            geometry = row.shape
            barrier_string += "{}\n".format(name)
            barrier_string += _write_barrier_points(geometry, barrier_info)
        return barrier_string

def _write_receivers(receiver_feature_class):
    """Writes receiver feature class to STAMINA format. This method assumes bldg_hgt field is populated.
    For elevations, STAMINA import process will subtract 5 feet (or metric equivalent) from provided Z-value 
    
    Arguments:
        receiver_feature_class {[String]} -- Path to receiver feature class
    """
    receiver_count = len([row for row in shapefile.Reader(receiver_feature_class)])
    receiver_string = "5,{}\n".format(receiver_count)
    receiver_string += "RECEIVERS\n"   
    with shapefile.Reader(receiver_feature_class) as receivers:
        for row in receivers.shapeRecords():         
            rec_id = row.record["rec_id"] # TODO: if no rec id, .dat file does not import properly into TNM 
            bldg_hgt = row.record["bldg_hgt"]            
            x = round(row.shape.points[0][0], 1)
            y = round(row.shape.points[0][1], 1)
            z = round(row.shape.z[0], 1) + bldg_hgt
            receiver_string += "'{}' {} {} {}\n".format(rec_id, x, y, z)
        return receiver_string

def write_stamina_file(file_path, condition, roadways=None, barriers=None, receivers=None):
    """Creates STAMINA file from set of feature classes
    
    Arguments:
        file_path {String} -- Path for output file
        condition {String} -- EXISTING, NOBUILD, or BUILD (case-insensitive)
    
    Keyword Arguments:
        roadways {String} -- Path to roadways feature class (default: {None})
        barriers {String} -- Path to barriers feature class (default: {None})
        receivers {String} -- Path to receivers feature class (default: {None})
    
    Returns:
        [String] -- Path to output STAMINA file
    """
    stamina_string = "1,3\n"
    if roadways:
        stamina_string += _write_roadways(roadways, condition)
    if barriers:
        stamina_string += _write_barriers(barriers)
    if receivers:
        stamina_string += _write_receivers(receivers)
    stamina_string += "7/\n"
    file_obj = open(os.path.join(file_path, "{}.dat".format(condition)), "w")
    file_obj.write(stamina_string)
    return file_path

if __name__ == '__main__':
    pass