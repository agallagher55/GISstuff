import arcpy
import os
from collections import defaultdict

# Origin field with many different destinations, number of journeys for each
# 1. Get a sum of all the different journeys for each Origin-Destination combination


def summaryStatistics(featureclass, fieldgroup, fieldsum, workspace):
    outputTableName = '_'.join([fieldgroup.split('.')[1], fieldsum.split('.')[1]])
    arcpy.AddMessage("Getting Summary Statistics for: {}".format(outputTableName))

    # if not arcpy.Exists(os.path.join(workspace, outputTableName)):
    #     arcpy.CreateTable_management(workspace, outputTableName)
    if arcpy.Exists(os.path.join(workspace, outputTableName)):
        arcpy.Delete_management(os.path.join(workspace, outputTableName))
    arcpy.CreateTable_management(workspace, outputTableName)

    # Add Fields
    for field in [fieldgroup, fieldsum]:
        field = field.split('.')[1]
        if field not in [x.name for x in arcpy.ListFields(os.path.join(workspace, outputTableName))]:
            try:
                arcpy.AddField_management(in_table=os.path.join(workspace, outputTableName),
                                          field_name=field,
                                          field_type='DOUBLE')
                arcpy.AddMessage("Added Field: '{}'".format(field))
            except:
                arcpy.AddMessage("**Not able to add field: '{}'".format(field))

    originJourneys = defaultdict(int)  # default value of int is 0

    with arcpy.da.SearchCursor(featureclass, [fieldgroup, fieldsum], where_clause='{} > 0'.format(fieldsum)) as cursor:
        iCursor = arcpy.da.InsertCursor(os.path.join(workspace, outputTableName), [fieldgroup.split('.')[1], fieldsum.split('.')[1]])
        for row in cursor:
            origin = row[0]
            journeyTotal = row[1]

            arcpy.AddMessage("Census Tract: {}\tJourney Total: {}".format(origin, journeyTotal))

            # Sum all of the journeys for each origin-destination pair for each unique origin\
            originJourneys[origin] += journeyTotal

        arcpy.AddMessage("Updating Output table...")
        for key, value in originJourneys.items():
            iCursor.insertRow((key, value))
        arcpy.AddMessage("Finished updating.")
        del iCursor

