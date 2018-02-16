from sys import argv
from os import path, remove, listdir

def clean_instances(instance_dir):
    """ Removes unnecessary numbers and symbols used by the claferIG."""

    # build csv dictionary
    csv_path = argv[1].split("Instances")[0]
    for child in listdir(csv_path):
        if '.' in child:
            if child.split('.')[1] == 'csv':
                csv_dict = dict()
                with open(csv_path+child) as csv_file:
                    for line in csv_file:
                        instance = list()
                        counter = 1
                        abstract = line.split(',')[0]
                        while counter < len(line.split(',')):
                            instance.append(line.split(',')[counter].replace("\n",""))
                            counter += 1
                        csv_dict[abstract]=instance


    for instance_file in listdir(instance_dir):
        if len(instance_file.split('.')) == 4:
            with open(argv[1]+'/'+instance_file) as data:
                filename = instance_file.split('.')[0]
                instance = instance_file.split('.')[2]

                #build files
                with open(path.join(instance_dir, "{}_{}.{}".format(filename, instance,'data')), 'w') as file:
                    #import pdb; pdb.set_trace()
                    for line in data:
                        if '\n' in line:
                            line=line.replace('\n','')
                        if '$' in line:
                            line = line.split('$')[0]
                        elif '$' not in line:
                            for key, value in csv_dict.items():
                                for cl_instance in value:
                                    if cl_instance in line:
                                        line = line.replace(cl_instance, "\n{}: {}".format(str(cl_instance), str(key)))
                                        break
                        file.write(line+'\n')

            remove(argv[1]+'/'+instance_file)

clean_instances(argv[1])
