import arcpy
arcpy.AddMessage("Processing...")

arcpy.env.workspace = arcpy.GetParameterAsText(0)

featureclasses = arcpy.ListFeatureClasses()
fieldsDelete = ["ADDBY", "MODBY", "ADDDATE", "MODDATE"]

for feature in featureclasses:
    fields = [field.name for field in arcpy.ListFields(feature)]

    if any(field in fields for field in fieldsDelete):
        arcpy.AddMessage("\tDeleting {} from {}...".format(fieldsDelete, feature))
        arcpy.DeleteField_management(feature, fieldsDelete)
    else:
        arcpy.AddMessage("\tNo fields to delete from {}".format(feature))

arcpy.AddMessage("\nFinished Processing.")
