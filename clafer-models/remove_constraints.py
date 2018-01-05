from sys import argv
from os import path
def rename(input_file):
    broken_constraint = 'Uid not Found'
    arrow = '->'
    orientation = 'rankdir=BT;'
    new_orientation = 'rankdir=RL;'
    filename = path.splitext(path.splitext(input_file)[0])[0]+'_removed.cvl.dot'
    file = open("{}".format(filename),'w')
    with open(input_file) as f:
        for line in f:
            if broken_constraint not in line:
                if orientation in line:
                    new_line = line.replace(orientation,new_orientation)
                    file.write(new_line)
                else:
                    file.write(line)
        file.close()
rename(argv[1])
