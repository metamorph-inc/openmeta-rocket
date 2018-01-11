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

def findInstances(instance_dir):
    # build an xml only for instance .txt files in the instance folder
    for file in listdir(instance_dir):
        if path.splitext(file)[1] == '.txt':
            buildXML(file)

def buildXML(instance_file):
    # Create new XML directory if necessary
    XML_dir = getcwd()+'\XML'
    if not path.exists(XML_dir):
        mkdir(XML_dir)

    # create file
    xmlfile = open(path.join(XML_dir, "{}{}".format(path.splitext(instance_file)[0],".ork")),'w')
    xmlfile.close()

    #create start tags
    xmlfile.write(RocketXML.start_tag(instance_file, xmlfile))

    #reference clafer components with subcomponents to a rocket builder class


findInstances(getcwd()+'\Instances')








class RocketXML:
    def __init__(self):

    def start_tag(readfile, writefile)
