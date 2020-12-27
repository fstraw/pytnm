# Pytnm #
## A module supporting geospatial template creation, geometry conversion, and reporting for noise analyses conducted utilizing the United States Federal Highway Administration's (FHWA) Traffic Noise Model (TNM) 2.5 ##

### Installation
```pip install pytnm```

### Create geospatial template for use in GIS editing software

```
import pytnm
output_directory = "~/projects/tnm_project"
# create receiver template
pytnm.utils.template.create_receivers(output_directory)
# create existing roadway template template
pytnm.utils.template.create_existing_roadways(output_directory)
# create noise barrier template
pytnm.utils.template.create_barriers(output_directory)
```
### Convert geospatial template files into STAMNA file, for importing into TNM 2.5

```
import pytnm

output_directory = "~/projects/tnm_project"
condition = "Existing" | "Build" | "NoBuild" # specify which noise model
receivers = "path/to/receiver.shp"
roadways = "path/to/<existing>|<proposed>_roadway.shp"
barriers = "path/to/barrier.shp"

pytnm.utils.stamina.write_stamina_file(output_directory, condition, receivers, roadways, barriers)

```