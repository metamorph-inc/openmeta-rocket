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
        rocketElem = tempXML.find('.//rocket')
        simElem = tempXML.find('.//simulations')
        motormountRoot = tempXML.find('.//innertube/motormount')
        motorlist = rocketElem.findall('motorconfiguration')
        simlist = simElem.findall('simulation')
        motormountlist = motormountRoot.findall('motor')
        motorsize_list = list()

        # remove elements using unselected motorclasses
        for motor in motorlist:
            motorconfigid = motor.attrib['configid']
            motorname = (motor.find('name')).text
            if motorclass not in motorname:
                rocketElem.remove(motor)
                for motor in motormountlist:
                    if motor.attrib['configid'] == motorconfigid:
                        motormountRoot.remove(motor)
                    else: #store motor dimesions for the correct class
                        motorsize_list.append([(motor.find('length')).text, (motor.find('diameter')).text])
                for sim in simlist:
                    simconfigidElem = sim.find('conditions/configid')
                    if simconfigidElem.text == motorconfigid:
                        simElem.remove(sim)

        # store maximum motor dimensions
        for elem in motorsize_list:
            if elem == motorsize_list[0]:
                elem1 = elem
            elif elem == motorsize_list[1]:
                elem2 = elem
                len_comparrison = max(elem1[0], elem2[0])
                diam_comparrison = max(elem1[1], elem2[1])
            else:
                len_comparrison = max(len_comparrison, elem[0])
                diam_comparrison = max(diam_comparrison, elem[1])
        max_motordimensions = [float(len_comparrison), float(diam_comparrison)]
        return max_motordimensions


    def edit_nosecone(self, tempXML, coneshape, material, density, finish, motor_dimensions, noselen_coeff):
        """ Edits xml for the nosecone and its subcomponents."""
        noseroot = tempXML.find('.//nosecone')
        "Discrete changes"
        (noseroot.find('shape')).text = coneshape #change coneshape
        (noseroot.find('material')).text = material #change material name and density attrib
        (noseroot.find('material')).attrib['density'] = str(density) #converts kg/m^3 to g/cm^3
        (noseroot.find('finish')).text = finish # change finish

        "Continuous changes"
        noselen_scale = 2.0 #calculated relaitonship
        noselen_offset = 3.0 #calculated relaitonship
        noselen_ratio = noselen_coeff*noselen_scale + noselen_offset
        (noseroot.find('length')).text = str(noselen_ratio*float(motor_dimensions[1]))


    def solve_nonlinear(self, params, unknowns, resids):
        """ This is the 'main' function."""
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

        # remove all unused motors and save max motor dimensions
        motor_dimensions = self.edit_motordata(tempXML, motorclass)

        # edit bodytubes
        

        # edit nosecone
        self.edit_nosecone(tempXML, coneshape, material, density, finish, motor_dimensions, noselen_coeff)

        #write file
        self.write_ork(tempXML)
