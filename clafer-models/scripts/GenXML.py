from sys import argv
from os import listdir, path
from xml.etree import ElementTree as ET

class ORKfile:
    """class containing methods to create ork files from clafer instances and sizing scripts ."""
    def __init__(self, read_dir):
        """ declares variabless and create the template XML in memory"""
        self.read_dir = read_dir
        self.write_dir = read_dir.replace("Instances","XML")
        self.template_dir = argv[0].replace("GenXML.py","")
        self.tempXML = self.pull_template(self.template_dir)


    def buildMotormount(self, tempXML, ignitionevent, ignitiondelay, overhang, motor):
        """ Function to build only the specified motormount based on instance data."""
        motormount_args = locals()
        motormount_queries = dict()
        #For every variable passed into the function
        for key, value in motormount_args.items():
            motorflag = 0
            motormount_queries[key] = [value, './/{1}/{0}'.format(key,component)]
            found_elem = tempXML.find(motormount_queries[key][1])


    def buildNosecone(self, tempXML, name, finish, material, length, thickness, shape, shapeparameter, aftradius, aftshoulderradius, aftshoulderlength, aftshoulderthickness, aftshouldercapped):
        """ Function to build the nosecone based on instance data."""
        cone_args = locals()
        component = 'nosecone'
        cone_queries = dict()

        #For every variable passed into the function
        for key, value in cone_args.items():
            cone_queries[key] = [value, './/{1}/{0}'.format(key,component)]
            found_elem = tempXML.find(cone_queries[key][1])
            #edit element.text for all strings variables
            if isinstance(cone_queries[key][0], basestring):
                found_elem.text = cone_queries[key][0]
            #edit elem.attrib and elem.text for all list or tuple variables
            elif type(cone_queries[key][0]) is list or type(cone_queries[key][0]) is tuple:
                    attrib_count = 0
                    for attrib_key, attrib_value in found_elem.attrib.items():
                        found_elem.attrib[attrib_key] = cone_queries[key][0][attrib_count]
                        attrib_count += 1
                    found_elem.text = cone_queries[key][0][len(cone_queries[key][0])-1]


    def buildGenericFins(self, tempXML, fintype, name, position, finish, material, fincount, rotation, thickness, crosssection, cant, filletradius, filletmaterial):
        """ Function to build only the specified fintype; removes all other fintypes."""
        fin_args = locals()
        component = str(fintype)
        fin_queries = dict()

        #For every variable passed into the function
        for key, value in fin_args.items():
            finset_flag = 0
            fin_queries[key] = [value, './/{1}/{0}'.format(key,component)]
            found_elem = tempXML.find(fin_queries[key][1])

            # will occur if pointing to specific finset type
            if str(type(found_elem)) == "<type 'NoneType'>":
                fin_queries[key] = [value, './/{}'.format(component)]
                found_elem = tempXML.find(fin_queries[key][1])
                finset_flag = 1

            #edit element.text for all strings variables that are not the finset element
            if isinstance(fin_queries[key][0], basestring) and finset_flag==0:
                    found_elem.text = fin_queries[key][0]
            #edit elem.attrib and elem.text for all list or tuple variables
            elif type(fin_queries[key][0]) is list or type(fin_queries[key][0]) is tuple:
                attrib_count = 0
                for attrib_key, attrib_value in found_elem.attrib.items():
                    found_elem.attrib[attrib_key] = fin_queries[key][0][attrib_count]
                    attrib_count += 1
                found_elem.text = fin_queries[key][0][len(fin_queries[key][0])-1]

        #Remove unused fins from ORK
        fintype_list = ['freeformfinset', 'trapezoidfinset', 'ellipticalfinset']
        fintype_list.remove(fintype)
        for elem in fintype_list:
            finset = tempXML.find('.//*/{}'.format(elem))
            parent = tempXML.find('.//*/{}/..'.format(elem))
            parent.remove(finset)


    def buildInnetrube(name, position, material, length, radialposition, radialdirection, outerradius, thickness, clusterconfiguration, clusterscale, clusterrotation, motormount):
        pass


    def BuildLaunchlug(name, position, finish, material, radius, length, thickness, radialdirection):
        pass


    def buildBodytube(name, finish, material, length, thickness, radius, subcomponents):
        pass


    def buildStage(name, subcomponents):
        pass


    def buildRocket(self, tempXML, name, motorconfiguration, referencetype):
        "Select only one motor config and the corresponding simulation."
        rocket_args = locals()
        component = 'rocket'
        rocket_queries = dict()
        for key, value in rocket_args.items():
            if isinstance(value, basestring):
                rocket_queries[key] = [value, './/{1}/{0}'.format(key,component)]
                found_elem = tempXML.find(rocket_queries[key][1])
                found_elem.text = rocket_queries[key][0]

            elif key == 'motorconfiguration':
                rocket_queries[key] = [value[1], './/{}/{}[@configid="{}"]'.format(component, key, value[1])]
                motorid = value[1]
                found_elem = tempXML.find(rocket_queries[key][1])
                motorconfig_elem = tempXML.findall('.//motorconfiguration')
                rocket_elem = tempXML.find('.//rocket')
                for config in motorconfig_elem:
                    if config != found_elem:
                        rocket_elem.remove(config)
                rocket_queries['motorconfiguration_name'] = [value[0], './/{}/{}/name'.format(component,key)]
                config_name = tempXML.find(rocket_queries['motorconfiguration_name'][1])
                config_name.text = value[0]

        # select corresponding simulation
        simulations = tempXML.findall('.//*/simulation')
        sim = tempXML.find('.//simulations')
        simlist = list()
        for event in simulations:
            configid_elem = event.find('.//*/configid')
            configid = configid_elem.text
            if configid != motorid:
                simlist.append(event)
        counter = 0
        for item in simlist:
            sim.remove(simlist[counter])
            counter +=1

    def buildMotor(self, tempXML, configid):
        """ Function to build only the specified motor and correlating simulation event; removes all other motors and simulations."""
        motor_args = locals()
        component = 'motor'
        motor_queries = dict()
        for key, value in motor_args.items():
            if isinstance(value, basestring):
                if key == 'configid':
                    motor_queries[key] = [value, './/motormount/motor[@configid="{}"]'.format(value)]
                else:
                    motor_queries[key] = [value, './/{1}/{0}'.format(key,component)]
                found_elem = tempXML.find(motor_queries[key][1])
                if found_elem.tag == 'motor':
                    motor_elem = tempXML.findall('.//*/motor')
                    motormount_elem = tempXML.find('.//*/motormount')
                    for motor in motor_elem:
                        if motor != found_elem:
                            motormount_elem.remove(motor)


    def pull_template(self,template_dir):
        """Create template ork in memory."""
        tree = ET.parse(template_dir+'template.ork')
        root = tree.getroot()
        return tree

