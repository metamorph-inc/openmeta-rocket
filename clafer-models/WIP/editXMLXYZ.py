from sys import argv
from os import listdir, path
from xml.etree import ElementTree as ET
from xml.dom import minidom
"""
Objective: create an OpenRocket file corresponding to every clafer instance inside a directory
        1. copy XML template from the template.ork file
        2. parse the clafer file and make corresponding changes to new instance.ork

Input: An Instance directory containing several cleaned clafer instances
Output: An XML directory containing an OpenRocket XML (*.ork) for every clafer instance in the input directory
"""

def gen_ORK(read_dir):
    """input an Instance directory; writes the corresponding XML files."""

    write_dir = argv[1].replace("Instances","XML")
    template_dir = argv[0].replace("editXMLXYZ.py","")
    for file in listdir(read_dir):
        if path.splitext(file)[1] == '.data': #only for formatted instances
            tempXML = pull_template(template_dir)
            with open (read_dir+"/"+file, 'r') as readfile:
                changeXML_list = gen_query_dict(readfile)





def pull_template(template_dir):
    """Create template xml in memory."""

    tree = ET.parse(template_dir+'template.ork')
    root = tree.getroot()
    return root


def gen_query_dict(file):
    """Determine what lines from the clafer model will edit the XML.
    Save these lines as a dictionary following convention '{command: [path, value]}'
    """

    start_flag = 0
    file_list = list()
    query_dict = dict()

    for line in file:
        line_list = list()
        if ': Rocket' in line:
            start_flag=1
            rocket_name = line.split(":")[0]
            indent = len(line) - len(line.strip())
            line_list.append(indent)
            line_list.append(rocket_name.split("\n")[0])
            file_list.append(line_list)

        elif start_flag == 1 and line != "\n":
            indent = len(line) - len(line.strip())
            line_list.append(indent)
            line_list.append(line.strip().split("\n")[0])
            file_list.append(line_list)

        elif start_flag == 1 and line == "\n":
            break

    pair_count = 0
    for pair in file_list:
        # Statement for the first set (Value will always be name)
        if pair == file_list[0]:
            file_list[0].append('rocket_name')

        # Statement for the last set, which can be anything
        elif pair == file_list[len(file_list)-1]:
            file_list[len(file_list)-1].append(file_list[pair_count-1][1])
            prev_gen = 1
            ancestry_flag = 0
            while ancestry_flag == 0:
                parent = file_list[pair_count-prev_gen]
                ancestor = file_list[pair_count-(prev_gen+1)]
                prev_gen += 1

                if ancestor[0] < parent[0] and ancestor != file_list[0]:
                    file_list[pair_count].append(ancestor[1])
                else:
                    ancestry_flag =1

        # Statement all middle statements, which can be anything
        elif pair[0] > file_list[pair_count-1][0] and pair[0] > file_list[pair_count+1][0]:
            file_list[pair_count].append(file_list[pair_count-1][1])
            prev_gen = 1
            ancestry_flag = 0
            while ancestry_flag == 0:
                parent = file_list[pair_count-prev_gen]
                ancestor = file_list[pair_count-(prev_gen+1)]
                prev_gen += 1

                if ancestor[0] < parent[0] and ancestor != file_list[0]:
                    file_list[pair_count].append(ancestor[1])
                else:
                    ancestry_flag =1
        pair_count += 1

    # remove lists that are not lowest level
    query_list = list()
    for pair in file_list:
        if len(pair) > 2:
            query_list.append(pair)

    # check that ancestry tree doesn't break due to multiple children cases
    pair_count = 0
    for pair in query_list:
        if len(pair) != 0.5*pair[0] + 0.5 and pair != query_list[0]:
            query_list[pair_count].append(query_list[pair_count-1][len(query_list[pair_count-1])-1])
        pair_count += 1

    import pdb; pdb.set_trace()
    return query_list


"=============================================================================================================="
if __name__ == "__main__":
    gen_ORK(argv[1])
