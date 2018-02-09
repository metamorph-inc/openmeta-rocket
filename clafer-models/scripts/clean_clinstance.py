from sys import argv
from os import path, mkdir, getcwd, remove

def clean_instances(data_file):
    with open(data_file) as data:
        filename = data_file.split('.')[0]
        instance = data_file.split('.')[2]
        inst_dir=argv[0].replace("scripts/clean_clinstance.py","{}\\Instances".format(filename))
        print("\n")
        print("***************")
        print(inst_dir)
        print("***************")
        file = open(path.join(inst_dir, "{}_{}.{}".format(filename, instance,'data')), 'w')
        for line in data:
            if '$' in line:
                newline = line.split('$')[0]
                file.write(newline+'\n')
            else:
                file.write(line)
    file.close()
    #remove(data_file)

clean_instances(argv[1])
