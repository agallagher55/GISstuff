import arcpy
import os
from collections import defaultdict

# Origin field with many different destinations, number of journeys for each
# 1. Get a sum of all the different journeys for each Origin-Destination combination

def summaryStatistics(featureclass, fieldgroup, fieldsum, workspace):
    outputTableName = [fieldgroup, fieldsum].join('_')
    arcpy.CreateTable(workspace, outputTableName
    
    origins = []
    originJourneys = defaultdict(int) #default value of int is 0

    fields = [x.name for x in arcpy.ListFields(featureclass)]
    with arcpy.da.SearchCursor(featureclass, "*") as cursor:
        for row in cursor:
            
            # Names of 'Origin' and 'Journeys' may need to be ammended
            origin = row[fields.index(fieldgroup)]
            journeyTotal = row[fields.index(fieldsum)]
        
            # Sum all of the journeys for each origin-destination pair for each unique origin
            originJourneys[origin] += journeyTotal
    
    # Take resulting dictionary and write to database table
    with arcpy.da.UpdateCursor(os.path.join(workspace, outputTableName), "*") as cursor:
        for row in cursor:
            for key, value in originJourneys.items():
                row[0] = key
                row[1] = value


summaryStatistics(xyLine, 'Origin','Journeys', workspace)