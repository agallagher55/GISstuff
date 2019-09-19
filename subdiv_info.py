import os
import pandas as pd
import re
import win32com.client


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

# EMAIL STUFF
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

root_folder = outlook.Folders.Item(1)
subFolder = root_folder.Folders['Tickets'].Folders['Tasks'].Folders['Subdivisions']

messages = subFolder.Items
messages.Sort("[ReceivedTime]", True)

message = messages.GetFirst()
rec_time = message.CreationTime
body_content = message.body
subj_line = message.subject

subNumbers = []

for i in range(100):
# while message:
    # print(message.subject, message.CreationTime)
    try:
        if 'ubdivision' in message.body:
            # print(message.subject, message.CreationTime)
            # print(message.body, "\n\n\t\t")

            sub = re.search(r"Subdivision \d+", message.body)
            sub = str(sub.group()).split('Subdivision')[1].strip()
            subNumbers.append(sub)
            print("\tFound Subdivision:\t'{}'".format(sub))

    except Exception as e:
        print("\t**", str(e))

    message = messages.GetNext()

print("SUBS: {}".format(subNumbers))

for x in subNumbers[:5]:
    findfile(x)

# findfile(13891, True)

# sub = input("What is your subdivision number? ")
# findfile(sub)
