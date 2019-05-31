import arcpy
import os
import csv
import datetime

# "C:\Users\gallaga\Downloads\.idea"
user_dir = os.path.expanduser('~')
downloads_dir = os.path.join(user_dir, 'Downloads')
csv_file = os.path.join(downloads_dir, 'results.csv')

# VARIALBLES
workspace = r"Database Connections\Prod_GIS_Halifax.sde"

parkPoly = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_outdoor_rec_poly'
parkPoint = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_park_recreation_feature'

# Run select statement to get all disposed polys with
parkPolyFields = [f.name for f in arcpy.ListFields(parkPoly)]
parkPointFields = [f.name for f in arcpy.ListFields(parkPoint)]

sql_disposed = "ASSETSTAT LIKE 'DIS' and REC_ID != 0"
sql_notDisposed = "ASSETSTAT NOT LIKE 'DIS' and REC_ID != 0"

polyData_notDisposed = [row for row in arcpy.da.SearchCursor(parkPoly, "*", where_clause=sql_notDisposed)]
polyData_Disposed = [row for row in arcpy.da.SearchCursor(parkPoly, "*", where_clause=sql_disposed)]
disposedRecIDS = [row[parkPolyFields.index('REC_ID')] for row in arcpy.da.SearchCursor(parkPoly, "*", where_clause=sql_disposed)]
# disposedRecIDS = [1805, 1806, 1807, 1808, 1826]

text_result = str(datetime.datetime.now()) + "\n\n"

print "Processing...\n"
arcpy.env.workspace = workspace

# HOW MANY RECORDS NEED MODIFYING
if len(disposedRecIDS) > 0:
    text_result += "Found {} Polygon Assets that require modification/inspection.\n\t".format(len(disposedRecIDS))
    text_result += "Disposed REC_IDs: {}".format([str(x) for x in disposedRecIDS])

else:
    text_result += "Found 0 Polygon Assets that need modification!"

print text_result

with open(os.path.join(downloads_dir, 'results.txt'), 'w') as txt_results:
    txt_results.write(text_result)
os.startfile(os.path.join(downloads_dir, 'results.txt'))


def write_results(data):
    with open(csv_file, 'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
    print "Wrote Results."

# with arcpy.da.Editor(r"Database Connections\Prod_GIS_Halifax.sde") as edit:
    # edit.startEditing(False, True)


def main():
    edit = arcpy.da.Editor(workspace)

    for rec in disposedRecIDS:
        print "\nDisposed RecID: ", rec
        # NEED TO FINISH THIS LOGIC - ACCOUNTS FOR POLYGONS THAT REPLACE DISPOSED POLYGONS
        # OR WHERE ONLY ONE PART OF THE ASSET (PLAYGROUND) IS DISPOSED

        # CHECK IF OTHER POLYGONS PRESENT WITH SAME REC_ID, IF THERE ARE,
        # CHANGE REC_ID TO ZERO, KEEP REC POINT

        if rec in [row[parkPolyFields.index("REC_ID")] for row in polyData_notDisposed]:
            print "*\t{} has more than one feature"

            # Update REC_ID
            # edit.startEditing(False, True)
            # edit.startOperation()
            with arcpy.da.UpdateCursor(parkPoly, "REC_ID", where_clause=sql_disposed) as cursor:
                for row in cursor:
                    if row[0] == rec:
                        print "MULTIPLE FEATURES", row
                        # row[0] = 0
                        # cursor.updateRow(row)
                        # edit.stopOperation()
                        # edit.stopEditing(True)
                        print "\tUpdated {} to 0".format(rec)
            # edit.stopEditing(True)

        # IF NO OTHER POLYGONS, CHANGE REC_ID TO 0 AND DELETE RECPOINT
        else:
            edit.startEditing(False, True)
            edit.startOperation()
            print "\nChanging REC_ID to 0..."
            with arcpy.da.UpdateCursor(parkPoly, "REC_ID", where_clause=sql_disposed) as cursor:
                for row in cursor:
                    if row[0] == rec:
                        row[0] = 0
                        cursor.updateRow(row)
                        print "\tUpdated REC_ID {} to 0".format(rec)
            edit.stopOperation()

            # DELETE POINT
            print "\nDeleting Park Rec Feature {}...".format(rec)
            # edit.startEditing(False, True)
            edit.startOperation()
            with arcpy.da.UpdateCursor(parkPoint, "REC_ID") as pointCursor:
                for row in pointCursor:
                    if row[0] == rec:
                        pointCursor.deleteRow()
                        print "\tDeleted"
            edit.stopOperation()
            edit.stopEditing(True)

    # edit.stopEditing(True)


main()

print "\nFinished Processing."

# editor https://pro.arcgis.com/en/pro-app/arcpy/data-access/editor.htm

# BUGS
# Only deletes first feature in list each run --> try putting stopOperation, stopEditing outside of loop

# Deleteing park rec feature points does not get run
# --> *for row in cursor, changed to for row in point cursor
# --> should work now, if not maybe run editing operation inside cursors


# Add report mode and delete mode