import os
import arcpy

# PIMARY VARIABLES
workspace = r'R:\ICT\ICT BIDS\Mapping Services\ArcGIS_Online\Proposed - Interactive Maps\Journey To Work\alex\New File Geodatabase.gdb'
statsCanExcel = r"R:\ICT\ICT BIDS\Mapping Services\ArcGIS_Online\Proposed - Interactive Maps\Journey To Work\Spreadsheets\All_Modes.xlsx"
statsCanTable = os.path.join(workspace, 'statsCanData')
censusCentroids = r'R:\ICT\ICT BIDS\Mapping Services\ArcGIS_Online\Proposed - Interactive Maps\Journey To Work\Data\JTW.gdb\CensusTrack_Centroid_FNL'

# EXCEL TO TABLE
if not arcpy.Exists(statsCanTable):
    arcpy.AddMessage("Creating Table from Excel...")
    statsCanTable = arcpy.ExcelToTable_conversion(statsCanExcel, statsCanTable)


# ADD 5 FIELDS
def addfields(featureclass, fields, fieldtype):
    arcpy.env = os.path.dirname(featureclass)

    arcpy.AddMessage("Adding Fields...")
    for field in fields:
        if field not in [x.name for x in arcpy.ListFields(featureclass)]:
            try:
                arcpy.AddField_management(in_table=featureclass, field_name=field, field_type=fieldtype)
                arcpy.AddMessage("Added Field: '{}'".format(field))
            except:
                arcpy.AddMessage("**Not able to add field: '{}'".format(field))


fieldsAdd = ["ORIGIN_X", "ORIGIN_Y", "DESTINATION_X", "DESTINATION_Y", "ID"]
addfields(statsCanTable, fieldsAdd, 'DOUBLE')

# Join Tables
arcpy.AddMessage("Joining Tables...")
statsCanTableView = arcpy.MakeTableView_management(statsCanTable, "statsCanTableView")
joinedTable = arcpy.AddJoin_management(statsCanTableView, 'ORIGIN', censusCentroids, 'CENSUS_TRACT')

# Calculate Origin X, Origin Y
# Origin X = [CTRPLONG] & Origin Y = [CTRPLAT]
expression_lon = '!CensusTrack_Centroid_FNL.CTRPLAT!'
expression_lat = '!CensusTrack_Centroid_FNL.CTRPLONG!'
arcpy.CalculateField_management(joinedTable, 'statsCanData.ORIGIN_X', expression_lat, 'PYTHON')
arcpy.CalculateField_management(joinedTable, 'statsCanData.ORIGIN_Y', expression_lon, 'PYTHON')

# REMOVE
arcpy.RemoveJoin_management(statsCanTableView)
arcpy.AddMessage("\t!Removed Join!")

# ADD JOIN -> Destination ID - Census Tract
joinedTable = arcpy.AddJoin_management(statsCanTableView, 'DESTINATIN', censusCentroids, 'CENSUS_TRACT')

# CACLULATE DESTINATION X & Y
arcpy.CalculateField_management(joinedTable, 'statsCanData.DESTINATION_X', expression_lat, 'PYTHON')
arcpy.CalculateField_management(joinedTable, 'statsCanData.DESTINATION_Y', expression_lon, 'PYTHON')

arcpy.RemoveJoin_management(statsCanTableView)
arcpy.AddMessage("\t!Removed Join!")

arcpy.CalculateField_management(joinedTable, 'ID', '!OBJECTID!', 'PYTHON')

# EXPORT RESULTS TO TABLE
joinedTableDir = os.path.join(workspace, 'joinTable')

if arcpy.Exists(joinedTableDir):
    arcpy.Delete_management(joinedTableDir)
    arcpy.CopyRows_management(joinedTable, joinedTableDir)
else:
    arcpy.CopyRows_management(joinedTable, joinedTableDir)


# XY TO LINE
arcpy.AddMessage("Processing XY to Line...\n")
if arcpy.Exists(os.path.join(workspace, 'XYLineTest')):
    arcpy.Delete_management(os.path.join(workspace, 'XYLineTest'))

try:
    # joinedTable_layer = arcpy.MakeTableView_management(joinedTableDir, 'joinedTable')
    joinedTable_view = arcpy.MakeTableView_management(joinedTableDir, 'joinedTableView')
    xyLine = arcpy.XYToLine_management(in_table=joinedTable_view,
                                       # in_table=joinedTableDir,
                                       out_featureclass=os.path.join(workspace, 'XYLineTest'),
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


# SUMMARIZE
def stats_analysis(feature, field, transitTypeField):
    # Parameter 3 - Summary Statistics for these fields
    # Parameter 4 - Grouped By this Field

    arcpy.AddMessage("Running Stats Analysis on {}".format(field))
    output = os.path.join(workspace, 'Summary_{}'.format(field.split(".")[1]))
    # transitTypeField = 'All_MODES'
    statField = 'joinTable.{}'.format(transitTypeField)

    if arcpy.Exists(output):
        print "Deleting output..."
        arcpy.Delete_management(output)
        print "Deleted output"

    print "Running Statistics Analysis"
    arcpy.Statistics_analysis(feature,
                              output,
                              [[statField, "SUM"], [statField, "COUNT"]],
                              field)


xyLineFC = os.path.join(workspace, 'XYLineTest')

joinedTable_layer = arcpy.MakeTableView_management(joinedTableDir, 'joinedTable')
print "Created joinedTable_layer"
xyLine_layer = arcpy.MakeFeatureLayer_management(xyLineFC, "xyLine") # Try using table view...
print "Created xyLine_layer"
xyJoinedTable = arcpy.AddJoin_management(xyLine_layer, 'OID', joinedTable_layer, 'ID')
print "Created xyJoinedTable"
# with arcpy.da.SearchCursor(xyJoinedTable, "*") as cursor:
#     for row in cursor:
#         print row
print [x.name for x in arcpy.ListFields(xyJoinedTable)]

if arcpy.Exists(os.path.join(workspace, "joinedTablePreSum")):
    arcpy.Delete_management(os.path.join(workspace, "joinedTablePreSum"))
    print "Deleted joinedTablePreSum"

# joinedTablePreSummary = arcpy.CopyRows_management(xyJoinedTable, os.path.join(workspace, "joinedTablePreSum"))
arcpy.AddMessage("127")

# arcpy.CopyRows_management(xyJoinedTable, os.path.join(workspace, "joinedTablePreSum"))
print "133"

# arcpy.AddMessage([x.name for x in arcpy.ListFields(xyJoinedTable)])

# joinedTablePreSummary = os.path.join(workspace, "joinedTablePreSum")
# stats_analysis(joinedTablePreSummary, 'joinTable.ORIGIN', 'All_MODES')
# stats_analysis(joinedTablePreSummary, 'joinTable.DESTINATIN', 'All_MODES')
stats_analysis(xyJoinedTable, 'joinTable.ORIGIN', 'All_MODES')
stats_analysis(xyJoinedTable, 'joinTable.DESTINATIN', 'All_MODES')

arcpy.AddMessage("Finished Processing.")

# with arcpy.da.SearchCursor(joinedTable, "*") as cursor:
#     for row in cursor:
#         arcpy.AddMessage(row)