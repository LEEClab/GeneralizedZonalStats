# GeneralizedZonalStats
# Description 
Scripts and tests for calculating a wide array of functions ans statistics for multiple rasters using zonal masks within GRASS GIS

# Scripts

### [GeneralizedZonalStats.py](https://github.com/LEEClab/GeneralizedZonalStats/blob/master/GeneralizedZonalStats.py)

### [test_GeneralizedZonalStats.py](https://github.com/LEEClab/GeneralizedZonalStats/blob/master/test_GeneralizedZonalStats.py)

# Functions implemented for zonal statistics in GeneralizedZonalStats:
+ create_new_columns: auxiliary function to store landscape metrics in the attribute table of a ESRI shapefile
+ number_patches: calculates number of unique patches based on patch identification (pid) raster. Patches are counted as unique from the original raster for the entire region, and are not cut from zonal mask. The pid rasters can be easily generated from [LSMetrics](https://github.com/LEEClab/LS_METRICS)
+ proportion_habitat: calculates proportion of cells with value equals to 1 in a binary raster
+ run_zonal_stats: applies functions of interest for landscape metrics on the shapefile containing multiple polygons 

### Last version of LSmetrics tested available at
[https://github.com/LEEClab/LS_METRICS](https://github.com/LEEClab/LS_METRICS)

### Original scripts
[https://github.com/LEEClab/GeneralizedZonalStats](https://github.com/LEEClab/GeneralizedZonalStats)

#### Helpful Comments

- The script which calculates patch number in zonal statistics depends on LSmetrics outputs of pids (patch id info); 
- LSmetrics gui works well for a single raster, but fot running the option for a sequence of rasters with a string common pattern in raster file name, you must use the symbol "*": 
for example, if the file names' common pattern is all that starts with BR, put: BR *;
if it is all that has "forest" in the middle of file name, put: * forest *;
if it's all that ends with forest_albers, type: * forest_albers in the white box of LSmetrics (Pattern).

#### Important tips for running python script without copying and pasting code in Python Grass

+ Use an auxiliary set of five lines as a starter, so you don´t need to type anything else on the terminal
+ Always type code in the black terminal screen. The python shell in GRASS GIS DO NOT run well all the defs created!!!
+ Remove the command python from inner script. If you let it there, the code will stop, since from the auxiliary code you already got into python inside GRASS command line. However, if you could call a python code from GRASS command line without calling python first, then the auxiliary code would change. But I don´t know how to start a large script differently;

### The auxiliary starter code has five lines

+ python # calls python in GRASS 
+ import os # allows changing directory
+ import grass.script as grass # allows importing scripts
+ os.chdir('WORKDIR') # set directory where the script was saved
+ import SCRIPT # imports the script and make your life easier
+ After that, if everything is correctly written in the script, you can wait for the results and rest.

If you have questions, contact us:

Name |Email 
--- | --- 
**Bernardo Niebuhr** | bernardo_brandaum@yahoo.com.br 
**Renata Muylaert** | renatamuy@gmail.com 

