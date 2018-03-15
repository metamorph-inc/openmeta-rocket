# Possible PET implementation of OpenRocketInstance
# NOT TESTED

from __future__ import print_function
from openmdao.api import Component
from pprint import pprint
import numpy as np
import orhelper

with orhelper.OpenRocketInstance('..\openmeta-OpenRocket.jar'):
    orh = orhelper.Helper()

class Rocket(Component):
        ''' Simulates the rocket design simple.ork '''

        def __init__(self):
                super(Rocket, self).__init__()

                ''' Inputs to the PythonWrapper Component are added here as params '''
                self.add_param('bodytube')
                self.add_param('fin')
                self.add_param('nosecone')

                ''' Outputs from the PythonWrapper Component are added here as unknowns '''
                self.add_output('maxaltitude')

        def solve_nonlinear(self, params, unknowns, resids):

                bodytube = params['bodytube']
                fin = params['fin']
                nosecone = params['nosecone']

                # Generate ork file

                ''' Run OpenRocket Simulation '''
                doc = orh.load_doc('..\ork_files\simple.ork')
                sim = doc.getSimulation(0)
                orh.run_simulation(sim)

                ''' Extract data '''
                events = orh.get_events(sim)

                unknowns['altitude'] = events(1) # Needs to be checked