"======================================================================================================================="
sampleRocket=ORKfile('C:\\Users\\austin\\Desktop\\openmeta-rocket\\clafer-models\\manuf_rocket_space\\Instances')
sampleRocket.buildNosecone(sampleRocket.tempXML, 'parabolicCone', 'unfinished', ['bulk', '6.1', 'carbonFiber'], '0.2', '0.002', 'parabolic', '1.0', 'auto', '0.0', '0.0', '0.0', 'false')
sampleRocket.buildGenericFins(sampleRocket.tempXML, 'trapezoidfinset', 'trapfins', ['bottom','0.0'], 'smooth', ['bulk', '2.3', 'carbon_fiber'], '4', '10.0', '0.0025', 'rounded', '2.3', '0.005', ['bulk', '2.3', 'carbon_fiber'])
sampleRocket.buildMotor(sampleRocket.tempXML, 'fe0d7f7c-fbe8-488b-bf92-cc11c1a3b797')
sampleRocket.buildRocket(sampleRocket.tempXML, 'SupercoolRocket', ['K1', 'fe0d7f7c-fbe8-488b-bf92-cc11c1a3b797'], 'maximum')
#sampleRocket.buildMotormount(sampleRocket.tempXML, 'K1127LB', 'automatic', '0.0', '0.0', 'fe0d7f7c-fbe8-488b-bf92-cc11c1a3b797')
sampleRocket.tempXML.write('test.xml')

sampleRocket1=ORKfile('C:\\Users\\austin\\Desktop\\openmeta-rocket\\clafer-models\\manuf_rocket_space\\Instances')
sampleRocket1.buildNosecone(sampleRocket1.tempXML, 'ogiveCone', 'polished', ['bulk', '1.85', 'fiberglass'], '0.25', '0.003', 'ogive', '1.2', 'auto', '0.015', '0.01', '0.002', 'false')
sampleRocket1.buildGenericFins(sampleRocket1.tempXML, 'ellipticalfinset', 'elfins', ['top','0.0'], 'unfinished', ['bulk', '2.7', 'aluminum'], '3', '0.0', '0.0', 'square', '0', '0.0', ['bulk', '2.3', 'carbon_fiber'])
sampleRocket1.tempXML.write('test1.xml')
