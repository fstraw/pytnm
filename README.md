# Pytnm #
## A module supporting geospatial template creation, geometry conversion, and reporting for noise analyses conducted utilizing the United States Federal Highway Administration's (FHWA) Traffic Noise Model (TNM) 2.5 ##

### Installation
```pip install pytnm```

### Create geospatial template for use in GIS editing software

```
from pytnm.utils import template

output_directory = "~/projects/tnm_project"
# create receiver template
template.create_receivers(output_directory)
# create existing roadway template template
template.create_existing_roadway(output_directory)
# create noise barrier template
template.create_barrier(output_directory)
```
### Convert geospatial template files into STAMINA file, for importing into TNM 2.5

```
from pytnm.utils import stamina

output_directory = "~/projects/tnm_project"
condition = "Existing" | "Build" | "NoBuild" # specify which noise model
receivers = "path/to/receiver.shp"
roadways = "path/to/<existing>|<proposed>_roadway.shp"
barriers = "path/to/barrier.shp"

stamina.write_stamina_file(output_directory, condition, receivers, roadways, barriers)

```
