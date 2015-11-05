__author__ = 'lab'

from os import walk
import json
import csv

def same_direction(sub_sheets):
    same_direction_sub_sheets = []
    for sub_sheet in sub_sheets:
        direction = -1 if sub_sheet[0] < 0 else 1
        if ((sub_sheet[1]*direction > 0) and (sub_sheet[2]*direction > 0)):
            same_direction_sub_sheets.append(sub_sheet)
    return same_direction_sub_sheets

def match_pattern(sub_sheet):
    if sub_sheet == [2,1,3]:
        return "P-loop"
    elif sub_sheet == [3,2,1]:
        return "Rossmann"
    else:
        return ""

def matching_sub_sheets(sub_sheets, sheet):
    matching_subsheets = []
    for sub_sheet in sub_sheets:
        direction = -1 if sub_sheet[0] < 0 else 1
        is_reversed = False
        corrected_sub_sheet = map(lambda x: x*direction, sub_sheet)
        sorted_sub_sheet = sorted(corrected_sub_sheet)
        gap_value = (sorted_sub_sheet[0] - 1) if (sorted_sub_sheet[0]>1) else 0
        corrected_sub_sheet = map(lambda x: x-gap_value, sub_sheet)
        matched_pattern = match_pattern(corrected_sub_sheet)
        if matched_pattern:
            corrected_sheet = map(lambda x: x*direction - gap_value, sheet)
            matching_subsheets.append({'pattern': matched_pattern, 'direction': direction, 'reversed': is_reversed, 'subsheet': sub_sheet, 'corrected_subsheet': corrected_sub_sheet, 'corrected_sheet': corrected_sheet, 'total_strands': len(sheet), 'sheet': sheet})
        else:
            is_reversed = True
            corrected_sub_sheet.reverse()
            matched_pattern = match_pattern(corrected_sub_sheet)
            if matched_pattern:
                corrected_sheet = map(lambda x: x*direction - gap_value, sheet)
                corrected_sheet.reverse()
                matching_subsheets.append({'pattern': matched_pattern, 'direction': direction, 'reversed': is_reversed, 'subsheet': sub_sheet, 'corrected_subsheet': corrected_sub_sheet, 'corrected_sheet': corrected_sheet,'total_strands': len(sheet), 'sheet': sheet})
    return matching_subsheets

def fill_reversed(sub_sheet):
    return

def fill(sub_sheet_dic):
    fill_pattern_length(sub_sheet_dic)
    fill_strands_number_before_pattern(sub_sheet_dic)
    return

def fill_pattern_length(sub_sheet_dic):
    sheet = sub_sheet_dic['corrected_sheet']
    start_index = sheet.index(sub_sheet_dic['corrected_subsheet'][2]) + 1
    length = min(3, len(sheet) - start_index)
    pattern_length = 3
    pattern_counter = 4
    for i in range(start_index, start_index+length):
        if sheet[i] * sub_sheet_dic['direction'] == pattern_counter:
            pattern_length+=1
            pattern_counter+=1
        else:
            break
    sub_sheet_dic['pattern_length'] = pattern_length
    return

def fill_strands_number_before_pattern(sub_sheet_dic):
    sheet = sub_sheet_dic['corrected_sheet']
    start_index = sheet.index(sub_sheet_dic['corrected_subsheet'][0])
    sub_sheet_dic['strands_before'] = start_index
    return

files = []
patterns_arr = []
for (dirpath, dirnames, filenames) in walk('/home/lab/Documents/rossman/'):
    files.extend(filenames)
    break

for filename in files:
    with open(dirpath+filename, 'r') as file:
        sheets_arr = json.load(file)
        for sheet in sheets_arr:
            if len(sheet) < 3:
                continue
            sub_sheets = zip(*[iter(sheet)]*3) + zip(*[iter(sheet[1:])]*3) + zip(*[iter(sheet[2:])]*3)
            sub_sheets = same_direction(sub_sheets)
            if len(sub_sheets) == 0:
                continue
            sub_sheets = matching_sub_sheets(sub_sheets, sheet)
            if len(sub_sheets) == 0:
                continue
            for sub_sheet in sub_sheets:
                    fill(sub_sheet)
                    sub_sheet['domain_id'] = filename[0:9]
                    sub_sheet['whole_protein'] = sheets_arr
            top_option = sub_sheets[0]
            for sub_sheet in sub_sheets:
                if sub_sheet['pattern_length'] > top_option['pattern_length']:
                    top_option = sub_sheet
            patterns_arr.append(sub_sheet)

with open('/home/lab/Documents/rossman_csv.txt', 'w') as csvfile:
    fieldnames = ['pattern','domain_id', 'total_strands', 'pattern_length', 'strands_before','sheet','whole_protein']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(patterns_arr)