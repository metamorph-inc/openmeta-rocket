from xml.etree import ElementTree as ET
from os import path, mkdir, listdir
from sys import argv
"""
Objective: using a clafer instance file, write new values inside of an existing
           OpenRocket XML.ork file.
             1. parse clafer file for something useful
             2. know what that clafer thing means on .ork XML format
             3. find the corresponding element in the .ork file and replace

Input: clafer instance file, generic OpenRocket file

Output: a new OpenRocket file containing all clafer decisions
"""

def gen_XMLdir(cl_instance_filepath, basedir):
    XMLdir = cl_instance_filepath+"\\XML"
    CFRdir = cl_instance_filepath+"\\Instances"
    if not path.exists(XMLdir):
        mkdir(XMLdir)
    cledit_ORK(CFRdir,XMLdir, basedir)

def cledit_ORK(read_dir, write_dir, format_dir):
    facility_tag = ": Facility"
    rocket_tag = ": Rocket"
    #import pdb; pdb.set_trace()
    for file in listdir(read_dir):
        if path.splitext(file)[1] == '.txt':
            with open(read_dir+'\\'+file,'r') as CFR:
                tree = ET.parse(format_dir+'\\original.ork')
                root = tree.getroot()

                for line in CFR:
                    with open(write_dir+'\\'+path.splitext(file)[0]+'.ork','w') as XML:
                        XML.write(tree)
                        if facility_tag in line:
                            XML.close()
                            CFR.close()
                            break


gen_XMLdir(argv[1], argv[2])
