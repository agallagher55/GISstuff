def find_phonenum():
    import re

    phoneregex = re.compile(r'''(
        (\d{3}|\(\d{3}\))?                # area code
        (\s|-|\.)?                        # separator
        (\d{3})                           # first 3 digits
        (\s|-|\.)                         # separator
        (\d{4})                           # last 4 digits
        (\s*(ext|x|ext.)\s*(\d{2,5}))?    # extension
        )''', re.VERBOSE)

    phonenumber = raw_input("Enter your phone number: ")
    mo = phoneregex.search(phonenumber)

    matches = []
    for groups in phoneregex.findall(phonenumber):
        phoneNum = '-'.join([groups[1], groups[3], groups[5]])
        if groups[8] != '':
            phoneNum += ' x' + groups[8]
        matches.append(phoneNum)

    if len(matches) > 0:
        match = matches[0].replace('(', '').replace(')', '')
        print "\tFound phone number: ", match

        return match

    else:
        print "*\tNo valid phone number found"


find_phonenum()
