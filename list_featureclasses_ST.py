def list_featureclasses():
    import arcpy, os
    arcpy.AddMessage("\nProcessing...\n")

    wild_card = arcpy.GetParameterAsText(0)
    workspace = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = workspace

    arcpy.AddMessage("\tVariables:\n\t\tSearch Parameter:\t'{}'\n\t\tWorkspace:\t\t'{}'".format(wild_card, workspace))
    arcpy.AddMessage("\n\n\tFeature classes...")

    feature_classes = sorted(arcpy.ListFeatureClasses(wild_card="*{}*".format(wild_card)))

    arcpy.AddMessage("\t\t{} FEATURE CLASS(ES) found:\n".format(len(feature_classes)))
    for fc in feature_classes:
        arcpy.AddMessage("\t\t\t{}".format(fc))

    ##################################################################################################################

    # List Datasets
    arcpy.AddMessage("\n\n\tDatasets...")

    datasets = sorted(arcpy.ListDatasets(wild_card="*{}*".format(wild_card)))

    arcpy.AddMessage("\t\t'{}' DATASET(S) found:\n".format(len(datasets)))
    for ds in datasets:
        arcpy.AddMessage("\t\t\t{}".format(ds))

    # Featureclasses in datasets
    arcpy.AddMessage("\n\tFeature Classes in Datasets...")
    all_datasets = arcpy.ListDatasets()

    for dataset in all_datasets:
        fcs = arcpy.ListFeatureClasses(wild_card="*{}*".format(wild_card), feature_dataset=dataset)

        if len(fcs) > 0:
            for fc in fcs:
                arcpy.AddMessage("\t\t\t{:<40}{}".format(fc, " Found in: " + dataset))

    arcpy.AddMessage("\nFinished Processing.\n")

    return feature_classes, datasets


list_featureclasses()

