
def sheets_tocsvs():
    import os, sys
    import pandas as pd
    # Can hardcode your filename to variable below or input data from prompt provided
    # target_xlsx = r'kijiji_data.xls'
    target_xlsx = raw_input("Please type name of excel file, including extension: ")

    xl_file = pd.ExcelFile(target_xlsx)

    sheet_names = xl_file.sheet_names
    sheet_data = [xl_file.parse(sheet) for sheet in sheet_names]

    sheet_dict = dict(zip(sheet_names, sheet_data))

    # Write sheets to own .csv
    for name, data in sheet_dict.items():
        print "Writing '{}' to .csv".format(name)
        data.to_csv(name + '_' + os.path.basename(target_xlsx).split('.')[0] + '.csv', encoding='utf-8', index=False)


def merge_csvs(filename='output'):
    import os, sys
    import pandas as pd

    print("Merging csvs...")

    # Get list of .csvs in script directory
    csvs = [x for x in os.listdir(sys.path[0]) if 'csv' in x]

    # Merge csvs into one file
    with pd.ExcelWriter(filename + '.xlsx') as writer:
        for csv in csvs:
            pd.read_csv(csv, encoding='utf-8').to_excel(writer, sheet_name=csv.strip('.csv'), encoding='utf-8', index=False)

    print("\tMerged: '{}' to '{}'".format(', '.join(csvs), filename + '.xlsx'))


# merge_csvs()


def main():
    print("Running main function...")

    # if raw_input("Create csvs from sheets? (Y/N)".upper() == 'Y'):
    #     sheets_tocsvs()

    merge_csvs()

    print("Finished processing.")


main()

