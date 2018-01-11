"""
Author: Austin Tabulog
Email: austin.tabulog@metamorphsoftware.com
Date: 01/10/2018

Ojective: create separate instance files for a *.cfr.data file

Input: clafer data file (.cfr.data)

Output: directory of individual .txt files for every instance
"""
from sys import argv
from os import path, mkdir, getcwd

def separate_instances(data_file):
    # Create new instance directory if necessary
    inst_dir = getcwd()+'\Instances'
    if not path.exists(inst_dir):
        mkdir(inst_dir)

    # set variables
    instance = 1
    filename = path.splitext(path.splitext(data_file)[0])[0]
    empty_line = '\n'

    # parse through *.cfr.data file looking for specific instances
    with open(data_file) as data:
        for line in data:
            instance_start = "=== Instance {} Begin ===".format(instance) #looking for specific instance start lines
            instance_end = "--- Instance {} End ---".format(instance) #looking for specific instance end lines

            # if line is an instance start, create a new file start writing to it
            if instance_start in line:
                file = open(path.join(inst_dir, "{}_{}.{}".format(filename, instance,'txt')), 'w')
                file.write(line)

            # if line is an instance end, write end line, close file, and up the instance counter
            elif instance_end in line:
                file.write(line)
                file.close()
                instance += 1

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
    flag_list = ['c0_', 'c1_', 'c2_', 'c3_', 'c4_']
    for elem in flag_list:
        if elem in line:
            new_line = line.replace(elem,"")
            break
        else:
            new_line = line
    return new_line


separate_instances(argv[1])
# TODO: rewrite to be class based and reuse class variables for directories and other common variables
