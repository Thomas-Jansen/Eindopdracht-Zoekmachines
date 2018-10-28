# A JSON-parser to read questions.csv and create manageable sized json files 


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
jsonfile1 = open('questions1.json', 'w')
jsonfile2 = open('questions2.json', 'w')
jsonfile3 = open('questions3.json', 'w')
jsonfile4 = open('questions4.json', 'w')
jsonfile5 = open('questions5.json', 'w')

fieldnames = ("Number","Date","UserId","Category", "Question", "Continue_1", "Continue_2", "Continue_3")
reader = csv.DictReader( csvfile, fieldnames)

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

counter = 0
for row in reader:
    if (row["Number"].isdigit()):
        if (int(row["Number"]) < 100000):
            jsonfile1.write('{"index":{ "_index":"questions", "_id":' + str(counter) + '}}' + "\n")
            row["Question"] = clean(row["Question"])
            row["Continue_1"] = clean(row["Continue_1"])
            row["Continue_2"] = clean(row["Continue_2"])
            row["Continue_3"] = clean(row["Continue_3"])
            row["Question"] = row["Question"] + row["Continue_1"] + row["Continue_2"] + row["Continue_1"]
            row["Continue_1"] = ""
            row["Continue_2"] = ""
            row["Continue_3"] = ""
            # print(row)
            # print('\n')
            json.dump(row, jsonfile1)
            # jsonfile.write(',')
            jsonfile1.write('\n')
        elif (int(row["Number"]) < 200000):
            jsonfile2.write('{"index":{ "_index":"questions", "_id":' + str(counter) + '}}' + "\n")
            row["Question"] = clean(row["Question"])
            row["Continue_1"] = clean(row["Continue_1"])
            row["Continue_2"] = clean(row["Continue_2"])
            row["Continue_3"] = clean(row["Continue_3"])
            row["Question"] = row["Question"] + row["Continue_1"] + row["Continue_2"] + row["Continue_1"]
            row["Continue_1"] = ""
            row["Continue_2"] = ""
            row["Continue_3"] = ""
            # print(row)
            # print('\n')
            json.dump(row, jsonfile2)
            # jsonfile.write(',')
            jsonfile2.write('\n')
        elif (int(row["Number"]) < 300000):
            jsonfile3.write('{"index":{ "_index":"questions", "_id":' + str(counter) + '}}' + "\n")
            row["Question"] = clean(row["Question"])
            row["Continue_1"] = clean(row["Continue_1"])
            row["Continue_2"] = clean(row["Continue_2"])
            row["Continue_3"] = clean(row["Continue_3"])
            row["Question"] = row["Question"] + row["Continue_1"] + row["Continue_2"] + row["Continue_1"]
            row["Continue_1"] = ""
            row["Continue_2"] = ""
            row["Continue_3"] = ""
            # print(row)
            # print('\n')
            json.dump(row, jsonfile3)
            # jsonfile.write(',')
            jsonfile3.write('\n')
        elif (int(row["Number"]) < 400000):
            jsonfile4.write('{"index":{ "_index":"questions", "_id":' + str(counter) + '}}' + "\n")
            row["Question"] = clean(row["Question"])
            row["Continue_1"] = clean(row["Continue_1"])
            row["Continue_2"] = clean(row["Continue_2"])
            row["Continue_3"] = clean(row["Continue_3"])
            row["Question"] = row["Question"] + row["Continue_1"] + row["Continue_2"] + row["Continue_1"]
            row["Continue_1"] = ""
            row["Continue_2"] = ""
            row["Continue_3"] = ""
            # print(row)
            # print('\n')
            json.dump(row, jsonfile4)
            # jsonfile.write(',')
            jsonfile4.write('\n')
        elif (int(row["Number"]) < 500000):
            jsonfile5.write('{"index":{ "_index":"questions", "_id":' + str(counter) + '}}' + "\n")
            row["Question"] = clean(row["Question"])
            row["Continue_1"] = clean(row["Continue_1"])
            row["Continue_2"] = clean(row["Continue_2"])
            row["Continue_3"] = clean(row["Continue_3"])
            row["Question"] = row["Question"] + row["Continue_1"] + row["Continue_2"] + row["Continue_1"]
            row["Continue_1"] = ""
            row["Continue_2"] = ""
            row["Continue_3"] = ""
            # print(row)
            # print('\n')
            json.dump(row, jsonfile5)
            # jsonfile.write(',')
            jsonfile5.write('\n')
    counter += 1

