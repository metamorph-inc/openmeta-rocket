# FIXME: OpenRocket.jar has to be manually entered; file needs to be incorporated into OpenMETA
# FIXME: Jpype library needs to be incorporated into OpenMETA

from __future__ import print_function
from openmdao.api import Component, FileRef
from pprint import pprint
import numpy as np
import orhelper

class SimOR(Component):
        def __init__(self):
                super(SimOR, self).__init__()

                # Input File
                # self.add_param('x', val=0.0)
                self.add_param('rocketFile', FileRef('rocket.ork'), binary=True)

                # Output Flight Metrics
                self.add_output('MotorIgnition', shape=1)
                self.add_output('Liftoff', shape=1)
                self.add_output('GroundHit', shape=1)
                self.add_output('Launch', shape=1)
                self.add_output('LaunchRodClearance', shape=1)
                self.add_output('SimulationEnd', shape=1)
                # self.add_output('EjectionCharge', shape=1)
                # self.add_output('RecoveryDeviceDeployment', shape=1)
                self.add_output('Apogee', shape=1)
                self.add_output('MotorBurnout', shape=1)


        def solve_nonlinear(self, params, unknowns, resids):
                # opens Open Rocket, runs simulation, and outputs common flight metrics
                with orhelper.OpenRocketInstance("C:\Users\metamorph\Documents\\rocket\scripts\openmeta-OpenRocket.jar"):
                    orh = orhelper.Helper()

                    # Load document
                    doc = orh.load_doc('rocket.ork')

                    # Run second OpenRocket simulation (first sim has a faulty motor)
                    sim = doc.getSimulation(1)
                    orh.run_simulation(sim)

                    # Get events
                    events = orh.get_events(sim)

                    # Use the Apogee event time to find the altitude from the Altitude time series data
                    unknowns['MotorIgnition'] = events["Motor ignition"]
                    unknowns['Liftoff'] = events["Lift-off"]
                    unknowns['GroundHit'] = events["Ground hit"]
                    unknowns['Launch'] = events["Launch"]
                    unknowns['LaunchRodClearance'] = events["Launch rod clearance"]
                    unknowns['SimulationEnd'] = events["Simulation end"]
                    # unknowns['EjectionCharge'] = events['Ejection charge']
                    # unknowns['RecoveryDeviceDeployment'] = events["Recovery device deployment"]
                    unknowns['Apogee'] = events["Apogee"]
                    unknowns['MotorBurnout'] = events["Motor burnout"]
