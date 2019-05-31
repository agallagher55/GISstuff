"""
Please review outdoor_rec_poly and
assign the correct park rec feature Fac_ID to any record where Fac_ID = 0 or is null.

If no PRF point exists to represent that feature, please create a PRF and record the new Fac_ID in outdoor_rec_poly.
"""

import arcpy
import os

user_dir = os.path.expanduser('~')

# VARIALBLES
workspace = r"Database Connections\Prod_GIS_Halifax.sde"
arcpy.env.workspace = workspace

parkPoly = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_outdoor_rec_poly'
parkPolyFields = [f.name for f in arcpy.ListFields(parkPoly)]
sql_poly = "ASSETSTAT NOT LIKE 'DIS' AND REC_ID = 0 OR REC_ID IS NULL"

parkPoint = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_park_recreation_feature'
parkPointFields = [f.name for f in arcpy.ListFields(parkPoint)]

text_result = ''
results_dict = {}

print "\nProcessing..."

# Get Count of results
with arcpy.da.SearchCursor(parkPoly, ["REC_ID", "ASSETID"], where_clause=sql_poly) as cursor:
    print '\tPark Poly Results\n\t\t\t"REC_ID", "ASSETID"'
    for row in cursor:
        print '\tFound:\t{}'.format(row)
        results_dict[row] = None


print results_dict

# link between polygon and point ==> RECPOLYID, poly -- ASSETID, point
# Search points where ASSETID = RECPOLYID
# Get REC ID for polygon ==> if no point, make point


def get_missing_ids():
    print "\nSearching Point Featureclass for matching IDs..."

    with arcpy.da.SearchCursor(parkPoint, ["RECPOLYID", "REC_ID"]) as pointCursor:
        for recID in results_dict.keys():
            print "\tProcessing '{}'".format(recID)

            for recpoly in pointCursor:
                if recpoly[0] is not None:
                    if recpoly[0] == recID[1]:
                        print "\t*Found RECPOLYID:\t{}".format(recpoly)
                        print "\t\tREC_ID should match:\t{}".format(recpoly[1])
                        results_dict[recID] = recpoly


get_missing_ids()

print "\nRESULTS:"
matches = []
no_matches = []

for k, v in results_dict.items():
    if v is not None:
        matches.append("{}: {}".format(k, v))

    else:
        no_matches.append("{}: {}".format(k, v))

if len(matches) > 0:
    print "\tMatches: ", matches
    # Add the rec_ID from rec point to rec poly?

if len(no_matches) > 0:
    print "\tNeed to create PARK REC FEATURES for;\n\t\t", '\n\t\t'.join(no_matches)
