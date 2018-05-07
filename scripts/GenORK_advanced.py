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
        self.add_param('payload_mass', val=0.0)
        self.add_param('coneshape', val=0.0, description='nosecone shape', pass_by_obj=True)
        self.add_param('noselen_coeff', val=0.0)
        self.add_param('bodylen_coeff', val=0.0)
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
        """
        temp_path = "test{}.ork".format(counter)
        if path.exists(temp_path):
            while path.exists(temp_path):
                counter += 1
                temp_path = "test{}.ork".format(counter)
        """
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
        motorsizeList = list()

        # remove elements using unselected motorclasses
        for motor in motorlist:
            motorconfigid = motor.attrib['configid']
            motorname = (motor.find('name')).text
            if motorclass not in motorname:
                rocketElem.remove(motor)
                for motor in motormountlist:
                    if motor.attrib['configid'] == motorconfigid:
                        motormountRoot.remove(motor)
                for sim in simlist:
                    simconfigidElem = sim.find('conditions/configid')
                    if simconfigidElem.text == motorconfigid:
                        simElem.remove(sim)
            else:
                for motor in motormountlist:
                    if motor.attrib['configid'] == motorconfigid:
                        motorsizeList.append([(motor.find('length')).text, (motor.find('diameter')).text])

        # store maximum motor dimensions
        for elem in motorsizeList:
            if elem == motorsizeList[0]:
                elem1 = elem
            elif elem == motorsizeList[1]:
                elem2 = elem
                len_comparrison = max(elem1[0], elem2[0])
                diam_comparrison = max(elem1[1], elem2[1])
            else:
                len_comparrison = max(len_comparrison, elem[0])
                diam_comparrison = max(diam_comparrison, elem[1])
        max_motordimensions = [float(len_comparrison), float(diam_comparrison)]
        return max_motordimensions


    def edit_bodytubes(self, tempXML, motor_dimensions, material, density, finish, bodylen_coeff, payload_mass, coneshape):
        """ Edits all bodytube dimensions, material, and finish."""
        bodytubeList = tempXML.findall(".//bodytube")
        for bodytube in bodytubeList:
            bodyroot = bodytube
            (bodyroot.find('finish')).text = finish
            (bodyroot.find('material')).text = material
            (bodyroot.find('material')).attrib['density'] = str(density) #converts kg/m^3 to g/cm^3
            tubetype = (bodytube.find('name')).text
            if tubetype == 'Payload tube':
                self.edit_payloadtube(bodytube, motor_dimensions, bodylen_coeff, payload_mass)
            elif tubetype == 'Recovery tube':
                self.edit_recoverytube(bodytube, motor_dimensions, bodylen_coeff)
            elif tubetype == 'Engine tube':
                self.edit_enginetube(tempXML, bodytube, motor_dimensions, bodylen_coeff, coneshape, material, density, finish)

    def edit_payloadtube(self, bodyroot, motor_dimensions, bodylen_coeff, payload_mass):
        payloadtubelen_scale = 2
        payloadtubelen_offset = 1.5
        tube_radius = (motor_dimensions[1]/2.0 + 0.005)/0.9
        tube_thickness = 0.10*tube_radius
        payloadtubelen_ratio = bodylen_coeff*payloadtubelen_scale + payloadtubelen_offset
        calc_len = payloadtubelen_ratio*float(motor_dimensions[0])
        (bodyroot.find('length')).text = str(calc_len/3.0)
        bodyroot.find('subcomponents/masscomponent/mass').text = str(payload_mass)
        "==========Edit internal Components=========="
        bulkheadRoot = bodyroot.find("subcomponents/tubecoupler/subcomponents/bulkhead")
        (bulkheadRoot.find("position")).text = str(-0.015)
        (bulkheadRoot.find("length")).text = str(0.015)
        (bulkheadRoot.find("outerradius")).text = str(tube_radius - tube_thickness)


    def edit_recoverytube(self, bodyroot, motor_dimensions, bodylen_coeff):
        recoverytubelen_scale = 1
        recoverytubelen_offset = 0.75
        recoverytubelen_ratio = bodylen_coeff*recoverytubelen_scale + recoverytubelen_offset
        calc_len = recoverytubelen_ratio*float(motor_dimensions[0])
        (bodyroot.find('length')).text = str(calc_len)

        "==========Edit internal Components=========="
        chuteList = bodyroot.findall("subcomponents/parachute")
        shockcordList = bodyroot.findall("subcomponents/shockcord")
        for chute in chuteList:
            if (chute.find("name")).text == "Drogue chute":
                (chute.find("packedlength")).text = str(0.20)
                (chute.find("packedradius")).text = str(0.025)
                (chute.find("diameter")).text = str(1.484)

            elif (chute.find("name")).text == "Main chute":
                (chute.find("packedlength")).text = str(0.21)
                (chute.find("packedradius")).text = str(0.03)
                (chute.find("diameter")).text = str(1.985)

        for shockcord in shockcordList:
            if (shockcord.find("name")).text == "Ripchord drogue chute":
                (shockcord.find("position")).text = str(-0.01)
                (shockcord.find("packedlength")).text = str(0.01)
                (shockcord.find("packedradius")).text = str(0.0275)
                (shockcord.find("cordlength")).text = str(0.6)

            elif (shockcord.find("name")).text == "Ripchord main chute":
                (shockcord.find("position")).text = str(0.0)
                (shockcord.find("packedlength")).text = str(0.02)
                (shockcord.find("packedradius")).text = str(0.0275)
                (shockcord.find("cordlength")).text = str(1.5)

    def edit_enginetube(self, tempXML, bodyroot, motor_dimensions, bodylen_coeff, coneshape, material, density, finish):
        """ Edit continuous values for the engine tube and subcomponents with resepect to motor values."""
        (bodyroot.find('length')).text = str(1.5*motor_dimensions[0] - 1.095*(motor_dimensions[1]/2.0))
        tube_radius = (motor_dimensions[1]/2.0 + 0.005)/0.9
        tube_thickness = 0.10*tube_radius
        (bodyroot.find('radius')).text = str(tube_radius)
        (bodyroot.find('thickness')).text = str(tube_thickness)

        "==========Edit internal Components=========="
        #Transition
        transroot = tempXML.find('.//transition')
        (transroot.find('shape')).text = coneshape
        (transroot.find('finish')).text = finish
        (transroot.find('material')).text = material
        (transroot.find('material')).attrib['density'] = str(density) #converts kg/m^3 to g/cm^3
        (transroot.find('length')).text = str((tube_radius - tube_thickness)/0.5774)
        (transroot.find('thickness')).text = str(tube_thickness)
        (transroot.find('aftradius')).text = str(motor_dimensions[1]/2.0 + 0.0005)
        #Motorsleeve
        innertubeRoot = tempXML.find('.//innertube')
        (innertubeRoot.find('length')).text = str(motor_dimensions[0])
        (innertubeRoot.find('outerradius')).text = str(motor_dimensions[1]/2.0 + 0.0005)
        (innertubeRoot.find('thickness')).text = str(0.0005)

        #engine block
        engineblockRoot = tempXML.find('.//engineblock')
        (engineblockRoot.find('material')).text = material
        (engineblockRoot.find('material')).attrib['density'] = str(density) #converts kg/m^3 to g/cm^3
        (engineblockRoot.find('length')).text = str(3*tube_thickness)
        (engineblockRoot.find('outerradius')).text = str(tube_radius - tube_thickness)
        (engineblockRoot.find('position')).text = str(-3*tube_thickness)
        (engineblockRoot.find('thickness')).text = str(6*tube_thickness)

        # centering rings
        centeringringlist = tempXML.findall('.//centeringring')
        for centeringringElem in centeringringlist:
            (centeringringElem.find('material')).text = material
            (centeringringElem.find('material')).attrib['density'] = str(density) #converts kg/m^3 to g/cm^3
            (centeringringElem.find('length')).text = str(2*tube_thickness)
            (centeringringElem.find('outerradius')).text = str(tube_radius - tube_thickness)
            (centeringringElem.find('innerradius')).text = str(motor_dimensions[1]/2.0 + 0.0005)
            if (centeringringElem.find('name')).text == "Forward centering ring":
                (centeringringElem.find('position')).text = str(motor_dimensions[0]/3)
            elif (centeringringElem.find('name')).text == "Aft centering ring":
                (centeringringElem.find('position')).text = str(-motor_dimensions[0]/3)

    def edit_finset(self, tempXML, material, density, finish, fintype, fincount, finprofile, motor_dimensions):
        """ Removes excess finset, edits values for fins."""
        bodytubeList = tempXML.findall(".//bodytube")
        tube_radius = (motor_dimensions[1]/2.0 + 0.005)/0.9
        tube_thickness = 0.10*tube_radius
        for bodyroot in bodytubeList:
            tubetype = (bodyroot.find('name')).text
            bodysubroot = bodyroot.find(".//subcomponents")
            if tubetype == 'Engine tube':
                if fintype == 'trapezoidfinset':
                    bodysubroot.remove(bodysubroot.find('ellipticalfinset'))
                    finsetRoot = bodysubroot.find('trapezoidfinset')
                    (finsetRoot.find('material')).text = material
                    (finsetRoot.find('material')).attrib['density'] = str(density) #converts kg/m^3 to g/cm^3
                    (finsetRoot.find('finish')).text = finish
                    (finsetRoot.find('fincount')).text = str(int(fincount))
                    (finsetRoot.find('thickness')).text =str(0.005) #half cm
                    (finsetRoot.find('crosssection')).text = finprofile
                    (finsetRoot.find('rootchord')).text = str(motor_dimensions[0]/1.25)
                    (finsetRoot.find('tipchord')).text = str(3*motor_dimensions[0]/8.0)
                    (finsetRoot.find('height')).text = str(2*tube_radius)

                if fintype == 'ellipticalfinset':
                    bodysubroot.remove(bodysubroot.find('trapezoidfinset'))
                    finsetRoot = bodysubroot.find('ellipticalfinset')
                    (finsetRoot.find('material')).text = material
                    (finsetRoot.find('material')).attrib['density'] = str(density) #converts kg/m^3 to g/cm^3
                    (finsetRoot.find('finish')).text = finish
                    (finsetRoot.find('fincount')).text = str(int(fincount))
                    (finsetRoot.find('thickness')).text =str(0.005) #half cm
                    (finsetRoot.find('crosssection')).text = finprofile
                    (finsetRoot.find('rootchord')).text = str(motor_dimensions[0]/2.0)
                    (finsetRoot.find('height')).text = str(2*tube_radius)

    def edit_launchlug(self, tempXML, material, density, finish, fincount, motor_dimensions):
        """ Edits xml for the launchlug size."""
        lugroot = tempXML.find('.//bodytube/subcomponents/launchlug')
        (lugroot.find('material')).text = material
        (lugroot.find('material')).attrib['density'] = str(density) #converts kg/m^3 to g/cm^3
        (lugroot.find('finish')).text = finish
        (lugroot.find('length')).text = str(motor_dimensions[0]/10.0)
        if fincount == 3.0:
            (lugroot.find('radialdirection')).text = str(60.0)
        elif fincount == 4.0:
            (lugroot.find('radialdirection')).text = str(45.0)

    def edit_nosecone(self, tempXML, coneshape, material, density, finish, motor_dimensions, noselen_coeff):
        """ Edits xml for the nosecone and its subcomponents."""
        noseroot = tempXML.find('.//nosecone')
        (noseroot.find('shape')).text = coneshape #change coneshape
        (noseroot.find('material')).text = material #change material name and density attrib
        (noseroot.find('material')).attrib['density'] = str(density) #converts kg/m^3 to g/cm^3
        (noseroot.find('finish')).text = finish # change finish
        noselen_scale = 2.0 #calculated relaitonship
        noselen_offset = 3.0 #calculated relaitonship
        noselen_ratio = noselen_coeff*noselen_scale + noselen_offset
        (noseroot.find('length')).text = str(noselen_ratio*float(motor_dimensions[1] + 0.01))


    def solve_nonlinear(self, params, unknowns, resids):
        """ This is the 'main' function."""
        # set variables
        payload_mass = params['payload_mass']
        coneshape = params['coneshape']
        noselen_coeff = params['noselen_coeff']
        bodylen_coeff = params['bodylen_coeff']
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
        self.edit_bodytubes(tempXML, motor_dimensions, material, density, finish, bodylen_coeff, payload_mass, coneshape)
        # edit nosecone
        self.edit_nosecone(tempXML, coneshape, material, density, finish, motor_dimensions, noselen_coeff)
        #edit finsets
        self.edit_finset(tempXML, material, density, finish, fintype, fincount, finprofile, motor_dimensions)
        #edit launchlug
        self.edit_launchlug(tempXML, material, density, finish, fincount, motor_dimensions)
        #write file
        self.write_ork(tempXML)
