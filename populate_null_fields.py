# TWO FEATURES for program
# 1) Feature with null value attributes - nullValuesFeature
# 2) Feature to Reference - Reference Feature

import arcpy
import os
import sys
import datetime

# BOOLEANS
editable = arcpy.GetParameterAsText(0)
checkMultiFeature = arcpy.GetParameterAsText(1)

# PRIMARY VARIABLES
workspace = arcpy.GetParameterAsText(2)

featureWithNulls = arcpy.GetParameterAsText(3)
fieldWithNull = arcpy.GetParameterAsText(4)
nullFeatureAssetID = arcpy.GetParameterAsText(5)

# Feature to Reference
featureToReference = arcpy.GetParameterAsText(6)
nullReferenceFieldName = arcpy.GetParameterAsText(7)

# NON SCRIPT TOOL TEST PARAMETERS
# editable = 'true'
# checkMultiFeature = 'true'
# workspace = r"Database Connections\Prod_GIS_Halifax.sde"
# Feature with Null attribute
# featureWithNulls = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_outdoor_rec_poly'
# fieldWithNull = 'PARK_ID'
# nullFeatureAssetID = 'ASSETID'


# EMPTY VARIABLES
count = 0
checkManual = []
nullMatchesDict = {}  # AssetID, ParkID
resultText = str(datetime.datetime.now()) + "\nParameters: {}".format("\n\t".join([editable, checkMultiFeature,
                                                                                   workspace, featureWithNulls,
                                                                                   fieldWithNull, nullFeatureAssetID,
                                                                                   featureToReference, nullReferenceFieldName]))
# DERIVED VARIABLES
featureToReferenceFields = [x.name for x in arcpy.ListFields(featureToReference)]

sql_null = "{} IS NULL".format(fieldWithNull)
nullFeatures = [row[0] for row in arcpy.da.SearchCursor(featureWithNulls,
                                                        nullFeatureAssetID,
                                                        where_clause=sql_null)]

arcpy.AddMessage("Found {} assets with null values: {}...".format(len(nullFeatures),
                                                                  (nullFeatures[:5])))
resultText += "\n\nFound {} assets with null values...\n".format(len(nullFeatures))

# Check assets for missing values ==> ParkID, LandID, etc.
# How many of these features intersect it's parent feature? aka. number of recpolys, with null park_id, in a park
if len(nullFeatures) > 0:
    arcpy.AddMessage("\nLooking for {} features that intersect {}...".format(os.path.basename(featureWithNulls),
                                                                             os.path.basename(featureToReference)))
    arcpy.AddMessage("Processing...")
    for feature in nullFeatures:
        arcpy.AddMessage("\t{}...".format(feature))

        # Make Feature Layer
        nullFeatures_layer = str(feature) + "_layer"
        nullFeatures = arcpy.MakeFeatureLayer_management(featureWithNulls,
                                                         nullFeatures_layer,
                                                         where_clause="{} LIKE '{}'".format(nullFeatureAssetID, feature))

        # Null value feature has centre in Parent Feature
        arcpy.SelectLayerByLocation_management(nullFeatures_layer,
                                               "HAVE_THEIR_CENTER_IN",
                                               featureToReference)

        numIntersectFeatures = int(arcpy.GetCount_management(nullFeatures_layer).getOutput(0))
        if numIntersectFeatures > 0:  # GET Value for null value

            parkFeatures_layer = arcpy.MakeFeatureLayer_management(featureToReference,
                                                                   "_".join([os.path.basename(featureToReference),
                                                                             feature,
                                                                             "layer"]),
                                                                   )

            # GET WHICH PARKS INTERSECT OUR NULL FEATURES - inverse of before
            arcpy.SelectLayerByLocation_management(parkFeatures_layer,
                                                   "INTERSECT",
                                                   nullFeatures)  # SHOULD BE ABLE TO USE 'nullFeatures'

            with arcpy.da.SearchCursor(parkFeatures_layer, "*") as cursor:
                for row in cursor:
                    # parkID = row[featureToReferenceFields.index(fieldWithNull)]
                    parkID = row[featureToReferenceFields.index(nullReferenceFieldName)]

            arcpy.AddMessage("\t\t*{} intersects {} where {} is {}".format(feature,
                                                                           os.path.basename(featureToReference),
                                                                           nullReferenceFieldName, parkID))

            # Get count of features that intersect the park
            # IF NUMBER OF INTERSECTS > 1, PUT ASIDE FOR MANUAL REVIEW
            if checkMultiFeature == 'true':
                numIntersectFeaturesII = int(arcpy.GetCount_management(parkFeatures_layer).getOutput(0))

                if numIntersectFeaturesII > 1:
                    count += 1
                    checkManual.append(feature)

            if feature not in checkManual:
                nullMatchesDict[feature] = parkID

arcpy.AddMessage("\n{} features had more than one intersect".format(count))

if len(nullMatchesDict) == 0:
    arcpy.AddMessage("\nNone of your features interesect! Unable to fill in null values.")
    sys.exit()

arcpy.AddMessage("\nRESULTS: {} - {}".format(nullFeatureAssetID, nullReferenceFieldName))

for assetid, parkid in nullMatchesDict.items():
    arcpy.AddMessage("\t{} - {}".format(assetid, parkid))

# If asset is missing value, select by intersect with matching featureclass to get value
update_sql = '{} in {}'.format(nullFeatureAssetID, tuple(nullMatchesDict.keys()))

editCount = 0
if editable == 'true':
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(True, True)
    edit.startOperation()

    arcpy.AddMessage("\nUpdating {} WHERE '{}'".format(os.path.basename(featureWithNulls), update_sql))

    with arcpy.da.UpdateCursor(featureWithNulls, [nullFeatureAssetID, fieldWithNull], where_clause=update_sql) as cursor:
        for row in cursor:
            nullAssetID = row[0]
            for assetid in nullMatchesDict.keys():
                if nullAssetID == assetid:
                    row[1] = nullMatchesDict[assetid]
                    arcpy.AddMessage("\t{} - Setting {} to {}".format(assetid, fieldWithNull, nullMatchesDict[assetid]))

                    cursor.updateRow(row)
                    editCount += 1
                    resultText += "\n\t{} - Set {} to {}".format(assetid, fieldWithNull, nullMatchesDict[assetid])

    edit.startOperation()
    edit.stopEditing(True)

arcpy.AddMessage("Updated {} features in total.".format(editCount))
resultText += "\n\nUpdated {} features in total.".format(editCount)

if len(checkManual) > 0:
    arcpy.AddMessage("Edit these features manually: {}".format(checkManual))

with open(os.path.join(os.path.expanduser('~'),
                       "Downloads",
                       "{}_{}_results.txt".format(os.path.basename(featureWithNulls).split(".")[1], fieldWithNull)
                       ), 'w') as txt_results:
    txt_results.write(resultText)

arcpy.AddMessage("\n\n**CHECK DOWNLOADS FOLDER FOR REPORT OF RESULTS")
