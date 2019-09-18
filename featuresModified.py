import arcpy
import datetime
import os

"""
For each Feature Class
Get records modified within the last 5 days
"""
daysOld = 7
today = datetime.date.today()

user_dir = os.path.expanduser('~')
date = datetime.datetime.now().date()
results_txtfile = os.path.join(os.path.expanduser('~'), "Downloads", "{}_{}.txt".format("lastModifiedFeatures", date))

workspace = r'Database Connections\Prod_GIS_Halifax.sde'

parkFC = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_hrm_parcel_parks\SDEADM.LND_hrm_park'
recPolyFC = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_outdoor_rec_poly'
recFeatureFC = r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_park_recreation_feature'
featureClasses = [parkFC, recPolyFC, recFeatureFC]

assetReport = {parkFC: ['PARK_NAME', 'PARK_ID'],
               recPolyFC: ['ASSETID', 'REC_ID'],
               recFeatureFC: ['REC_NAME', 'ASSETID']}

arcpy.env.workspace = workspace

with open(results_txtfile, 'w') as txt_results:
    for k, v in assetReport.items():
        txt_results.write("\n\nFEATURE CLASS: {}".format(os.path.basename(k)))
        arcpy.AddMessage("\nFEATURE CLASS: {}".format(os.path.basename(k)))

        with arcpy.da.SearchCursor(k, field_names="*") as cursor:
            fields = [x.name for x in arcpy.ListFields(k)]

            for row in cursor:
                modifiedBy = row[fields.index('MODBY')]
                try:
                    daysDelta = (today - datetime.datetime.date(row[fields.index('MODDATE')])).days

                    if daysDelta <= daysOld:
                        arcpy.AddMessage("\n\t{} - {}\n\t{} - {}".format(
                            v[0], row[fields.index(v[0])], v[1], row[fields.index(v[1])]))
                        arcpy.AddMessage("\n\tLAST MODIFIED: {} days ago \n\tBY: {}".format(daysDelta, modifiedBy))

                        txt_results.write("\n\n\t{} - {}\n\t{} - {}".format(
                            v[0], row[fields.index(v[0])], v[1], row[fields.index(v[1])]))
                        txt_results.write("\n\tLAST MODIFIED: {} days ago \n\tBY: {}".format(daysDelta, modifiedBy))
                except:
                    continue

os.startfile(results_txtfile)
arcpy.AddMessage("\nFinished Processing.")
