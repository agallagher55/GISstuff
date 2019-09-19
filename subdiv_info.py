import os
import pandas as pd

"""
September 19, 2019
- Search folders method
- Read .xlsx
- Read comments field
"""

def getcomments(filepath):
    # 1 Read COMMENTS from .xlsx

    dirFiles = os.listdir(filepath)

    try:
        excelFile = os.path.join(filepath, [x for x in dirFiles if '.xls' in x][0])
        # print(excelFile)

        df = pd.read_excel(excelFile, skiprows=3)   # Row start - Row 4
        df.set_index('PID', inplace=True)

        comments = df['COMMENTS'].tolist()
        # print(comments)
        commentsNoNull = [x for x in comments if str(x) != 'nan' or str(x) != " "]

        if len(commentsNoNull) > 0:
            print("\nSUBDIVISION: ", os.path.basename(filepath))
            print(excelFile)
            # print(commentsNoNull)
            dfComments = df[['COMMENTS']]
            print(dfComments)
            return commentsNoNull

        # else:
        #     print("**NO COMMENTS FOUND")

    except Exception as e:
        print("EXCEPTION: {}".format(str(e)))

"""
Search folders with subdivision number
Test folders: 22400, 22350, 22220
"""

# WOULD CHANGE THIS TO GET INPUT FROM USER (AS A STRING)
mainDir = r'H:\Civic Addressing\Shared Work\LOT CREATION DATA'
subs = [22400, 22350, 22220, 15759, 22312]
subs = [str(x) for x in subs]
subdirs = ['DBUPDATE COMPLETED TO DECEMBER 31 2019', 'REGISTERED']


def findfile(subdivision, all=False):
    count = 0
    for root, dirs, files in os.walk(mainDir, topdown=True):
        if subdivision is not None:
            # if os.path.basename(root) in subs:
            if os.path.basename(root) == str(subdivision):
                # print("\nROOT: {}".format(root), "DIRS: {}".format(dirs), "FILES: {}".format(files),sep='\n-->')
                getcomments(root)
                count += 1

        # Get all files with comments
        if all is True:
            if os.path.basename(root)[0].isdigit():
                print(root)
                getcomments(root)
                count += 1

    print("\nFOUND {} RESULTS".format(count))


# findfile(13891, True)

sub = input("What is your subdivision number? ")
findfile(sub)
