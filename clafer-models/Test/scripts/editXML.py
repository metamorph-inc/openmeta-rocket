from xml.etree import ElementTree as ET
from xml.dom import minidom
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
    """ Checks if an instance XML directory exists, if not creates one, then calls cledit_ork."""
    XMLdir = cl_instance_filepath+"\\XML"
    CFRdir = cl_instance_filepath+"\\Instances"
    if not path.exists(XMLdir):
        mkdir(XMLdir)
    cledit_ORK(CFRdir,XMLdir, basedir)

def cledit_ORK(read_dir, write_dir, format_dir):
    """ creates corresponding instance XML file, pulls format from existing XML, then fills in cfr data."""
    mission_tag = ": Mission"
    rocket_tag = ": Rocket"
    for file in listdir(read_dir):
        if path.splitext(file)[1] == '.txt':
            with open(read_dir+'\\'+file,'r') as CFR:
                tree = ET.parse(format_dir+'\\original.ork')
                root = tree.getroot()
                with open(write_dir+'\\'+path.splitext(file)[0]+'.ork','w') as XML:

                    for line in CFR:
                        if 'fins' in line:
                            component = 'fins'
                        elif 'nosecone' in line:
                            component = 'nosecone'
                        elif 'material' in line:
                            component = 'material'
                        elif 'surface_finish' in line:
                            component = 'surface_finish'
                        elif 'type' in line:
                            attrib = 'type'
                        elif 'profile' in line:
                            attrib = 'profile'

                        if 'trapezoidal' in line:
                            if attrib == 'type' and component == 'fins':
                                for child in root.iter():
                                    print(child.tag, child.attrib)
                                    if child.tag == 'ellipticalfinset':
                                        import pdb; pdb.set_trace()
                                        root.remove(child)

                                """
                                for child in root.iter():
                                    print(child.tag, child.attrib)
                                    if child.tag == 'ellipticalfinset':
                                        import pdb; pdb.set_trace()
                                        root.remove(child)
                                """
                                """
                                for ellipticalfinset in root.iter(root.findall('ellipticalfinset')):
                                    print('ellipticalfinset')
                                    root.remove(ellipticalfinset)
                                for freeformfinset in root.findall('freeformfinset'):
                                    print('freeformfinset')
                                    root.remove(freeformfinset)
                                """
                        if mission_tag in line:
                            pass
                            #XML.close()
                            #CFR.close()
                            #break

                    rough_string = ET.tostring(root)
                    reparsed_string = minidom.parseString(rough_string)
                    XML.write('\n'.join([line for line in reparsed_string.toprettyxml(indent='    ').split('\n') if line.strip()]))

gen_XMLdir(argv[1], argv[2])
