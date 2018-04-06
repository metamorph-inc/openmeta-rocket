from __future__ import print_function
from openmdao.api import Component, FileRef
from pprint import pprint
from os import listdir, path
from xml.etree import ElementTree as ET
from random import uniform

class ORKfle(Component):
   """ Creates ORK file from OpenMETA config imputs."""
   def __init__(self):
       super(ORKfle, self).__init__()

       #Python wrapper inputs
       self.add_param('coneshape', val=0.0, description='nosecone shape', pass_by_obj=True)
       self.add_param('noselen_coeff', val=0.0)
       self.add_param('fintype', val=0.0, description='planform fin shape', pass_by_obj=True)
       self.add_param('fincount', val=0.0, description='number of fins', pass_by_obj=True)
       self.add_param('finprofile', val=0.0, description='fin profile', pass_by_obj=True)
       self.add_param('motorclass', val=0.0, description='class of motor', pass_by_obj=True)
       self.add_param('material', val=0.0, description='material used', pass_by_obj=True)
       self.add_param('density', val=0.0, description='density of material [kg/m^3]', pass_by_obj=True)
       self.add_param('finish', val=0.0, description='finish used', pass_by_obj=True)
       self.add_param('launchrodlength', val=0.0)

       # Output: ORK File
       self.add_output('ORK_File', FileRef('test.ork'), binary=True, pass_by_obj=True)

   def pull_template(self):
       """ Locastes advanced_template.ork and loads into memory for use."""
       dir = path.dirname(path.realpath(__file__))
       temp_path = path.join(dir, 'advanced_template.ork')
       tree = ET.parse(temp_path)
       return tree

   def write_ork(self, tempXML):
       """saves .ork file to specific result folder"""
       counter = 1
       temp_path = "test.ork"
       tempXML.write(temp_path, "utf-8", True)

   def edit_simulation(self, tempXML, launchrodlength):
       """ edits xml values for simulation(s)."""
       simroot = tempXML.find('./simulations/simulation/conditions')
       launchrodElem = simroot.find('launchrodlength')
       launchrodElem.text = str(launchrodlength)

    def edit_motordata(self, tempXML, motorclass):
        """ Remove all unsed motorclasses, save maximum used motor dimesions as variables."""
        motormountRoot = tempXML.find('.//innertube/motormount')
        motorlist = motormountRoot.findall('motor')
        with open('C:\\Users\\austin\\Desktop\\test.txt','w') as testout:
            for motor in motorlist
            testout.write(str())
        testout.close()

   def edit_nosecone(self, tempXML, coneshape, material, density, finish, body_diam, noselen_coeff):
       """ edits xml for the nosecone and its subcomponents."""
       noseroot = tempXML.find('.//nosecone')
       """Discrete changes"""
       #change coneshape
       (noseroot.find('shape')).text = coneshape
       #change material name and density attrib
       (noseroot.find('material')).text = material
       (noseroot.find('material')).attrib['density'] = str(density) #converts kg/m^3 to g/cm^3
       # change finish
       (noseroot.find('finish')).text = finish

       """Continuous changes"""
       noselen_scale = 2.0
       noselen_offset = 3.0
       noselen_ratio = noselen_coeff*noselen_scale + noselen_offset
       (noseroot.find('length')).text = str(noselen_ratio*body_diam)





   def solve_nonlinear(self, params, unknowns, resids):
       "This is the 'main' function"
       # set variables
       coneshape = params['coneshape']
       noselen_coeff = params['noselen_coeff']
       fintype = params['fintype']
       fincount = params['fincount']
       finprofile = params['finprofile']
       motorclass = params['motorclass']
       material = params['material']
       density = params['density']
       finish = params['finish']
       launchrodlength = params['launchrodlength']
       # create the template rocket file
       tempXML = self.pull_template()
       # remove all unused motors
       self.edit_motordata(tempXML, motorclass)
       # edit nosecone
       #self.edit_nosecone(tempXML, coneshape, material, density, finish, body_diam, noselen_coeff)
       #write file
       self.write_ork(tempXML)
