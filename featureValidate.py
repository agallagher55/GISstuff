"""
With first priority being playgrounds,
please review outdoor_rec_poly and assign the correct park rec feature Fac_ID to any record where Fac_ID = 0 or is null.
If no PRF point exists to represent that feature, please create a PRF and record the new Fac_ID in outdoor_rec_poly.
"""

import arcpy

print "Processing..."
arcpy.env.workspace = r"Database Connections\Prod_GIS_Halifax.sde"

outdoor_rec_poly = r"Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_outdoor_rec_poly"

parks = r"Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_hrm_parcel_parks\SDEADM.LND_hrm_park"
parks_layer = arcpy.MakeFeatureLayer_management(parks, "parks_layer")

sql = 'PARK_ID is Null or PARK_ID = 0'
poly_layer = arcpy.MakeFeatureLayer_management(outdoor_rec_poly, "poly_layer", where_clause=sql)

print "{} records found where: '{}'".format(arcpy.GetCount_management(poly_layer[0]), sql)

# Select all rec_poly's that overlap a park
points_inPark = arcpy.SelectLayerByLocation_management("poly_layer", "INTERSECT", "parks_layer")
print arcpy.GetCount_management(points_inPark[0])


def rec_poly_FacID_0():
    fields = ["REC_ID", "ASSETSTAT", "RECPOLYID", "GENRECTYPE", "ASSETCODE", "PARK_ID"]
    playground_sql = 'GENRECTYPE like "PLAYGROUND"'

    # Select all where Fac_ID is 0 or null ==> Fac_ID is an alias for Rec_ID**
    with arcpy.da.SearchCursor(outdoor_rec_poly, fields) as cursor:
        # results = [row for row in cursor if row[0] == 0 or row[0] is None]
        # print results

        for row in cursor:
            if row[0] is None or row[0] == 0 and 'DIS' not in row[1]:
                print row


print "\nFinished Processing."
