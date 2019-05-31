import arcpy, os
print("Processing...\n")

enterprise_gdb = r'C:\Users\gallaga\AppData\Roaming\ESRI\Desktop10.4\ArcCatalog\Prod_GIS_Halifax.sde'

# Create folder for outputs
curr_dir = os.getcwd()
working_dir = os.path.join(curr_dir, os.path.basename(__file__).strip(".py"))

# if not os.path.exists(working_dir):
#     os.makedirs(working_dir, False)
#     print "Made dir: {}".format(working_dir)
# else:
#     print "\t*{} already exists".format(working_dir)
#
# # Create database connection
# out_folder_path = working_dir
# out_name = "database_connection.sde"
# database_platform = 'ORACLE'
# instance = r'http://proxy.halifax.ca:8002'
# account_authentication = 'DATABASE_AUTH'
# user_name = "gallaga"
# user_password = "Az1muth"
# save_user_pass = 'SAVE_USERNAME'
# version_type = 'TRANSACTIONAL'
# version = 'DEFAULT'

# print "\nCreating database connection..."
# if os.path.exists(os.path.join(working_dir, out_name)):
#     os.remove(os.path.join(working_dir, out_name))
#     print "\tDeleted '{}'".format(os.path.join(working_dir, out_name))

# if arcpy.CreateDatabaseConnection_management(out_folder_path=out_folder_path,
#                                           out_name=out_name,
#                                           database_platform=database_platform,
#                                           instance=instance,
#                                           account_authentication=account_authentication,
#                                           username=user_name,
#                                           password=user_password,
#                                           save_user_pass=save_user_pass,
#                                           version_type=version_type,
#                                           version=version):
#     print "\tCreated database connection"
# else:
#     print "\t*Database connection failed"


def list_featureclasses(workspace, wild_card=None):
    arcpy.env.workspace = workspace

    print "\tVariables:\n\t\tWorkspace: {}\n\t\tWild Card: '%{}%'".format(workspace, wild_card)
    print "\n\tGetting Feature classes..."

    feature_classes = arcpy.ListFeatureClasses()

    if wild_card is not None:
        feature_classes = [f for f in feature_classes if wild_card in f]

    print feature_classes
    return feature_classes


list_featureclasses(enterprise_gdb, wild_card='ontract')

print "Finished Processing"
