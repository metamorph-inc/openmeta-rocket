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
        self.add_param('coneshape', val=u'', description='nosecone shape', pass_by_obj=True)
        self.add_param('fintype', val=u'', description='planform fin shape', pass_by_obj=True)
        self.add_param('fincount', val=0.0, description='number of fins', pass_by_obj=True)
        self.add_param('finprofile', val=u'', description='fin profile', pass_by_obj=True)
        self.add_param('motorclass', val=u'', description='class of motor', pass_by_obj=True)
        self.add_param('material', val=u'', description='material used', pass_by_obj=True)
        self.add_param('finish', val=u'', description='finish used', pass_by_obj=True)

    def pull_template(self):
        temp_path = path.join(path.realpath(__file__),'template.ork')
        tree = ET.parse(temp_path)
        return tree

    def solve_nonlinear(self, params, unknowns, resids):
        """This will act as "main" funciton. """
        # set variables
        coneshape = params['coneshape']
        fintype = params['fintype']
        fincount = params['fincount']
        finprofile = params['finprofile']
        motorclass = params['motorclass']
        material = params['material']
        finish = params['finish']

        # create the template rocket file
        tempXML = self.pull_template()
        # edit nosecone
        # edit bodytube
