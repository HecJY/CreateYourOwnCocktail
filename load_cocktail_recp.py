import numpy as np
import pprint
import csv
import re


COCKTAIL_DATABASE = "cocktail.csv"
#this function outputs cocktail grad grad, grad tech, grad tech amount
def grad_grad():
    cock_info = dict()
    index = 0
    with open(COCKTAIL_DATABASE, encoding='utf8') as file:
        cock_reader = csv.reader(file, delimiter = ",")
        for row in cock_reader:
            if index > 1:
                grad_raw = row[4]
                print(grad_raw)
                grad_filtered = gradfilter(grad_raw)

                tech_raw = row[7]

                print(row)
            index += 1


#filter the grad out
def gradfilter(raw_input):
    match = re.findall(r'[\w]+|[,]', raw_input)
    str1 = " "
    match = str1.join(match)
    match = re.findall(r'[^0-9]+', match)
    match = str1.join(match)
    match = re.findall(r'\b(?!oz|dash|ml)\b(\S+\s?[,]?)', match)
    match = str1.join(match)

    print(match)


    return match



if __name__ == '__main__':
    grad_grad()