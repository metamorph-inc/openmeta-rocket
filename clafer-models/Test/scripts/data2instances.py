"""
Author: Austin Tabulog
Email: austin.tabulog@metamorphsoftware.com
Date: 01/10/2018

Objective: take a clafer data file (*.cfr.data) and create a specific directory of
           every individual instance from the data file without the claferIG tags

Input: in the command terminal, path to the scripts directory and call this script
       followed by the .cfr.data file ("python scripts/data2instances.py example_file.crf.data"
Output: directory of individual .txt files for every instance
"""

from sys import argv
from os import path, mkdir, getcwd

def separate_instances(data_file):
    # set variables
    instance = 1
    ext = '.'
    filename = data_file
    while ext in filename:
        filename = path.splitext(filename)[0]
    empty_line = '\n'

    # Create new model directory if necessary
    model_dir = getcwd()+'\{}'.format(filename)
    if not path.exists(model_dir):
        mkdir(model_dir)

    # Create new instance directory if necessary
    inst_dir = model_dir + '\Instances'
    if not path.exists(inst_dir):
        mkdir(inst_dir)

    # parse through *.cfr.data file looking for specific instances
    with open(data_file) as data:
        for line in data:
            instance_start = "=== Instance {} Begin ===".format(instance) #specific instance start lines

            # if line is an instance start, create a new file start writing to it
            if instance_start in line:
                file = open(path.join(inst_dir, "{}_{}.{}".format(filename, instance,'txt')), 'w')

            # if line is no longer about rocket object, close file, and up the instance counter
            elif 'Facility' in line:
                file.close()
                instance += 1
                break

            # for all other lines, clean up claferIG flags and avoid writing empty lines to instance files.
            # Writing empty lines will cause an I/O error inbetween instances
            else:
                new_line = clean_line(line)
                if new_line == empty_line:
                    pass
                else:
                    file.write(new_line)

# check if clafer flag is in line, and remove if so.
def clean_line(line):
    flag_list = ['c0_', 'c1_', 'c2_', 'c3_', 'c4_','c5_','c6_']
    for elem in flag_list:
        if elem in line:
            new_line = line.replace(elem,"")
            break
        else:
            new_line = line
    return new_line
separate_instances(argv[1])
