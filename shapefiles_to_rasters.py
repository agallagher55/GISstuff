import os
import arcpy

# Primary Variables
mainDir = r'C:\Users\gallaga\Desktop\rasterTesting'
serviceAreasDir = r'C:\Users\gallaga\Desktop\rasterTesting\ServiceAreas\RC_ServiceAreas_Individual'

# Derived Variables
areasDir = os.path.join(mainDir, 'Grids', 'Areas')
populationsDir = os.path.join(mainDir, 'Grids', 'Populations')

# Environment Settings
arcpy.env.workspace = serviceAreasDir
arcpy.env.overwriteOutput = True

serviceAreas = arcpy.ListFeatureClasses()

def shapefiles_to_rasters(shapefilelocation, field, outputfolder, cellsize):
    arcpy.env.workspace = shapefilelocation
    shapefiles = arcpy.ListFeatureClasses()
    failed_shapfiles = []

    for shapefile in shapefiles:
        print "Coverting {}...".format(shapefile)
        try:
            arcpy.FeatureToRaster_conversion(shapefile,
                                             field,
                                             os.path.join(outputfolder, shapefile.strip('.shp')),
                                             cellsize)
        except Exception as e:
            print "\t{}".format(e)
            print "\tUnable to convert {} to raster!".format(shapefile)
            failed_shapfiles.append(shapefile)

    print "\n{} conversions failed.\n\t{}".format(len(failed_shapfiles), failed_shapfiles)

# shapefiles_to_rasters(serviceAreasDir, 'Park_ha', areasDir, 100)
# shapefiles_to_rasters(serviceAreasDir, 'SA_pop', populationsDir, 100)

from arcpy.sa import *

def grid_total(workspace, outputrastername):
    try:
        arcpy.CheckExtension("Spatial") == "Available"
        arcpy.CheckOutExtension("Spatial")

        arcpy.env.workspace = workspace
        areaRasters = arcpy.ListRasters()

        # ADD all area rasters together
        areaRasterCalc = [Raster(x) for x in areaRasters]
        areaRasterCalc = sum(areaRasterCalc)
        # areaRasterCalc = CellStatistics(areaRasterCalc, "SUM", "NODATA")
        areaRasterCalc.save(os.path.join(areasDir, outputrastername))

    except Exception as e:
        print "\t{}".format(e)

    # https: // gis.stackexchange.com / questions / 285580 / arcpy - add - rasters - using - raster - calculator


# grid_total(areasDir, 'AreasSumCalc')
grid_total(populationsDir, 'PopulationSumCalc')

arcpy.env.workspace = populationsDir
popRasters = arcpy.ListRasters()

# AVERAGE all population rasters together
# avgRasterCalc = [Raster(x) for x in popRasters]
# avgRasterCalc.save(os.path.join(populationsDir, "PopulationAvgCalc"))

# raster1 = r'C:\Users\gallaga\Desktop\rasterTesting\Grids\Populations\997'
# raster2 = r'C:\Users\gallaga\Desktop\rasterTesting\Grids\Populations\996'
#
# if arcpy.CheckExtension("Spatial") == "Available":
#     arcpy.CheckOutExtension("Spatial")
# else:
#     print "*Spatial Anaylst not available"
#
# from arcpy.sa import *
# sumRaster = (Raster(raster1) + Raster(raster2)) /2
# sumRaster.save(r'C:\Users\gallaga\Desktop\rasterTesting\Grids\Populations\avgRaster')

print "Finished Processing"