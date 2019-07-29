# TWO FEATURES for program
# 1) Feature with null value attributes - nullValuesFeature
# 2) Feature to Reference - Reference Feature

import arcpy
import os

# PRIMARY VARIABLES
workspace = r"Database Connections\Prod_GIS_Halifax.sde"

featureWithNulls = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_outdoor_rec_poly'
featureToReference = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_hrm_parcel_parks\SDEADM.LND_hrm_park'

nullFeatureAssetID = 'ASSETID'
nullFieldName = 'PARK_ID'

editable = True
edit = arcpy.da.Editor(workspace)

nullMatchesDict = {}  # AssetID, ParkID

# DERIVED VARIABLES
featureToReferenceFields = [x.name for x in arcpy.ListFields(featureToReference)]

sql_null = "{} IS NULL".format(nullFieldName)
nullFeatures = [row[0] for row in arcpy.da.SearchCursor(featureWithNulls,
                                                        nullFeatureAssetID,
                                                        where_clause=sql_null)]

arcpy.AddMessage("Found {} assets with null values: {}...".format(len(nullFeatures),
                                                                  nullFeatures[:len(nullFeatures)/10]))

# Check assets for missing values ==> ParkID, LandID, etc.
# How many of these features intersect it's parent feature? aka. number of recpolys, with null park_id, in a park
if len(nullFeatures) > 0:
    arcpy.AddMessage("\nLooking for {} features that intersect {}...".format(os.path.basename(featureWithNulls),
                                                                             os.path.basename(featureToReference)))

    for feature in nullFeatures:
        arcpy.AddMessage("\tProcessing {}...".format(feature))

        # Make Feature Layer
        nullFeatures_layer = feature + "_layer"
        nullFeatures = arcpy.MakeFeatureLayer_management(featureWithNulls,
                                                         nullFeatures_layer,
                                                         where_clause="{} LIKE '{}'".format(nullFeatureAssetID, feature))

        # Null value feature has centre in Parent Feature
        arcpy.SelectLayerByLocation_management(nullFeatures_layer,
                                               "HAVE_THEIR_CENTER_IN",
                                               featureToReference)

        # Get count of features that intersect the park
        numIntersectFeatures = int(arcpy.GetCount_management(nullFeatures_layer).getOutput(0))

        if numIntersectFeatures > 0:  # GET Value for null value

            parkFeatures_layer = arcpy.MakeFeatureLayer_management(featureToReference,
                                                                   "_".join([os.path.basename(featureToReference), feature,
                                                                             "layer"]),
                                                                   )

            # GET WHICH PARKS INTERSECT OUR NULL FEATURES - inverse of before
            arcpy.SelectLayerByLocation_management(parkFeatures_layer,
                                                   "INTERSECT",
                                                   nullFeatures)  # SHOULD BE ABLE TO USE 'nullFeatures'

            with arcpy.da.SearchCursor(parkFeatures_layer, "*") as cursor:
                for row in cursor:
                    parkID = row[featureToReferenceFields.index(nullFieldName)]

            arcpy.AddMessage("\t\t*{} intersects {} where {} is {}".format(feature,
                                                                           os.path.basename(featureToReference),
                                                                           nullFieldName, parkID))

            nullMatchesDict[feature] = parkID

arcpy.AddMessage("\nRESULTS: {} - {}".format(nullFeatureAssetID, nullFieldName))
for assetid, parkid in nullMatchesDict.items():
    arcpy.AddMessage("\t{} - {}".format(assetid, parkid))


# If asset is missing value, select by intersect with matching featureclass to get value
update_sql = '{} in {}'.format(nullFeatureAssetID, tuple(nullMatchesDict.keys()))

if editable is True:
    edit.startEditing(True, True)
    edit.startOperation()

    arcpy.AddMessage("\nUpdating {} WHERE '{}'".format(os.path.basename(featureWithNulls), update_sql))

    with arcpy.da.SearchCursor(featureWithNulls, [nullFeatureAssetID, nullFieldName], where_clause=update_sql) as cursor:
        for row in cursor:
            nullAssetID = row[0]
            for assetid in nullMatchesDict.keys():
                if nullAssetID == assetid:
                    # row[1] = nullMatchesDict[assetid]
                    arcpy.AddMessage("\t{} - Setting {} to {}".format(assetid, nullFieldName, nullMatchesDict[assetid]))

    edit.startOperation()
    edit.stopEditing(True)




