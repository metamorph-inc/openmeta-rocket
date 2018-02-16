from sys import argv
from os import path

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
#import pdb; pdb.set_trace()
with open(argv[0].replace("scripts/cl_abstract.py","{}/{}_abstracts.csv".format(argv[2], ds_name)),'w') as write_file:
    for key, value in dict.items():
        counter = 0
        line = str(key)
        if len(value) > 1:
            while counter < len(value):
                str_val = str(value[counter])
                line = line + ",{}".format(str_val)
                counter += 1
        else:
            line = line + ",{}".format(str(value[counter]))
        line = line+'\n'
        write_file.write(line)
