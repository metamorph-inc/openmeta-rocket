from __future__ import print_function
from openmdao.api import Component, FileRef
from pprint import pprint
from os import listdir, path
from xml.etree import ElementTree as ET
from random import uniform

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
        self.add_param('launchrodlength', val=0.0)

        # Output: ORK File
        self.add_output('ORK_File', FileRef('test.ork'), binary=True, pass_by_obj=True)

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

    def edit_simulation(self, tempXML, launchrodlength):
        """ edits xml values for simulation(s) """
        simroot = tempXML.find('./simulations/simulation/conditions')
        launchrodElem = simroot.find('launchrodlength')
        launchrodElem.text = str(launchrodlength)

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

        #edit launchlug
        lugroot = tempXML.find('.//bodytube/subcomponents/launchlug')
        (lugroot.find('position')).attrib['type'] = 'bottom'
        (lugroot.find('finish')).text = finish
        lugmatElem = lugroot.find('material')
        lugmatElem.text = material
        lugmatElem.attrib['density']=str(density/1E3) #converts kg/m^3 to g/cm^3

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

    def edit_continuous(self, tempXML, fintype):
        """ Edits all continuous variables that are a function of motor size."""
        motorsize_list = list()
        motorroot = tempXML.find('.//innertube/motormount')
        motorlist=motorroot.findall('motor')
        bodyroot = tempXML.find('.//bodytube')
        noseroot = tempXML.find('.//nosecone')
        finsetroot = tempXML.find('.//{}'.format(fintype))

        # get maximum motor length and diameter
        for motorElem in motorlist:
            motorsize_list.append([(motorElem.find('length')).text, (motorElem.find('diameter')).text])
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
        max_motorlen = float(len_comparrison)
        max_motordiam = float(diam_comparrison)

        #Edit bodytube sizing
        bodyradius=bodyroot.find('radius')
        bodyradius.text = str(max_motordiam/2.0 + 0.005)
        bodylength = bodyroot.find('length')
        bodylength.text = str(max_motorlen*uniform(2.0,3.0))
        if float(bodylength.text) < max_motorlen:
            bodylength.text = str(2.0*max_motorlen)
        bodythickness = bodyroot.find('thickness')
        bodythickness.text = str(2.0*float(bodyradius.text)/uniform(5.0,10.0))
        bodywallspace = abs(2*float(bodyradius.text)-(max_motordiam))/2
        if bodythickness.text > bodywallspace:
            bodythickness.text = str(bodywallspace-0.0025)

        #Edit nosecone sizing
        noselength = noseroot.find('length')
        noselength.text = str(2.0*float(bodyradius.text)*uniform(3.0,5.0))
        nosethickness = noseroot.find('thickness')
        nosethickness.text = bodythickness.text

        #edit finsets
        if fintype =='trapezoidfinset':
            finrootchord = finsetroot.find('rootchord')
            finrootchord.text = str(float(bodylength.text)/uniform(8.0,10.0))
            fintipchord = finsetroot.find('tipchord')
            fintipchord.text =  str(float(finrootchord.text)*uniform(2.0,3.0)/uniform(3.0,4.0))
            finheight = finsetroot.find('height')
            finheight.text =  str(float(finrootchord.text)/uniform(1.5,3.0))
            finposition = finsetroot.find('position')
            finposition.text =  str((-1)*float(finheight.text))
        elif fintype =='ellipticalfinset':
            finrootchord = finsetroot.find('rootchord')
            finrootchord.text =  str(float(bodylength.text)/uniform(8.0,10.0))
            finheight = finsetroot.find('height')
            finheight.text =  str(float(finrootchord.text)/uniform(1.5,3.0))
            finposition = finsetroot.find('position')
            finposition.text =  str((-1)*float(finheight.text))
        """
        if
        with open('C:\\Users\\austin\\Desktop\\test.txt','w') as testout:
            testout.write(str(fintype))
        testout.close()
        """

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
        launchrodlength = params['launchrodlength']

        # create the template rocket file
        tempXML = self.pull_template()
        # edit nosecone
        self.edit_nosecone(tempXML, coneshape, material, density, finish)
        # edit bodytube
        self.edit_bodytube(tempXML, fintype, fincount, finprofile, motorclass, material, density, finish)
        # size continuous variables with motor dimensions
        self.edit_continuous(tempXML, fintype)
        # edit simulation
        self.edit_simulation(tempXML, launchrodlength)
        #write file
        self.write_ork(tempXML)
