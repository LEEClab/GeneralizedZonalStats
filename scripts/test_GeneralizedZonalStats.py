#---------------------------------------------------------------------------------------
"""
 Script to test generalized zonal stats in GRASS GIS
 Bernardo B. S. Niebuhr - bernardo_brandaum@yahoo.com.br
 
 Laboratorio de Ecologia Espacial e Conservacao
 Universidade Estadual Paulista - UNESP
 Rio Claro - SP - Brasil
 This script runs in GRASS GIS 7.X environment.
"""
#--------------------------------------------------------------------------------------- 

#------------------
# 1.
# First create a GRASS GIS location based on the input shapefile and open GRASS within it

# Open python
python

# Import modules
import os
import grass.script as grass
import subprocess
import time

#------------------
# 2.
# Import files

# Set folder where input files are
input_dir = r'/home/leecb/Github/GeneralizedZonalStats/input_files_zonal_stats'
os.chdir(input_dir)

# Import shape file (municipalities of South Brazil)
shape_name = 'mun_teste_wgs84'
grass.run_command('v.in.ogr', input = shape_name+'.shp', output = shape_name, overwrite = True)

# Import rasters (areas of Eucalyptus plantation in 2001-2004)
maps = ['BR_2001_euca_9', 'BR_2002_euca_9', 'BR_2003_euca_9', 'BR_2004_euca_9']
for i in maps:
    grass.run_command('r.in.gdal', input = i+'.tif', output = i, overwrite = True)

#------------------
# 3.
# Run patch size metric (only for number of patches)

# To calculate the number of patches in each municipality, we will need a map of patch ID, which
# identifies habitat patches and sets an ID for each of them
# It may be done, e.g., running LSMetrics - it is necessary to calculate the metric "patch size"
# More info here: https://github.com/LEEClab/LS_METRICS/

# We can leave python, change to LSMetrics script dir and run the LSMetrics script there
# Or, here, we will call the script from within GRASS
lsmetrics_dir = r'/home/leecb/Github/LS_METRICS/_LSMetrics_v1_0_0'
os.chdir(lsmetrics_dir)

# Run LSMetrics
subprocess.call('python LSMetrics_v1_0_0.py', shell=True) # runs and wait
# Here it is important to decide whether pixels on the diagonal will be considered as the same patch or not!!

#------------------
# 4.
# Run zonal stats

# We will use the Patch ID map to calculate the number of patches within a shapefile feature (municipality in this example)
# We will use the binary eucaliptus map to calculate the proportion of eucaliputs within a shapefile feature (municipality in this example)

# Change to the script folder!
script_dir = r'/home/leecb/Github/GeneralizedZonalStats/scripts'
os.chdir(script_dir)

# Import GeneralizedZonalStats class and functions
from GeneralizedZonalStats import GeneralizedZonalStats, proportion_habitat, number_patches

#------------------
# 4.1.
# Running for proportion of eucalyptus for only 1 year - 2001

# Input shape and raster
input_shp = 'mun_teste_wgs84'
input_rast = ['BR_2001_euca_9']

# Initialize and select maps to be used in zonal stats
teststats = GeneralizedZonalStats(input_shape = input_shp, input_rasters = input_rast, folder = input_dir)

# Create new cols
cols = ['p_euc_2001'] # Column name
col_type = ['float'] # Column type

# WARNING! GRASS GIS does not like col names longer than 8-10 characters, so try to be very concise!!

# Create cols
teststats.create_new_column(column_names = cols, type_col=col_type)

# Calculate proportion of eucaliptus in each feature using proportion_habitat function
teststats.run_zonal_stats(proportion_habitat)

# Export shapefile
os.chdir(input_dir)
# export shape file
#grass.run_command('v.out.ogr', input = shape_name, output = shape_name+'_prop_euca.shp', overwrite = True)
# export db in csv format
#grass.run_command('db.out.ogr', input = shape_name, output = shape_name+'_prop_euca.csv')

#------------------
# 4.2.
# Running for proportion of eucalyptus for only 3 years - 2002-2004

# Input shape and rasters
input_shp = 'mun_teste_wgs84'
input_rast = ['BR_2002_euca_9', 'BR_2003_euca_9', 'BR_2004_euca_9']

