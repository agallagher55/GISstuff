"""
DATE: July 16, 2019
AUTHOR: Alex Gallagher
PURPOSE: Analyze Stats Can. commuting data
NOTES: Excel sheet should have three columns - ORIGIN CENSUS TRACT, DESTINATION CENSUS TRACT, NUMBER OF COMMUTERS
"""
import os
import arcpy
from collections import defaultdict

# arcpy.env.overwriteOutput = True

# DYNAMIC VARIABLES
statsCanExcel = arcpy.GetParameterAsText(0)
workspace = arcpy.GetParameterAsText(1)

# DERIVED & STATIC VARIABLES
censusCentroids = r'R:\ICT\ICT BIDS\Mapping Services\ArcGIS_Online\Proposed - Interactive Maps\Journey To Work\Data\JTW.gdb\CensusTrack_Centroid_FNL'
statsCanTable = os.path.join(workspace, 'statsCanData')

try:
    # EXCEL TO TABLE
    if arcpy.Exists(statsCanTable):
        arcpy.Delete_management(statsCanTable)

    arcpy.AddMessage("Creating Table from Excel...")
    arcpy.ExcelToTable_conversion(statsCanExcel, statsCanTable)

    # Test target field
    journeysTotalFieldName = [x.name for x in arcpy.ListFields(statsCanTable)][3]  # Have to factor in Object ID field
    arcpy.AddMessage("Transit Field: {}".format(journeysTotalFieldName))

    # ADD 5 FIELDS


    def addfields(featureclass, fields, fieldtype):
        arcpy.env = os.path.dirname(featureclass)

        arcpy.AddMessage("\nAdding Fields...")
        for field in fields:
            if field not in [x.name for x in arcpy.ListFields(featureclass)]:
                try:
                    arcpy.AddField_management(in_table=featureclass, field_name=field, field_type=fieldtype)
                    arcpy.AddMessage("\tAdded Field: '{}'".format(field))
                except:
                    arcpy.AddMessage("**Not able to add field: '{}'".format(field))


    fieldsAdd = ["ORIGIN_X", "ORIGIN_Y", "DESTINATION_X", "DESTINATION_Y", "ID"]
    addfields(statsCanTable, fieldsAdd, 'DOUBLE')

    # Join Tables
    arcpy.AddMessage("\nJoining Tables...")
    if arcpy.Exists("statsCanTableView"):
        arcpy.Delete_management("statsCanTableView")
    statsCanTableView = arcpy.MakeTableView_management(statsCanTable, "statsCanTableView")
    joinedTable = arcpy.AddJoin_management(statsCanTableView, 'ORIGIN', censusCentroids, 'CENSUS_TRACT')

    # Calculate Origin X, Origin Y
    # Origin X = [CTRPLONG] & Origin Y = [CTRPLAT]
    expression_lon = '!CensusTrack_Centroid_FNL.CTRPLAT!'
    expression_lat = '!CensusTrack_Centroid_FNL.CTRPLONG!'
    arcpy.AddMessage("\tCalculating Fields...")
    arcpy.CalculateField_management(joinedTable, 'statsCanData.ORIGIN_X', expression_lat, 'PYTHON')
    arcpy.CalculateField_management(joinedTable, 'statsCanData.ORIGIN_Y', expression_lon, 'PYTHON')

    # REMOVE
    arcpy.RemoveJoin_management(statsCanTableView)
    arcpy.AddMessage("\t\tRemoved Join.")

    # ADD JOIN -> Destination ID - Census Tract
    joinedTable = arcpy.AddJoin_management(statsCanTableView, 'DESTINATION', censusCentroids, 'CENSUS_TRACT')

    # CACLULATE DESTINATION X & Y
    arcpy.AddMessage("\tCalculating Fields...")
    arcpy.CalculateField_management(joinedTable, 'statsCanData.DESTINATION_X', expression_lat, 'PYTHON')
    arcpy.CalculateField_management(joinedTable, 'statsCanData.DESTINATION_Y', expression_lon, 'PYTHON')

    arcpy.RemoveJoin_management(statsCanTableView)
    arcpy.AddMessage("\t\tRemoved Join.")

    arcpy.CalculateField_management(joinedTable, 'ID', '!OBJECTID!', 'PYTHON')

    # EXPORT RESULTS TO TABLE
    joinedTableDir = os.path.join(workspace, 'joinTable')

    if arcpy.Exists(joinedTableDir):
        arcpy.Delete_management(joinedTableDir)
        arcpy.CopyRows_management(joinedTable, joinedTableDir)
    else:
        arcpy.CopyRows_management(joinedTable, joinedTableDir)


    # XY TO LINE
    arcpy.AddMessage("\nProcessing XY to Line...")
    xyLineFC = os.path.join(workspace, 'XYLine_{}'.format(journeysTotalFieldName))

    if arcpy.Exists(xyLineFC):
        arcpy.Delete_management(xyLineFC)

    try:
        # joinedTable_layer = arcpy.MakeTableView_management(joinedTableDir, 'joinedTable')
        joinedTable_view = arcpy.MakeTableView_management(joinedTableDir, 'joinedTableView')
        xyLine = arcpy.XYToLine_management(in_table=joinedTable_view,
                                           out_featureclass=xyLineFC,
                                           startx_field='ORIGIN_X',
                                           starty_field='ORIGIN_Y',
                                           endx_field='DESTINATION_X',
                                           endy_field='DESTINATION_Y',
                                           id_field='ID',
                                           spatial_reference=censusCentroids
                                           )
        arcpy.AddMessage("\tXY to Line Complete.")
    except Exception as e:
        arcpy.AddMessage("\t{}".format(e))

    joinedTable_layer = arcpy.MakeTableView_management(joinedTableDir, 'joinedTable')
    xyLine_layer = arcpy.MakeFeatureLayer_management(xyLineFC, "xyLine")  # Try using table view...
    xyJoinedTable = arcpy.AddJoin_management(xyLine_layer, 'OID', joinedTable_layer, 'ID')

    if arcpy.Exists(os.path.join(workspace, "joinedTablePreSum")):
        arcpy.Delete_management(os.path.join(workspace, "joinedTablePreSum"))
        arcpy.AddMessage("Deleted joinedTablePreSum")


    def summaryStatistics(featureclass, fieldgroup, fieldsum, workspace):
        outputTableName = '_'.join([fieldgroup.split('.')[1], fieldsum.split('.')[1], 'SUM'])

        # if not arcpy.Exists(os.path.join(workspace, outputTableName)):
        #     arcpy.CreateTable_management(workspace, outputTableName)
        if arcpy.Exists(os.path.join(workspace, outputTableName)):
            arcpy.Delete_management(os.path.join(workspace, outputTableName))
        arcpy.CreateTable_management(workspace, outputTableName)
        arcpy.AddMessage("Created Output table for Sum Stats")

        # Add Fields
        for field in [fieldgroup, fieldsum]:
            field = field.split('.')[1]
            if field not in [x.name for x in arcpy.ListFields(os.path.join(workspace, outputTableName))]:
                try:
                    arcpy.AddField_management(in_table=os.path.join(workspace, outputTableName),
                                              field_name=field,
                                              field_type='DOUBLE')
                    arcpy.AddMessage("\tAdded Field: '{}'".format(field))
                except:
                    arcpy.AddMessage("**Not able to add field: '{}'".format(field))

        originJourneys = defaultdict(int)  # default value of int is 0

        arcpy.AddMessage("\nGetting Summary Statistics for: {}...".format(outputTableName))
        with arcpy.da.SearchCursor(featureclass, [fieldgroup, fieldsum], where_clause='{} > 0'.format(fieldsum)) as cursor:
            iCursor = arcpy.da.InsertCursor(os.path.join(workspace, outputTableName), [fieldgroup.split('.')[1], fieldsum.split('.')[1]])
            for row in cursor:
                origin = row[0]
                journeyTotal = row[1]

                arcpy.AddMessage("\tCensus Tract: {}\tJourney Total: {}".format(origin, journeyTotal))

                # Sum all of the journeys for each origin-destination pair for each unique origin\
                originJourneys[origin] += journeyTotal

            arcpy.AddMessage("\n\tUpdating Output table...")
            for key, value in originJourneys.items():
                iCursor.insertRow((key, value))
            arcpy.AddMessage("\t\tFinished updating.")
            del iCursor


    summaryStatistics(xyJoinedTable, 'joinTable.ORIGIN', 'joinTable.{}'.format(journeysTotalFieldName), workspace)
    summaryStatistics(xyJoinedTable, 'joinTable.DESTINATION', 'joinTable.{}'.format(journeysTotalFieldName), workspace)

    arcpy.AddMessage("Finished Processing.")

except Exception as e:
    arcpy.AddMessage("Unable to process: {}".format(statsCanExcel))
    arcpy.AddMessage(e)
