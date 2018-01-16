from os import getcwd, path, mkdir
from sys import argv
from xml.dom import minidom
from xml.etree import ElementTree as ET
class RocketXML:
    """class for building basic components to every OpenRocketrocket XML ."""
    def __init__(self, name):
        self.instance_name = name

    def gen_boilerplate(self, new_file, XML_dir):
        openrocket = ET.Element('openrocket')
        openrocket.set('version', '1.0')
        openrocket.set('creator', 'OpenRocket 15.03')

        rocket = ET.SubElement(openrocket,'rocket')
        rocket_name = ET.SubElement(rocket,'name')
        rocket_name.text = self.instance_name

        referencetype = ET.SubElement(rocket, 'referencetype')
        referencetype.text = 'maximum'

        subcomponents = ET.SubElement(rocket, 'subcomponents')
        stage = ET.SubElement(subcomponents, 'stage')
        stage_name = ET.SubElement(stage,'name')
        stage_name.text = 'Sustainer'

        stage_subcomponents = ET.SubElement(stage,'subcomponents')

        with open(path.join(XML_dir, new_file),'w') as output_file:
            #import pdb; pdb.set_trace()
            rough_string = ET.tostring(openrocket)
            reparsed_string = minidom.parseString(rough_string)
            output_file.write(reparsed_string.toprettyxml(indent='  '))


def gen_XML(cl_instance_file_path):
    #generate new Instance\XML directory if necessary
    #import pdb; pdb.set_trace()
    dir = getcwd()
    base_dir = 'C:\\Users\\austin\\Desktop\\openmeta-rocket\\clafer-models\\Test'
    if dir == base_dir:
        dir = dir+'\TestRocket'+'\Instances'

    XML_dir = dir.replace('Instances','XML')
    if not path.exists(XML_dir):
        mkdir(XML_dir)

    # Create RocektXML class instance of clafer instance
    #import pdb; pdb.set_trace()
    #cl_instance_name = path.splitext(path.basename(cl_instance_file_path))[0]
    cl_instance_name = path.splitext(path.basename(cl_instance_file_path))[0]
    Rocket_instance = RocketXML('{}'.format(cl_instance_name))
    Rocket_instance.gen_boilerplate(cl_instance_name+'.ork', XML_dir)

gen_XML(argv[1])

#TestRocket = RocketXML('TestRocket')
#TestRocket.gen_boilerplate(new_file)
