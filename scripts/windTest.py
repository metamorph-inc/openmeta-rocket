# FIXME: OpenRocket.jar has to be manually entered; file needs to be incorporated into OpenMETA

from __future__ import print_function
from openmdao.api import Component, FileRef
from pprint import pprint
import numpy as np
import orhelper

class WindTest(Component):
        def __init__(self):
                super(WindTest, self).__init__()

                # Input OR file and wind speed
                # self.add_param('rocketFile', FileRef('rocket.ork'), binary=True, pass_by_obj=True)
                self.add_param('WindSpeedAverage', val=0.0)

                # Output Flight Metrics
                self.add_output('MaxVelocity', shape=1)
                self.add_output('MaxAltitude', shape=1)
                self.add_output('MaxAcceleration', shape=1)
                self.add_output('MaxMach', shape=1)
                self.add_output('GroundHitVelocity', shape=1)
                self.add_output('LaunchRodVelocity', shape=1)
                self.add_output('FlightTime', shape=1)

                orhelper.OpenRocketInstance("C:\Users\metamorph\Documents\\rocket\scripts\openmeta-OpenRocket.jar")


        def solve_nonlinear(self, params, unknowns, resids):
                # creates Open Rocket Helper object, sets wind speed, runs simulation, and outputs flight data
                orh = orhelper.Helper()

                # Load OR document
                doc = orh.load_doc('C:\Users\metamorph\Documents\OR_source\ork_files\simple.ork')

                # set up simulation
                sim = doc.getSimulation(1) # Run second OpenRocket simulation (first sim has a faulty motor)
                simOptions = sim.getOptions() # get handle for simulation options class
                simOptions.setRandomSeed(0) # get rid of randomization
                simOptions.setWindSpeedAverage( params['WindSpeedAverage'] ) # set wind speed

                orh.run_simulation(sim)
                flightData = sim.getSimulatedData()

                # export flight data
                unknowns['MaxVelocity'] = flightData.getMaxVelocity()
                unknowns['MaxAltitude'] = flightData.getMaxAltitude()
                unknowns['MaxAcceleration'] = flightData.getMaxAcceleration()
                unknowns['MaxMach'] = flightData.getMaxMachNumber()
                unknowns['GroundHitVelocity'] = flightData.getGroundHitVelocity()
                unknowns['LaunchRodVelocity'] = flightData.getLaunchRodVelocity()
                unknowns['FlightTime'] = flightData.getFlightTime()
