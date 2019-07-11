"""
Please review outdoor_rec_poly and
assign the correct park rec feature Fac_ID to any record where Fac_ID = 0 or is null.

If no PRF point exists to represent that feature, please create a PRF and record the new Fac_ID in outdoor_rec_poly.
"""

# Add option to edit
# Add Option for log as textfile
import arcpy
import os

arcpy.AddMessage("\nSetting Variables...")
editable = arcpy.GetParameterAsText(0)
user_dir = os.path.expanduser('~')
centroidPoints = r'C:\Users\gallaga\testing\New File Geodatabase.gdb\centroids'


# VARIALBLES
workspace = r"Database Connections\Prod_GIS_Halifax.sde"
arcpy.env.workspace = workspace

recPoly = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_outdoor_rec_poly'
recPolyFields = [f.name for f in arcpy.ListFields(recPoly)]
sql_poly = "ASSETSTAT NOT LIKE 'DIS' AND REC_ID = 0 OR REC_ID IS NULL"

recPoint = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_park_recreation_feature'
recPointFields = [f.name for f in arcpy.ListFields(recPoint)]

text_result = ''
results_dict = {}

arcpy.AddMessage("\nProcessing...")

# Get Count of results
with arcpy.da.SearchCursor(recPoly, ["REC_ID", "ASSETID"], where_clause=sql_poly) as cursor:
    arcpy.AddMessage('\tPark Poly Results\n\t\t"REC_ID", "ASSETID"')
    for index, row in enumerate(cursor, 1):
        arcpy.AddMessage('\t{})\t{}'.format(index, row))
        results_dict[row] = None


arcpy.AddMessage(results_dict)

# link between polygon and point ==> RECPOLYID, poly -- ASSETID, point
# Search points where ASSETID = RECPOLYID
# Get REC ID for polygon ==> if no point, make point


def get_missing_ids():
    arcpy.AddMessage("\nSearching RecPoint Featureclass for matching IDs...")
    # We could have a recPoint with a recID to use for corresponding recPoly, otherwise will need to make one

    with arcpy.da.SearchCursor(recPoint, ["RECPOLYID", "REC_ID"]) as pointCursor:
        for key in results_dict.keys():
            poly_recID = key[0]
            poly_recpoly = key[1]
            arcpy.AddMessage("\tRec_Poly[REC_ID]: '{}'".format(poly_recpoly))

            for row in pointCursor:
                point_recPoly = row[0]
                point_recID = row[1]

                if point_recPoly is not None:
                    if point_recPoly == poly_recpoly:
                        arcpy.AddMessage("\t*Found RECPOLYID:\t{}".format(point_recPoly))
                        arcpy.AddMessage("\t\tREC_ID should match:\t{}".format(point_recID))

                        # Add match to Dictionary
                        results_dict[poly_recID] = point_recID


get_missing_ids()


def getcentroids(featureclass):
    arcpy.AddMessage("\nGetting Centroid Coordinate Values of ''...".format(featureclass))

    centroids = []

    with arcpy.da.SearchCursor(featureclass, "SHAPE@", where_clause=sql_poly) as cursor:
        for row in cursor:
            labelPoint = row[0].labelPoint
            coords = [(labelPoint.X, labelPoint.Y)]
            centroids.append(coords)

    return centroids


# with arcpy.da.InsertCursor(centroidPoints, ["SHAPE@"]) as icursor:
#     for coords in getcentroids(recPoly):
#         arcpy.AddMessage("COORDS: {}".format(coords))
#         icursor.insertRow(coords)


arcpy.AddMessage("\nRESULTS:")
matches = []
no_matches = []

for k, v in results_dict.items():

    # Values contain record matches
    if v is not None:
        matches.append("{}: {}".format(k, v))

    else:
        no_matches.append(str(k[1]))

if len(matches) > 0:
    arcpy.AddMessage("\tMatches: ", matches)
    # Add the rec_ID from rec point to rec poly?

if len(no_matches) > 0:
    arcpy.AddMessage("\t**Need to create PARK REC FEATURES for;\n\t\t{}".format('\n\t\t'.join(no_matches)))

# Can create text results
# Still need to make actual edits

