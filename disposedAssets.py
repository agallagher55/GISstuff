"""
June 4, 2019
Data Quality Check
If rec_poly feature asset status is set to disposed,
make sure Rec_ID/Fac_Id is set 0 and  rec_point is deleted if no more polygons for feature are present
"""

import arcpy
import os
import datetime

# Boolean to Trigger Edit Mode
print "Would you like to make edits? (Y/N)"

editable = False
if raw_input().upper() == "Y":
    editable = True

# ========== VARIABLES ==========
arcpy.AddMessage("Setting Variables...\n")
user_dir = os.path.expanduser('~')
downloads_dir = os.path.join(user_dir, 'Downloads')
csv_file = os.path.join(downloads_dir, 'results.csv')
text_result = str(datetime.datetime.now()) + "\n\n"

# Primary Variables
workspace = r"Database Connections\Prod_GIS_Halifax.sde"
parkPoly = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_outdoor_rec_poly'
parkPoint = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_park_recreation_feature'

# Derived Variables
parkPolyFields = [f.name for f in arcpy.ListFields(parkPoly)]
parkPointFields = [f.name for f in arcpy.ListFields(parkPoint)]

sql_disposed = "ASSETSTAT LIKE 'DIS' and REC_ID != 0"
sql_notDisposed = "ASSETSTAT NOT LIKE 'DIS' and REC_ID != 0"

polyData_notDisposed = [row for row in arcpy.da.SearchCursor(parkPoly, "*", where_clause=sql_notDisposed)]
polyData_Disposed = [row for row in arcpy.da.SearchCursor(parkPoly, "*", where_clause=sql_disposed)]

disposedRecIDS = [row[parkPolyFields.index('REC_ID')] for row in arcpy.da.SearchCursor(parkPoly, "*", where_clause=sql_disposed)]
# disposedRecIDS = [1805, 1806, 1807, 1808, 1826]

# ========== PROCESSING ==========

arcpy.AddMessage("Processing...\n")
arcpy.env.workspace = workspace

# How Many Records Need Modifying? - Result of count of sql query result
if len(disposedRecIDS) > 0:
    arcpy.AddMessage("Found {} Polygon Assets that require modification/inspection.\n\t".format(len(disposedRecIDS)))
    arcpy.AddMessage("Disposed REC_IDs: {}".format([str(x) for x in disposedRecIDS]))
    
    text_result += "Disposed REC_IDs: {}".format([str(x) for x in disposedRecIDS])
    text_result += "Found {} Polygon Assets that require modification/inspection.\n\t".format(len(disposedRecIDS))
else:
    arcpy.AddMessage("Found 0 Polygon Assets that need modification!")
    text_result += "Found 0 Polygon Assets that need modification!"

# with arcpy.da.Editor(r"Database Connections\Prod_GIS_Halifax.sde") as edit:
    # edit.startEditing(False, True)


def main(results_string):
    edit = arcpy.da.Editor(workspace)

    for rec in disposedRecIDS:
        arcpy.AddMessage(("\nDisposed RecID: ", rec))
        results_string += ("\nDisposed RecID: ", rec)
        
        # NEED TO FINISH THIS LOGIC - ACCOUNTS FOR POLYGONS THAT REPLACE DISPOSED POLYGONS
        # OR WHERE ONLY ONE PART OF THE ASSET (PLAYGROUND) IS DISPOSED

        # CHECK IF OTHER POLYGONS PRESENT WITH SAME REC_ID, IF THERE ARE,
        # CHANGE REC_ID TO ZERO, KEEP REC POINT

        if rec in [row[parkPolyFields.index("REC_ID")] for row in polyData_notDisposed]:
            arcpy.AddMessage("*\t{} has more than one feature")
            results_string += "*\t{} has more than one feature"

            # Update REC_ID
            # edit.startEditing(False, True)
            # edit.startOperation()
            with arcpy.da.UpdateCursor(parkPoly, "REC_ID", where_clause=sql_disposed) as cursor:
                for row in cursor:
                    if row[0] == rec:
                        arcpy.AddMessage(("MULTIPLE FEATURES", row))
                        results_string += "MULTIPLE FEATURES", row
                        # row[0] = 0
                        # cursor.updateRow(row)
                        # edit.stopOperation()
                        # edit.stopEditing(True)
                        arcpy.AddMessage("\tUpdated {} to 0".format(rec))
                        results_string += "\tUpdated {} to 0".format(rec)
            # edit.stopEditing(True)

        # IF NO OTHER POLYGONS, CHANGE REC_ID TO 0 AND DELETE RECPOINT
        else:
            if editable is True:
                edit.startEditing(False, True)
                edit.startOperation()
                arcpy.AddMessage("\nChanging REC_ID to 0...")
                results_string += "\nChanging REC_ID to 0..."

                with arcpy.da.UpdateCursor(parkPoly, "REC_ID", where_clause=sql_disposed) as cursor:
                    for row in cursor:
                        if row[0] == rec:
                            row[0] = 0
                            cursor.updateRow(row)
                            arcpy.AddMessage(("\tUpdated REC_ID {} to 0".format(rec)))
                            results_string += "\tUpdated REC_ID {} to 0".format(rec)
                edit.stopOperation()

                # DELETE POINT
                arcpy.AddMessage("\nDeleting Park Rec Feature {}...".format(rec))
                results_string += "\nDeleting Park Rec Feature {}...".format(rec)
                # edit.startEditing(False, True)
                edit.startOperation()
                with arcpy.da.UpdateCursor(parkPoint, "REC_ID") as pointCursor:
                    for row in pointCursor:
                        if row[0] == rec:
                            pointCursor.deleteRow()
                            arcpy.AddMessage("\tDeleted")
                            results_string += "\tDeleted"
                edit.stopOperation()
                edit.stopEditing(True)
            else:
                arcpy.AddMessage("\nChanging REC_ID to 0...")
                results_string += "\nChanging REC_ID to 0..."
                with arcpy.da.SearchCursor(parkPoly, "REC_ID", where_clause=sql_disposed) as cursor:
                    for row in cursor:
                        if row[0] == rec:
                            row[0] = 0
                            cursor.updateRow(row)
                            arcpy.AddMessage("\tUpdated REC_ID {} to 0".format(rec))
                            results_string += "\tUpdated REC_ID {} to 0".format(rec)

                # DELETE POINT
                arcpy.AddMessage("\nDeleting Park Rec Feature {}...".format(rec))
                results_string += "\nDeleting Park Rec Feature {}...".format(rec)
                with arcpy.da.SearchCursor(parkPoint, "REC_ID") as pointCursor:
                    for row in pointCursor:
                        if row[0] == rec:
                            pointCursor.deleteRow()
                            arcpy.AddMessage("\tDeleted")
                            results_string += "\tDeleted"

    # edit.stopEditing(True)


main(text_result)

arcpy.AddMessage("\nFinished Processing.")
text_result += "\nFinished Processing."

with open(os.path.join(downloads_dir, 'results.txt'), 'w') as txt_results:
    txt_results.write(text_result)
os.startfile(os.path.join(downloads_dir, 'results.txt'))

# editor https://pro.arcgis.com/en/pro-app/arcpy/data-access/editor.htm

# BUGS
