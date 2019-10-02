def merge_csvs(filextension, filename='output'):
    import os, sys
    import pandas as pd

    print("Merging csvs...")

    # Get list of .csvs in script directory
    files = [x for x in os.listdir(sys.path[0]) if str(filextension) in x]


    # Merge csvs into one file
    with pd.ExcelWriter(filename + '.xlsx') as writer:
        for file in files:

            if filextension in 'xlsx':
                try:
                    pd.read_excel(file, encoding='utf-8').to_excel(writer, sheet_name=file.strip(filextension), encoding='utf-8', index=False)
                except:
                    print("Unable to write: {}".format(file))

            if filextension in 'csv':
                try:
                    pd.read_csv(file, encoding='utf-8').to_excel(writer, sheet_name=excel.strip(filextension), encoding='utf-8', index=False)
                except:
                    print("Unable to write: {}".format(file))

    print("\tMerged: '{}' to '{}'".format(', '.join(files), filename + '.xlsx'))


def main():
    print("Running main function...")

    # if raw_input("Create csvs from sheets? (Y/N)".upper() == 'Y'):
    #     sheets_tocsvs()

    merge_csvs('xls')
    print("Finished processing.")


main()
