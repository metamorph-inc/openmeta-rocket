from __future__ import print_function
from openmdao.api import Component
from pprint import pprint
from os import listdir, path
from xml.etree import ElementTree as ET

class ORKfile(Component):
    """ creates ORK file from OpenMETA config inputs."""
    def __init__(self):
        super(ORKfile, self).__init__()

        #Python wrapper inputs
        self.add_param('coneshape', val=0.0, description='nosecone shape', pass_by_obj=True)
        self.add_param('fintype', val=0.0, description='planform fin shape', pass_by_obj=True)
        self.add_param('fincount', val=0.0, description='number of fins', pass_by_obj=True)
        self.add_param('finprofile', val=0.0, description='fin profile', pass_by_obj=True)
        self.add_param('motorclass', val=0.0, description='class of motor', pass_by_obj=True)
        self.add_param('material', val=0.0, description='material used', pass_by_obj=True)
        self.add_param('density', val=0.0, description='density of material [kg/m^3]', pass_by_obj=True)
        self.add_param('finish', val=0.0, description='finish used', pass_by_obj=True)

        # Output: ORK File
        self.add_output('ORK_File', FileRef('test.ork'), binary=True)

    def pull_template(self):
        """ locates template.ork file, loads it into memory for use."""
        dir = path.dirname(path.realpath(__file__))
        temp_path = path.join(dir,'template.ork')
        tree = ET.parse(temp_path)
        return tree

    def write_ork(self, tempXML):
        """ find results folder for this run, create ORK folder, add file for each run."""
        counter=1
        temp_path = "test.ork"
        tempXML.write(temp_path, "utf-8", True)
        #temp_path = dir.replace("scripts\\{}".format(__file__), "")

    def edit_nosecone(self, tempXML, coneshape, material, density, finish):
        """ edits xml values for nosecone and any subcomponents within."""
        noseroot = tempXML.find('.//nosecone')
        shapeElem = noseroot.find('shape')
        shapeElem.text=coneshape
        matElem = noseroot.find('material')
        matElem.text = material
        matElem.attrib['density'] = str(density/1E3) #converts kg/m^3 to g/cm^3
        finishElem = noseroot.find('finish')
        finishElem.text=finish

    def edit_bodytube(self, tempXML, fintype, fincount, finprofile, motorclass, material, density, finish):
        """ edits xml values for bodytube and any subcomponents within the bodytube, including motor."""
        # body tube features
        bodyroot = tempXML.find('.//bodytube')
        bodymatElem = bodyroot.find('material')
        bodymatElem.text = material
        bodymatElem.attrib['density'] = str(density/1E3) #converts kg/m^3 to g/cm^3
        bodyfinishElem = bodyroot.find('finish')
        bodyfinishElem.text = finish

        #body tube subcomponents features
        bodysubroot = tempXML.find('.//bodytube/subcomponents')
        #only fins
        finElem = bodysubroot.find(fintype)
        finfinishElem = finElem.find('finish')
        finfinishElem.text = finish
        finmatElem = finElem.find('material')
        finmatElem.text = material
        finmatElem.attrib['density']=str(density/1E3) #converts kg/m^3 to g/cm^3
        fincountElem = finElem.find('fincount')
        fincountElem.text = str(fincount)
        finprofileElem = finElem.find('crosssection')
        finprofileElem.text=finprofile


        #remove excess finsets
        if fintype != 'trapezoidfinset':
            bodysubroot.remove(bodysubroot.find('trapezoidfinset'))
        if fintype != 'ellipticalfinset':
            bodysubroot.remove(bodysubroot.find('ellipticalfinset'))
        if fintype != 'freeformfinset':
            bodysubroot.remove(bodysubroot.find('freeformfinset'))
        #remove excess motors
        rocketElem = tempXML.find('.//rocket')
        simElem = tempXML.find('.//simulations')
        motorlist = rocketElem.findall('motorconfiguration')
        for elem in motorlist:
            motorconfigid = elem.attrib['configid']
            motornameElem = elem.find('name')
            motorname = motornameElem.text
            #remove simulations and configs related to unused motors
            if motorclass not in motorname:
                rocketElem.remove(elem)
                motormountElem = bodysubroot.find('innertube/motormount')
                innermotorlist = motormountElem.findall('motor')
                for motor in innermotorlist:
                    if motor.attrib['configid'] == motorconfigid:
                        motormountElem.remove(motor)
                simlist = simElem.findall('simulation')
                for sim in simlist:
                    simconfigidElem = sim.find('conditions/configid')
                    if simconfigidElem.text == motorconfigid:
                        simElem.remove(sim)

    def solve_nonlinear(self, params, unknowns, resids):
        """This will act as 'main' funciton. """
        # set variables
        coneshape = params['coneshape']
        fintype = params['fintype']
        fincount = params['fincount']
        finprofile = params['finprofile']
        motorclass = params['motorclass']
        material = params['material']
        density = params['density']
        finish = params['finish']
        print("CONESHAPE TYPE", type(coneshape))
        print("CONESHAPE", coneshape)

        # create the template rocket file
        tempXML = self.pull_template()
        # edit nosecone
        self.edit_nosecone(tempXML, coneshape, material, density, finish)
        # edit bodytube
        self.edit_bodytube(tempXML, fintype, fincount, finprofile, motorclass, material, density, finish)
        #write file
        self.write_ork(tempXML)

#import pdb; pdb.set_trace()
"""
test1=ORKfile()
xml=test1.pull_template()
test1.edit_nosecone(xml, 'ogive', 'carbon_fiber', 2300, 'polished')
test1.edit_bodytube(xml, 'trapezoidfinset', 5, 'airfoil', 'L', 'carbon_fiber', 2300, 'polished')
xml.write("C:\\Users\\austin\\Desktop\\openmeta-rocket\\scripts\\testN.ork")
"""
