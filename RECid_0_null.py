"""
Please review outdoor_rec_poly and
assign the correct park rec feature Fac_ID to any record where Fac_ID = 0 or is null.

If no PRF point exists to represent that feature, please create a PRF and record the new Fac_ID in outdoor_rec_poly.
"""

# Add option to edit
# Add Option for log as textfile
import arcpy
import os
import sys
import datetime

arcpy.AddMessage("\nSetting Variables...")
editable = arcpy.GetParameterAsText(0)
user_dir = os.path.expanduser('~')
date = datetime.datetime.now().date()
results_txtfile = os.path.join(os.path.expanduser('~'), "Downloads", "{}_{}.txt".format("recNull0", date))

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
    arcpy.AddMessage('\tRECPOLYS with {}\n\t\t"REC_ID", "ASSETID"'.format(sql_poly))
    for index, row in enumerate(cursor, 1):
        arcpy.AddMessage('\t{})\t{}'.format(index, row))
        results_dict[row] = None

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

            # Search recPoint for matching RPLY IDS --> Get Rec ID
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

arcpy.AddMessage("\nRESULTS:")
matches = []
no_matches = []

for k, v in results_dict.items():

    # Values contain record matches
    if v is not None:
        matches.append("{}: {}".format(k, v))

    else:
        no_matches.append(str(k[1]))

try:
    no_matches.remove('RPLY2064')
    no_matches.remove('RPLY2067')
except:
    pass

# Can create text results
with open(results_txtfile, 'w') as txt_results:

    if len(matches) > 0:
        arcpy.AddMessage("Matches: ", matches)
        txt_results.write("Matches: ", matches)
        # Add the rec_ID from rec point to rec poly?

    if len(no_matches) > 0 and ('RPLY2064' or 'RPLY2067' not in no_matches):
        arcpy.AddMessage("**Need to create PARK REC FEATURES for;\n\t\t{}".format('\n\t\t'.join(no_matches)))
        txt_results.write("**Need to create PARK REC FEATURES for;\n\t\t{}".format('\n\t\t'.join(no_matches)))

if os.stat(results_txtfile).st_size > 0:    # Check if size is > 0
    os.startfile(results_txtfile)

# Still need to make actual edits
