import arcpy

fields = arcpy.GetParameterAsText(0).split(',')
fields = [x.strip() for x in fields]

featureClass = arcpy.GetParameterAsText(1)
fieldType = arcpy.GetParameterAsText(2)

# TEXT, FLOAT, SHORT, LONG, DATE

for field in fields:
    try:
        arcpy.AddField_management(in_table=featureClass, field_name=field, field_type=fieldType)
        arcpy.AddMessage("Added Field: '{}'".format(field))
    except:
        arcpy.AddMessage("**Not able to add field: '{}'".format(field))
