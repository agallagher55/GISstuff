# AUTHOR:   Alex Gallagher
# DATE:     February 14, 2019
# NOTES:    Takes one column of mis-typed data, cross-references mis-typed data with a column of correctly typed data &
#           finds closest match

# INPUTS:   1) Name of bad csv file 2) Name of good csv file 3) Names of columns for each
# OUTPUTS:  1) results csv


import csv, difflib, os, re
from fuzzywuzzy import fuzz
# python-Levenshtein

# minscore = 65
# VARIABLES
csv_raw = 'classifications_balldiamonds_sportsfields.csv'
column_name_raw = 'Facility Name'

csv_clean = 'arcmap_ballfields_sportfields.csv'
column_name_clean = 'REC_NAME'

results_csv = csv_raw.replace(".csv", "_matches.csv")
matches_dict = {}


def extract_colcsv(file, col_name):
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        header = reader.next()

        facility_index = header.index(col_name)
        facilities = [row[facility_index].upper() for row in reader]
        return facilities


data_clean = extract_colcsv(csv_clean, column_name_clean)
data_raw = extract_colcsv(csv_raw, column_name_raw)


# Clean Raw Data
# def clean_data():
data_raw_cleaned = [raw.replace(
    ' JH', ' JUNIOR HIGH SCHOOL').replace(
    ' HS', ' HIGH SCHOOL').replace(
    ' DH', ' DISTRICT HIGH ').replace(
    'MUSQ', 'MUSQUODOBOIT').replace(
    ' JR ', ' JUNIOR ').replace(
    'LK', 'LAKE PARK').replace(
    'REC CTR', 'RECREATION CENTRE').replace(
    'PK', 'PARK').replace(
    'HBR', 'HARBOUR').replace(
    ' EC ', 'EDUCATION CENTRE').replace(
    ' MS', ' MIDDLE SCHOOL'.replace(
        'CTR', 'CENTRE').replace(
        'RD', 'ROAD').replace(
        'NORTH COMMON', 'HALIFAX NORTH COMMON')) for raw in data_raw]

data_raw_cleaned = [word.strip(')').strip('(').strip("'").strip(".") for word in data_raw_cleaned]
# regex
data_raw_cleaned = [re.sub(r'\sE[^a-zA-Z]| E$', ' ELEMENTARY SCHOOL', string) for string in data_raw_cleaned]
data_raw_cleaned = [re.sub(r'(\d{1,2})',  r'#\1 ', string) for string in data_raw_cleaned]

master_dict = dict(zip(data_raw, data_raw_cleaned))


def difflib_matches(dirty_data, clean_data, number_ofmatches=1, min_score=65):
    match_dict = {}
    for word in dirty_data:
        if difflib.get_close_matches(word, clean_data, number_ofmatches, (min_score/100.0)):
            match = difflib.get_close_matches(word, clean_data, number_ofmatches)[0]
            match_dict[word] = [match, 'difflib', min_score]

    return match_dict


def fuzzywuzzy_ratio(dirty_data, clean_data, min_score=65):
    match_dict = {}
    cleanest_match = 0

    for raw in dirty_data:

        for clean in clean_data:
            match_ratio = fuzz.ratio(raw, clean)

            if match_ratio > cleanest_match and match_ratio > min_score:
                cleanest_match = match_ratio
                match_dict[raw] = [clean, 'fuzzwuzzy_ratio', min_score]

    return match_dict


def fuzzywuzzy_partial(dirty_data, clean_data, min_score=65):
    match_dict = {}
    cleanest_match = 0

    for raw in dirty_data:

        for clean in clean_data:
            match_ratio = fuzz.partial_ratio(raw, clean)

            if match_ratio > cleanest_match and match_ratio > min_score:
                cleanest_match = match_ratio
                match_dict[raw] =[clean, 'fuzzwuzzy_partial', min_score]

    return match_dict


def fuzzywuzzy_tokensort(dirty_data, clean_data, min_score=65):
    match_dict = {}
    cleanest_match = 0

    for raw in dirty_data:

        for clean in clean_data:
            match_ratio = fuzz.token_sort_ratio(raw, clean)

            if match_ratio > cleanest_match and match_ratio > min_score:
                cleanest_match = match_ratio
                match_dict[raw] = [clean, 'fuzzwuzzy_tokensort', min_score]

    return match_dict


def fuzzywuzzy_tokenset(dirty_data, clean_data, min_score=65):
    match_dict = {}
    cleanest_match = 0

    for raw in dirty_data:

        for clean in clean_data:
            match_ratio = fuzz.token_set_ratio(raw, clean)

            if match_ratio > cleanest_match and match_ratio > min_score:
                cleanest_match = match_ratio
                match_dict[raw] = [clean, 'fuzzwuzzy_tokenset', min_score]

    return match_dict


tokenset_fuzz_dict = fuzzywuzzy_tokenset(data_raw_cleaned, data_clean)
difflib_dict = difflib_matches(data_raw_cleaned, data_clean)
ratio_fuzz_dict = fuzzywuzzy_ratio(data_raw_cleaned, data_clean)
partial_fuzz_dict = fuzzywuzzy_partial(data_raw_cleaned, data_clean)
tokensort_fuzz_dict = fuzzywuzzy_tokensort(data_raw_cleaned, data_clean)

dictionaries = [tokensort_fuzz_dict, ratio_fuzz_dict, tokenset_fuzz_dict, difflib_dict, partial_fuzz_dict]

for dictionary in dictionaries:
    for k, v in dictionary.items():
        if k not in matches_dict.keys():
            matches_dict[k] = v

for k, v in master_dict.items():  # k is raw, v is raw_cleaned -->
    master_dict[k] = v, matches_dict.get(v)


print
for k, v in master_dict.items():
    if v[1] is not None:
        print "{} - {}".format(k.ljust(30), v[1][0])
    else:
        print "{} - {}".format(k.ljust(30), 'None')


# Create results csv
with open(csv_raw, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    header = reader.next()

    facility_index = header.index(column_name_raw)
    raw_data = [r for r in reader]

    header = [h.replace(' ', '_') for h in header]
    header.extend(['', 'MATCH_FOUND'])

    with open(results_csv, 'wb') as csvwrite:
        filewriter = csv.writer(csvwrite)
        filewriter.writerow(header)

        for row in raw_data:
            for key, value in master_dict.items():
                if row[facility_index].upper() == key:
                    if value[1] is not None:
                        filewriter.writerow(row + ["", value[1][0]])
                    else:
                        filewriter.writerow(row + ["", ""])

    # os.startfile(results_csv)