from sys import argv
from os import path
from csv import writer

""" Looks through *.cfr and orders all the instances and abstracts together as a *.csv."""
with open(argv[1], 'r') as file:
    ds_name = path.splitext(argv[1])[0]
    dict = dict()
    for line in file:
        if ': ' in line:
            instance = [line.split(': ')[0]]
            abstract = (line.split(': ')[1]).replace("\n","")

            if abstract in dict:
                instance = line.split(': ')[0]
                dict[abstract].append(instance)
            else:
                dict[abstract]=instance

with open(argv[0].replace("scripts/cl_abstract.py","{}_abstracts.csv".format(ds_name)),'wb') as write_file:
    writer = writer(write_file)
    for key, value in dict.items():
        writer.writerow([key, value])
