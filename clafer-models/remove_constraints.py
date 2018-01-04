from sys import argv
from os import path
def rename(input_file):
    broken_constraint = 'Uid not Found'
    arrow = '->'
    filename = path.splitext(path.splitext(input_file)[0])[0]+'_removed.dot'
    file = open("{}".format(filename),'w')
    with open(input_file) as f:
        for line in f:
            if broken_constraint not in line:
                file.write(line)
        file.close()
rename(argv[1])