# Initialize and select maps to be used in zonal stats
test_prop_euca = GeneralizedZonalStats(input_shape = input_shp, input_rasters = input_rast, folder = input_dir)

# Create new cols
cols = ['p_eu_2002', 'p_eu_2003', 'p_eu_2004'] # Col name
col_type = ['float', 'float', 'float'] # Col type

# WARNING! GRASS GIS does not like col names longer than 8-10 characters, so be very concise!!

# Create cols
test_prop_euca.create_new_column(column_names = cols, type_col=col_type)

# Monitoring time
start = time.time()

# Calculate proportion of eucalyptus in each feature using proportion_habitat function
test_prop_euca.run_zonal_stats(proportion_habitat)

# Monitoring time
end = time.time()

# Print total time
print 'The zonal stats for prop of habitat for 3 years took us '+str((end - start)/60)+' minutes.'

# Export shapefile
os.chdir(input_dir)
# export shape file
#grass.run_command('v.out.ogr', input = shape_name, output = shape_name+'_prop_euca.shp', overwrite = True)
# export db in csv format
#grass.run_command('db.out.ogr', input = shape_name, output = shape_name+'_prop_euca.csv')

#------------------
# 4.3.
# Running for number of patches for 2001-2004

# Input shape and rasters
input_shp = 'mun_teste_wgs84'
input_rast = ['BR_2001_euca_9_pid', 'BR_2002_euca_9_pid', 'BR_2003_euca_9_pid', 'BR_2004_euca_9_pid']

# Initialize and select maps to be used in zonal stats
test_np = GeneralizedZonalStats(input_shape = input_shp, input_rasters = input_rast, folder = input_dir)

# Create new cols
cols = ['np_2001', 'np_2002', 'np_2003', 'np_2004'] # Col names
col_type = ['int', 'int', 'int', 'int'] # Col type

# WARNING! GRASS GIS does not like col names longer than 8-10 characters, so try to be very concise!!

# Create cols
test_np.create_new_column(column_names = cols, type_col = col_type)

# Monitoring time
start = time.time()

# Calculate number of patches (clumps) of eucalyptus in each feature using number_patches function
test_np.run_zonal_stats(number_patches, mask = True)

# Monitoring time
end = time.time()

# Print total time
print 'The zonal stats for number of patches for 3 years took us '+str((end - start)/60)+' minutes.'

# Export shapefile
os.chdir(input_dir)
# export shape file
grass.run_command('v.out.ogr', input = shape_name, output = shape_name+'_prop_euca_np.shp', overwrite = True)

#-------------------------------------------------------------------------
# Do not run below!!!!
# Other tests
python 

import os
import grass.script as grass
import grass.script.vector as v
import grass.script.raster as r
import grass.script.db as db

cat = '20'

input_shape = 'mun_teste_wgs84'
input_raster = 'BR_2001_euca_9'
col = 'proportion_euca'

# Take resolution from raster map
rast_info = r.raster_info(input_raster)
ewres = rast_info['ewres']
nsres = rast_info['nsres']
ewres
nsres

# Create a raster for the feature
grass.run_command('g.region', vector = input_shape, ewres = ewres, nsres = nsres, align = input_raster)
grass.run_command('v.to.rast', input = input_shape, output = 'temp_rast', cats = cat, use='val', overwrite = True)

# Set region to the feature
grass.run_command('g.region', raster = 'temp_rast', zoom = 'temp_rast') 

# Run r.mask for the feature
grass.run_command('r.mask', vector = input_shape, cats = cat)

prop = proportion_habitat(input_raster)

grass.run_command('v.db.update', map = input_shape, column = col, value = str(prop), where='cat = '+cat)

grass.run_command('r.mask', flags = 'r')

#---------------
# test proportion_habitat function
# Open python
python

# Import modules
import os
import grass.script as grass

# Change to the script folder
# home/leecb/Github/GeneralizedZonalStats??
script_dir = r'/home/leecb/Github/GRASS-GIS-Landscape-Metrics/scripts'
os.chdir(script_dir)

# Import GeneralizedZonalStats class
from GeneralizedZonalStats import GeneralizedZonalStats, proportion_habitat

input_rast = ['BR_2001_euca_9']
proportion_habitat(input_rast)
