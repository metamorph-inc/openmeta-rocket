"""
Author: Austin Tabulog
Email: austin.tabulog@metamorphsoftware.com
Date: 01/10/2018

Objective: create a OpenRocket .ork file (in .xml format) based on discrete
decisions made inside of clafer and continous variables decided in another
script

Input: instance.txt files created with data2instances.py

Output: XML formatted .ork files for every instance generated
"""
from sys import argv
from os import path, mkdir, getcwd, listdir

class RocketXML:
    def __init__(self, readfile, writefile):
        self.readfile = readfile
        self.writefile = writefile


    def build_start_tag(self):
        self.writefile.write("<?xml version='1.0' encoding='utf-8'?>\n")
        self.writefile.write('<openrocket version="1.0" creator="OpenRocket 15.03">\n')
        self.writefile.write('\t<rocket> \n')
        self.writefile.write('\t\t<name>Rocket</name> \n')
        self.writefile.write('\t\t<referencetype>maximum</referencetype> \n')
        self.writefile.write('\t\t<subcomponents> \n')
        self.writefile.write('\t\t\t<stage>\n')
        self.writefile.write('\t\t\t\t<name>Sustainer</name>\n')
        self.writefile.write('\t\t\t\t<subcomponents>\n')

    def build_end_tag(self):
        pass

    def build_body(self, line, prevline):
        self.line = line
        catch_body = '  body\n'
        if line == catch_body:
            self.writefile.write('\t\t\t\t  <bodytube>\n')
            self.writefile.write('\t\t\t\t    <name>Body tube</name>\n')
            self.writefile.write('\t\t\t\t    <finish>normal</finish>\n')
            self.writefile.write('\t\t\t\t    <material type="bulk" density="6100.0">Carbon fiber</material>\n')
            self.writefile.write('\t\t\t\t    <length>0.2</length>\n')
            self.writefile.write('\t\t\t\t    <thickness>0.002</thickness>\n')
            self.writefile.write('\t\t\t\t    <radius>auto</radius>\n')

    def build_nosecone(self):
        pass

    def build_fins(self):
        pass

def listXML(instance_dir):
    # Create new XML directory if necessary
    XML_dir = instance_dir.replace('Instances','XML')
    if not path.exists(XML_dir):
        mkdir(XML_dir)

    # build an xml only for instance .txt files in the instance folder
    for file in listdir(instance_dir):
        if path.splitext(file)[1] == '.txt':
            # create file
            instance_name = path.splitext(file)[0]
            xml_file = open(path.join(XML_dir, "{}{}".format(instance_name,".ork")),'w')
            #xml_file.close()
            populateXML(path.join(instance_dir,file), xml_file)


def populateXML(readfile, writefile):
    #create RocketXML instance
    instance = RocketXML(readfile, writefile)
    #write start tag
    RocketXML.build_start_tag(instance)
    with open(readfile) as read:
        #import pdb; pdb.set_trace()
        catch_body = "  body\n"
        catch_material = "  material\n"
        catch_nosecone = "  nosecone\n"
        catch_material = "  material\n"
        catch_surface_finish = "  surface_finish\n"
        counter = 1 # will be used to keep track of previous line
        for line in read:
            if counter == 1:
                prevline = line
            counter += 1
            if line == catch_body:
                RocketXML.build_body(instance, line, prevline)
            elif line == catch_material:
                RocketXML.build_material(instance, line, prevline)
            elif line == catch_nosecone:
                RocketXML.build_nosecone(instance, line, prevline)
            elif line == catch_material:
                RocketXML.build_material(instance, line, prevline)
            elif line == catch_surface_finish:
                RocketXML.build_surface_finish(instance, line, prevline)
            prevline = line

#reference clafer components with subcomponents to a rocket builder class

listXML(getcwd()+'\TestRocket')
