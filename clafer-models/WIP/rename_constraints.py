from sys import argv
from os import path
def rename(input_file):
    broken_constraint = 'Uid not Found'
    arrow = '->'
    filename = path.splitext(path.splitext(input_file)[0])[0]+'_rename.dot'
    file = open("{}".format(filename),'w')
    with open(input_file) as f:
        for line in f:
            if broken_constraint in line:
                if arrow not in line:
                    start = '[ '
                    end = ']'
                    name = line[line.find(start):line.find(end)] + end
                    new_line = line.replace(broken_constraint, name)
                    file.write(new_line)
                else:
                    new_line = line.replace(broken_constraint, name)
                    file.write(new_line)

            else:
                file.write(line)
        file.close()
rename(argv[1])
