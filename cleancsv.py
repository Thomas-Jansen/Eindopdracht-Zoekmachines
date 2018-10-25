# import pandas as pd
#
# df = pd.read_csv("questions.csv")
# titel = pd.DataFrame(["index"])
# df = titel.append(df)
#
# df["index"].str().split(",", expand = True)
#
# for i in range(df.count()):
#     item = df[i]
#     if type(item["index"]) != int:
#         if (item["index"] != '\\'):
#             df[i-1].append(item["index"])
#         else:
#             df.drop(df.index[i])

import csv
import json
import re

def clean(row):
    new_row = ""
    if row != None:
        for x in row:
            if (x != "\n" and x != "\\" and x != "]" and x != "[" and x != ")" and x != "("):
                new_row = new_row + str(x)
        return new_row
    else:
        return ""



csvfile = open('questions.csv', 'r')
jsonfile = open('questionsklein.json', 'w')

fieldnames = ("Number","Date","UserId","Category", "Question", "Continue_1", "Continue_2", "Continue_3")
reader = csv.DictReader( csvfile, fieldnames)
jsonfile.write('{"Questions": [')


# for row in reader:
#     row["Question"] = clean(row["Question"])
#     row["Continue_1"] = clean(row["Continue_1"])
#     row["Continue_2"] = clean(row["Continue_2"])
#     row["Continue_3"] = clean(row["Continue_3"])
#     # print(row)
#     # print('\n')
#     json.dump(row, jsonfile)
#     jsonfile.write(',')
#     jsonfile.write('\n')
# jsonfile.write(']}')


# " " in row["Number"] or "/" in row["Number"] or "+" in row["Number"]
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

for row in reader:
    if (row["Number"].isdigit()):
        if (int(row["Number"]) < 1000):
            row["Question"] = clean(row["Question"])
            row["Continue_1"] = clean(row["Continue_1"])
            row["Continue_2"] = clean(row["Continue_2"])
            row["Continue_3"] = clean(row["Continue_3"])
            # print(row)
            # print('\n')
            json.dump(row, jsonfile)
            jsonfile.write(',')
            jsonfile.write('\n')

jsonfile.write(']}')





# jsonfile = open('questions.json', 'r')
# jsonfile2 = open('questionsClean.json', 'w')
#
# for object in jsonfile:
#     object = clean(object)
#     json.dump(object, jsonfile)
