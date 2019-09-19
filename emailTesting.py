# https://www.reddit.com/r/learnpython/comments/5v799v/using_python_for_outlook_messages/
import re
import win32com.client
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

root_folder = outlook.Folders.Item(1)

for folder in root_folder.Folders:
    print (folder.Name)
subFolder = root_folder.Folders['Tickets'].Folders['Tasks'].Folders['Subdivisions']

def getemailindex():
    for i in range(50):
        try:
            box = outlook.GetDefaultFolder(i)
            name = box.Name
            print(i, name)
        except:
            pass

inbox = outlook.GetDefaultFolder(6)

messages = subFolder.Items
# messages = inbox.Items
messages.Sort("[ReceivedTime]", True)

message = messages.GetFirst()
rec_time = message.CreationTime
body_content = message.body
subj_line = message.subject

subNumbers = []

# for i in range(100):
while message:
    # print(message.subject, message.CreationTime)
    try:
        if 'ubdivision' in message.body:
            print(message.subject, message.CreationTime)
            # print(message.body, "\n\n\t\t")

            sub = re.search(r"Subdivision \d+", message.body)
            sub = str(sub.group()).split('Subdivision')[1].strip()
            subNumbers.append(sub)
            print("\tSubdivision:\t'{}'".format(sub))

    except Exception as e:
        print("\t**", str(e))

    message = messages.GetNext()

print("SUBS: {}".format(subNumbers))


# body_content = message.body
# for message in messages:
#     print(body_content)
#     message.getNext