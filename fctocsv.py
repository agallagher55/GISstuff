import arcpy
import csv
import os

def featuretocsv(featureclass, directory):

    outputCSVName = os.path.basename(featureclass) + ".csv"
    outputCSVFile = os.path.join(directory, outputCSVName)

    fields = [x.name for x in arcpy.ListFields(featureclass)]
    data = [row for row in arcpy.da.SearchCursor(featureclass, "*")]

    with open(outputCSVFile, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        for row in data:
            writer.writerow(row)

    return outputCSVFile

featureClass = arcpy.GetParameterAsText(0)
outputCSVDir = arcpy.GetParameterAsText(1)
openOnExit = arcpy.GetParameterAsText(2)

if openOnExit == 'true':
    os.startfile(featuretocsv(featureClass, outputCSVDir))
else:
    featuretocsv(featureClass, outputCSVDir)