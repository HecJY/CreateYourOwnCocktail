import numpy as np
import pprint
import csv
import re


COCKTAIL_DATABASE = "cocktail.csv"
#this function outputs cocktail grad grad, grad tech, grad tech amount
def grad_grad():
    gradA = dict()
    grad = dict()
    tech = dict()
    index = 0
    with open(COCKTAIL_DATABASE, encoding='utf8') as file:
        cock_reader = csv.reader(file, delimiter = ",")
        for row in cock_reader:
            if index > 1:
                name = row[0]
                grad_raw = row[4]
                tech_raw = row[7]
                print(grad_raw)
                print(tech_raw)
                grad_filtered = gradfilter(grad_raw)
                gradA_filtered = gradAfilter(grad_raw)
                if tech_raw:
                    tech_filtered = techfilter(tech_raw)
                else:
                    tech_filtered = ""

                grad[name] = grad_filtered
                gradA[name] = gradA_filtered
                tech[name] = tech_filtered
            index += 1

    return (grad,gradA,tech)


#filter the grad out
def gradfilter(raw_input):
    match = re.findall(r'[\w]+|[,]', raw_input)
    str1 = " "
    match = str1.join(match)
    match = re.findall(r'[^0-9]+', match)
    match = str1.join(match)
    match = re.findall(r'\b(?!oz|dash|ml)\b(\S+\s?[,]?)', match)
    match = str1.join(match)
    match = match.replace(" ,",",")
    return match

def techfilter(raw):
    match = re.findall(r'[\w]+', raw)
    str1 = " "
    match = str1.join(match)
    match = match.replace(" ,", ",")
    return match

def gradAfilter(raw):
    match = re.findall(r'[.]|\w+|[,]', raw)
    str1 = " "
    match = str1.join(match)
    match = match.replace(" ,",",")
    return match




if __name__ == '__main__':
    A, B, C = grad_grad()

    pprint.pprint(B)
