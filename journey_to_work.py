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
joinedTable = arcpy.AddJoin_management(statsCanTableView, 'ORIGIN', censusCentroids,'CENSUS_TRACT')

# Calculate Origin X, Origin Y
# Origin X = [CTRPLONG] & Origin Y = [CTRPLAT]
expression_lon = '!CensusTrack_Centroid_FNL.CTRPLAT!'
expression_lat = '!CensusTrack_Centroid_FNL.CTRPLONG!'
arcpy.CalculateField_management(joinedTable, 'statsCanData.ORIGIN_X', expression_lat, 'PYTHON')
arcpy.CalculateField_management(joinedTable, 'statsCanData.ORIGIN_Y', expression_lon, 'PYTHON')

# REMOVE
arcpy.RemoveJoin_management(statsCanTableView)
arcpy.AddMessage("!Removed Join!")

# ADD JOIN -> Destination ID - Census Tract
joinedTable = arcpy.AddJoin_management(statsCanTableView, 'DESTINATIN', censusCentroids,'CENSUS_TRACT')

# CACLULATE DESTINATION X & Y
arcpy.CalculateField_management(joinedTable, 'statsCanData.DESTINATION_X', expression_lat, 'PYTHON')
arcpy.CalculateField_management(joinedTable, 'statsCanData.DESTINATION_Y', expression_lon, 'PYTHON')

arcpy.RemoveJoin_management(statsCanTableView)
arcpy.AddMessage("!Removed Join!")

arcpy.AddMessage([x.name for x in arcpy.ListFields(joinedTable)])
arcpy.CalculateField_management(joinedTable, 'ID', '!OBJECTID!', 'PYTHON')


# EXPORT RESULTS TO TABLE
joinedTableDir =  os.path.join(workspace, 'joinTable')
if arcpy.Exists(joinedTableDir):
    arcpy.Delete_management(joinedTableDir)
    arcpy.CopyRows_management(joinedTable, joinedTableDir)
else:
    arcpy.CopyRows_management(joinedTable, joinedTableDir)


arcpy.AddMessage([x.name for x in arcpy.ListFields(joinedTableDir)])

# XY TO LINE
arcpy.AddMessage("Processing XY to Line...\n")
if arcpy.Exists(os.path.join(workspace, 'XYLine')):
    arcpy.Delete_management(os.path.join(workspace, 'XYLine'))

try:
    xyLine = arcpy.XYToLine_management(in_table=joinedTableDir,
                                       out_featureclass=os.path.join(workspace, 'XYLine'),
                                       startx_field='ORIGIN_X',
                                       starty_field='ORIGIN_Y',
                                       endx_field='DESTINATION_X',
                                       endy_field='DESTINATION_Y',
                                       id_field='ID',
                                       spatial_reference=censusCentroids
                                       )
except Exception as e:
    arcpy.AddMessage("\t{}".format(e))


# SUMMARIZE
def stats_analysis(feature, field):
    arcpy.AddMessage("Running Stats Analysis on {}".format(field))
    output = os.path.join(workspace, 'Summary_{}'.format(field.split(".")[1]))
    if arcpy.Exists(output):
        arcpy.Delete_management(output)
    else:
        arcpy.Statistics_analysis(feature,
                                  output,
                                   # [['COUNT', 'SUM']],
                                  # [[field, 'SUM']],
                                  [[field, "SUM"], [field, "COUNT"]],
                                  field)

xyLine = os.path.join(workspace, 'XYLine')

xyLine_layer = arcpy.MakeFeatureLayer_management(xyLine, "xyLine")
joinedTable_layer = arcpy.MakeTableView_management(joinedTableDir, 'joinedTable')

xyJoinedTable = arcpy.AddJoin_management(xyLine_layer, 'OID', joinedTable_layer,'ID')



arcpy.AddMessage([x.name for x in arcpy.ListFields(xyJoinedTable)])

stats_analysis(xyJoinedTable, 'joinTable.ORIGIN')
stats_analysis(xyJoinedTable, 'joinTable.DESTINATIN')

arcpy.AddMessage("Finished Processing.")

# with arcpy.da.SearchCursor(joinedTable, "*") as cursor:
#     for row in cursor:
#         arcpy.AddMessage(row)