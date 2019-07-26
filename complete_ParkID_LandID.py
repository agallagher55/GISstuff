import arcpy
import os

# PRIMARY VARIABLES
workspace = r"Database Connections\Prod_GIS_Halifax.sde"
parkRecPoly = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_outdoor_rec_poly'
parksFeature = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_hrm_parcel_parks\SDEADM.LND_hrm_park'

nullFeatureAssetID = 'ASSETID'
nullFieldName = 'PARK_ID'

nullMatchesDict = {}  # AssetID, ParkID

# TWO FEATURES for program
# 1) Feature with null value attributes - nullValuesFeature
# 2) Feature to Reference - Reference Feature

# Select all assets with null values
referenceFeatureFields = [x.name for x in arcpy.ListFields(parksFeature)]

sql_null = "{} IS NULL".format(nullFieldName)
nullFeatures = [row[0] for row in arcpy.da.SearchCursor(parkRecPoly,
                                                        nullFeatureAssetID,
                                                        where_clause=sql_null)]

arcpy.AddMessage("Found {} assets with null values.".format(len(nullFeatures)))
arcpy.AddMessage(nullFeatures)


# Check assets for missing values ==> ParkID, LandID, etc.
# How many of these features intersect it's parent feature? aka. number of recpolys, with null park_id, in a park
if len(nullFeatures) > 0:
    arcpy.AddMessage("\nRunning Intersect Analysis...")

    for feature in nullFeatures:
        arcpy.AddMessage("\n\tProcessing Asset: {}".format(feature))

        nullFeatures_layer = feature + "_layer"
        nullFeatures = arcpy.MakeFeatureLayer_management(parkRecPoly,
                                                         nullFeatures_layer,
                                                         where_clause="{} LIKE '{}'".format(nullFeatureAssetID, feature))

        # Null value feature has centre in Parent Feature
        arcpy.SelectLayerByLocation_management(nullFeatures_layer,
                                               "HAVE_THEIR_CENTER_IN",
                                               parksFeature)

        numIntersectFeatures = int(arcpy.GetCount_management(nullFeatures_layer).getOutput(0))

        if numIntersectFeatures > 0:  # GET Value for null value
            arcpy.AddMessage("\t\tIntersected Features: {}".format(numIntersectFeatures))

            # GET UNIQUE IDS TO MAKE DATABASE EDITS
            # What is the PARK ID??
            # park feature to layer, intersect

            parkFeatures_layer = arcpy.MakeFeatureLayer_management(parksFeature,
                                                                   "_".join([os.path.basename(parksFeature), feature, "layer"]),
                                                                   )

            nullFeature_layer = arcpy.MakeFeatureLayer_management(parkRecPoly,
                                                                  "_".join([os.path.basename(parkRecPoly), feature,
                                                                            "layer"]),
                                                                  where_clause="{} LIKE '{}'".format(nullFeatureAssetID, feature)
                                                                  )

            arcpy.SelectLayerByLocation_management(parkFeatures_layer,
                                                   "INTERSECT",
                                                   nullFeature_layer)

            with arcpy.da.SearchCursor(parkFeatures_layer, "*") as cursor:
                for row in cursor:
                    parkID = row[referenceFeatureFields.index(nullFieldName)]

            arcpy.AddMessage("\t\tParkID: {}".format(parkID))
            nullMatchesDict[feature] = parkID

arcpy.AddMessage("\nRESULTS: assetid - parkid")
for assetid, parkid in nullMatchesDict.items():
    arcpy.AddMessage("\t{} - {}".format(assetid, parkid))


# If asset is missing value, select by intersect with matching featureclass to get value
update_sql = '{} in {}'.format(nullFeatureAssetID, tuple(nullMatchesDict.keys()))

arcpy.AddMessage("update_sql: {}".format(update_sql))

with arcpy.da.SearchCursor(parkRecPoly, [nullFeatureAssetID, nullFieldName], where_clause=update_sql) as cursor:
    for row in cursor:
        print row
        for assetid in nullMatchesDict.keys():
            if row[0] == assetid:
                print assetid
                # row[1] = nullMatchesDict[assetid]
                print nullMatchesDict[assetid]

        # for assetid, parkid in nullMatchesDict.items():


