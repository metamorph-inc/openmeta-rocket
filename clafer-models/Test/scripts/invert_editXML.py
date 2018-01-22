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
def build_nosecone(XML_elem, cl_file, read_dir):
    with open(read_dir+'\\'+cl_file,'r') as read_file:
        for line in read_file:
#-----------------------------------------------------------------------
# Nosecone
            if 'nosecone' in line:
                component = 'nosecone'
            elif 'type' in line:
                attrib = 'type'

#-----------------------------------------------------------------------
# Nosecone-Shape
            if 'parabolic' in line and component == 'nosecone' and attrib == 'type':
                for child in XML_elem:
                    if child.tag == 'shape':
                        child.text = 'parabolic'
            if 'hackmaan' in line and component == 'nosecone' and attrib == 'type':
                for child in XML_elem:
                    if child.tag == 'shape':
                        child.text = 'haackman'
            if 'ogive' in line and component == 'nosecone' and attrib == 'type':
                for child in XML_elem:
                    if child.tag == 'shape':
                        child.text = 'ogive'
#-----------------------------------------------------------------------
# Nosecone-Material
            if 'carbon_fiber' in line:
                for child in XML_elem:
                    if child.tag == 'material':
                        child.text = 'carbon fiber'
                        child.set('type','bulk')
                        child.set('density','6100.0')
            if 'fiberglass' in line:
                for child in XML_elem:
                    if child.tag == 'material':
                        child.text = 'fiberglass'
                        child.set('type','bulk')
                        child.set('density','1850.0')
            if 'aluminum' in line:
                for child in XML_elem:
                    if child.tag == 'material':
                        child.text = 'aluminum'
                        child.set('type','bulk')
                        child.set('density','2700.0')

"======================================================================"
def build_bodytube(XML_elem, cl_file, read_dir):
    "Build bodytube and all subcomponents like fins and motors ."
    with open(read_dir+'\\'+cl_file,'r') as read_file:
        for line in read_file:
#----------------------------------------------------------------------
# Body: to come, not supported in clafer design space yet.

#----------------------------------------------------------------------
# Fins
            if 'fins' in line:
                component = 'fins'
            elif 'type' in line:
                attrib = 'type'
            elif 'profile' in line:
                attrib = 'profile'
#-----------------------------------------------------------------------
# Fins-Shape
            #ET.dump(XML_elem)  #DEBUG
            if 'trapezoidal' in line and component == 'fins' and attrib == 'type':
                for bt_sub_comp in XML_elem:
                    if bt_sub_comp.tag == 'subcomponents':
                        for child in list(bt_sub_comp.getchildren()):
                            if child.tag == 'freeformfinset' or child.tag == 'ellipticalfinset':
                                bt_sub_comp.remove(child)

            elif 'elliptical' in line and component == 'fins' and attrib == 'type':
                for bt_sub_comp in XML_elem:
                    if bt_sub_comp.tag == 'subcomponents':
                        for child in list(bt_sub_comp.getchildren()):
                            if child.tag =='trapezoidfinset' or child.tag == 'freeformfinset':
                                bt_sub_comp.remove(child)
            elif 'freeform' in line and component == 'fins' and attrib == 'type':
                for bt_sub_comp in XML_elem:
                    if bt_sub_comp.tag == 'subcomponents':
                        for child in list(bt_sub_comp.getchildren()):
                            if child.tag =='trapezoidfinset' or child.tag == 'ellipticalfinset':
                                bt_sub_comp.remove(child)
#----------------------------------------------------------------------
# Fins-Profile
            if 'flat' in line and component == 'fins' and attrib == 'profile':
                for bt_sub_comp in XML_elem:
                    if bt_sub_comp.tag == 'subcomponents':
                        for fintypes in bt_sub_comp:
                            for child in fintypes:
                                if child.tag == 'crosssection':
                                    child.text = 'square'
            if 'subsonic' in line and component == 'fins' and attrib == 'profile':
                for bt_sub_comp in XML_elem:
                    if bt_sub_comp.tag == 'subcomponents':
                        for fintypes in bt_sub_comp:
                            for child in fintypes:
                                if child.tag == 'crosssection':
                                    child.text = 'rounded'
            if 'supersonic' in line and component == 'fins' and attrib == 'profile':
                for bt_sub_comp in XML_elem:
                    if bt_sub_comp.tag == 'subcomponents':
                        for fintypes in bt_sub_comp:
                            for child in fintypes:
                                if child.tag == 'crosssection':
                                    child.text = 'airfoil'
#----------------------------------------------------------------------
# Fins-material
            if 'carbon_fiber' in line:
                for bt_sub_comp in XML_elem:
                    if bt_sub_comp.tag == 'subcomponents':
                        for fins in bt_sub_comp:
                            for child in fins:
                                if child.tag == 'material':
                                    child.text = 'carbon fiber'
                                    child.set('type','bulk')
                                    child.set('density','6100.0')
            if 'fiberglass' in line:
                for bt_sub_comp in XML_elem:
                    if bt_sub_comp.tag == 'subcomponents':
                        for fins in bt_sub_comp:
                            for child in fins:
                                if child.tag == 'material':
                                    child.text = 'fiberglass'
                                    child.set('type','bulk')
                                    child.set('density','1850.0')
            if 'aluminum' in line:
                for bt_sub_comp in XML_elem:
                    if bt_sub_comp.tag == 'subcomponents':
                        for fins in bt_sub_comp:
                            for child in fins:
                                if child.tag == 'material':
                                    child.text = 'aluminum'
                                    child.set('type','bulk')
                                    child.set('density','2700.0')

#----------------------------------------------------------------------
# Fins-surface_finish
            

"======================================================================"
def gen_XMLdir(cl_instance_filepath, basedir):
    """ Checks if an instance XML directory exists, if not creates one, then calls cledit_ork."""
    XMLdir = cl_instance_filepath+"\\XML"
    CFRdir = cl_instance_filepath+"\\Instances"
    if not path.exists(XMLdir):
        mkdir(XMLdir)
    cledit_ORK(CFRdir,XMLdir, basedir)

"======================================================================"
def cledit_ORK(read_dir, write_dir, format_dir):
    """ creates corresponding instance XML file, pulls format from existing XML, then ckecks cfr for correct generation."""
    # init xml creation for every instance file
    for file in listdir(read_dir):
        if path.splitext(file)[1] == '.txt':
            #create xml in memory
            tree = ET.parse(format_dir+'\\template.ork')
            root = tree.getroot()
            #find things to be changed by clafer
            for rocket in root:
                if rocket.tag == 'rocket':
                    for sub_comp in rocket:
                        if sub_comp.tag == 'subcomponents':
                            for stage in sub_comp:
                                if stage.tag == 'stage':
                                    for sub_comp_stage in stage:
                                        if sub_comp_stage.tag == 'subcomponents':
                                            for children in sub_comp_stage:
                                                if children.tag == 'nosecone':
                                                    build_nosecone(children, file, read_dir)
                                                if children.tag == 'bodytube':
                                                    build_bodytube(children, file, read_dir)

        with open(write_dir+'\\'+path.splitext(file)[0]+'.ork','w') as XML:
            rough_string = ET.tostring(root)
            reparsed_string = minidom.parseString(rough_string)
            XML.write('\n'.join([line for line in reparsed_string.toprettyxml(indent='    ').split('\n') if line.strip()]))

gen_XMLdir(argv[1], argv[2])
