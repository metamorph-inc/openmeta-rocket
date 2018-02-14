from sys import argv
from os import listdir, path
"""
Objective: create an OpenRocket file corresponding to every clafer instance inside a directory
        1. copy XML template from the template.ork file
        2. parse the clafer file and make corresponding changes to new instance.ork

Input: An Instance directory containing several cleaned clafer instances
Output: An XML directory containing an OpenRocket XML (*.ork) for every clafer instance in the input directory
"""

def pull_ORK(read_dir, write_dir, template_dir):
    """ creates corresponding instance XML file, pulls format from existing XML, then fills in cfr data."""
    for file in listdir(read_dir):
        if path.splitext(file)[1] == '.data':
            #create template xml in memory
            tree = ET.parse(template_dir+'\\template.ork')
            root = tree.getroot()
            
'argv[1].replace("Instances","XML"),'
pull_ORK(argv[1], argv[0].replace("/editXMLXYZ.py",""))
