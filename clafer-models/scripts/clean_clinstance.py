from sys import argv
from os import path, mkdir, getcwd, remove

def clean_instances(data_file, counter, csv):
    """ Removes unnecessary numbers and symbols used by the claferIG."""
    with open(data_file) as data:
        filename = data_file.split('.')[0]
        instance = data_file.split('.')[2]

        if int(counter) != 0:
            filename = filename+str(counter)
        inst_dir=argv[0].replace("scripts/clean_clinstance.py","{}\\Instances".format(filename))

        file = open(path.join(inst_dir, "{}_{}.{}".format(filename, instance,'data')), 'w')
        for line in data:
            if '$' in line:
                newline = line.split('$')[0]
                file.write(newline+'\n')
            else:
                file.write(line)
    file.close()
    remove(data_file)

clean_instances(argv[1], argv[2], argv[3])
