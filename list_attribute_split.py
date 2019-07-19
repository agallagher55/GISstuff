import arcpy
import os

# PRIMARY VARIABLES

featureClass = arcpy.GetParameterAsText(0)
listField = arcpy.GetParameterAsText(1)
delimiter = arcpy.GetParameterAsText(2)

# featureClass = r'C:\Users\gallaga\testing\New File Geodatabase.gdb\busStopsTesting'
# listField = "Routes"
# delimiter = ","

arcpy.AddMessage("Processing...")

# Get Field Data
listFieldData = [row for row in arcpy.da.SearchCursor(featureClass, listField)]

# Get length of longest list
maxFields = 0

for row in listFieldData:
    routes = row[0]
    listRoutes = str(routes).split(delimiter)
    numRoutes = len(listRoutes)

    if numRoutes > maxFields:
        maxFields = numRoutes

arcpy.AddMessage("\nFOUND {} VALUES IN '{}' FIELD".format(maxFields, listField))


# Create x number of new fields
def addfields(featureclass, fields, fieldtype):
    arcpy.env = os.path.dirname(featureclass)

    arcpy.AddMessage("\nAdding Fields...")
    for field in fields:
        if field not in [x.name for x in arcpy.ListFields(featureclass)]:
            try:
                arcpy.AddField_management(in_table=featureclass, field_name=field, field_type=fieldtype)
                arcpy.AddMessage("\tAdded Field: '{}'".format(field))
            except Exception as e:
                arcpy.AddMessage(e)
                arcpy.AddMessage("**Not able to add field: '{}'".format(field))
        else:
            arcpy.AddMessage("\t{} already in {}".format(field, os.path.basename(featureclass)))


fieldsToAdd = ["{}_{}".format(listField, i + 1) for i in range(0, maxFields)]
arcpy.AddMessage("\nFields to Add: {}".format(fieldsToAdd))

addfields(featureClass, fieldsToAdd, "TEXT")

# For every item in list, populate one of the added fields
fieldsToUpdate = fieldsToAdd.insert(0, listField)
arcpy.AddMessage(fieldsToAdd)

arcpy.AddMessage("Updating {}...".format(os.path.basename(featureClass)))
with arcpy.da.UpdateCursor(featureClass, fieldsToAdd) as cursor:
    for row in cursor:
        routes = row[0]
        listRoutes = str(routes).split(delimiter)
        numRoutes = len(listRoutes)

        arcpy.AddMessage("Attributes: {}".format(listRoutes))

        for i in range(0, numRoutes):
            row[i + 1] = listRoutes[i]

        cursor.updateRow(row)


arcpy.AddMessage("Finished Processing")
