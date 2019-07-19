import arcpy
import os

# VARIABLES
targetFeatureClass = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.AST_barrier'
excelUpdates = r"T:\work\giss\monthly\201907july\otoolel\New Assets\HRMFacilitiesBarriers_updates.xlsx"
workspace = r'C:\Users\gallaga\testing\New File Geodatabase.gdb'

# DERIVED VARIABLES
excelTable = os.path.join(workspace, os.path.basename(excelUpdates).strip(".xlsx"))

arcpy.env.overwriteOutput = True
arcpy.env = workspace

arcpy.AddMessage("Processing...")

# TABLE TO EXCEL
arcpy.AddMessage("Excel to table...")
updatesTable = arcpy.ExcelToTable_conversion(excelUpdates, excelTable)

arcpy.AddMessage("Getting AssetIDS...")
updatesAssetIDS = [row[0] for row in arcpy.da.SearchCursor(updatesTable, "ASSETID")]
arcpy.AddMessage(updatesAssetIDS)

# SEARCH CURSOR - SDE FEATURE CLASS
fields = ["ASSETID", "LOCGEN", "ROLLUPID"]
whereClause = 'ASSETID in {}'.format(tuple(updatesAssetIDS))
count = 0

edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

with arcpy.da.UpdateCursor(targetFeatureClass, fields, where_clause=whereClause) as uCursor:
    with arcpy.da.SearchCursor(updatesTable, fields) as sCursor:
        for uRow in uCursor:
            count += 1

            locgen = uRow[1]
            rollup = uRow[2]

            arcpy.AddMessage(uRow)
            arcpy.AddMessage(sCursor[count])


# FIELDS ==> LOCGEN, ROLLUPID, ASSETID

arcpy.AddMessage("Finished Processing.")
