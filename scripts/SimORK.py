from __future__ import print_function
from openmdao.api import Component, FileRef
from pprint import pprint
from os import listdir, path
import numpy as np
import orhelper

class SimOR(Component):
        def __init__(self):
                super(SimOR, self).__init__()

                # Input File
                self.add_param('rocketFile', FileRef('rocket.ork'), binary=True, pass_by_obj=True)
                self.add_param('Temperature', val=0.0)

                # Output Flight Metrics
                self.add_output('MaxVelocity', shape=1)
                self.add_output('MaxAltitude', shape=1)
                self.add_output('MaxAcceleration', shape=1)
                self.add_output('MaxMach', shape=1)
                self.add_output('GroundHitVelocity', shape=1)
                self.add_output('LaunchRodVelocity', shape=1)
                self.add_output('FlightTime', shape=1)

                dir = path.dirname(path.realpath(__file__))
                jarpath = dir.replace("scripts","openmeta-OpenRocket.jar")
                orhelper.OpenRocketInstance(jarpath)


        def solve_nonlinear(self, params, unknowns, resids):
                # opens Open Rocket, runs simulation, and outputs common flight metrics
                orh = orhelper.Helper()

                # Load document
                doc = orh.load_doc('rocket.ork')

                # Run second OpenRocket simulation (first sim has a faulty motor)
                sim = doc.getSimulation(1)
                simOptions = sim.getOptions() # get handle for simulation options class
                simOptions.setRandomSeed(0) # get rid of randomization
                simOptions.setWindSpeedAverage( params['Temperature'] ) # set wind speed

                orh.run_simulation(sim)

                flightData = sim.getSimulatedData() # get handle to flight data object

                # export flight data
                unknowns['MaxVelocity'] = flightData.getMaxVelocity()
                unknowns['MaxAltitude'] = flightData.getMaxAltitude()
                unknowns['MaxAcceleration'] = flightData.getMaxAcceleration()
                unknowns['MaxMach'] = flightData.getMaxMachNumber()
                unknowns['GroundHitVelocity'] = flightData.getGroundHitVelocity()
                unknowns['LaunchRodVelocity'] = flightData.getLaunchRodVelocity()
                unknowns['FlightTime'] = flightData.getFlightTime()
