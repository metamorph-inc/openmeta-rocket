from __future__ import print_function
from openmdao.api import Component, FileRef
from pprint import pprint
import numpy as np
import orhelper
from os import listdir, path

class SimOR(Component):
        def __init__(self):
                super(SimOR, self).__init__()

                # Input File
                self.add_param('rocketFile', FileRef('rocket.ork'), binary=True, pass_by_obj=True)
                self.add_param('WindSpeed', val=0.0)

                # Output Flight Metrics
                self.add_output('MaxVelocity', shape=1)
                self.add_output('MaxAltitude', shape=1)
                self.add_output('MaxAcceleration', shape=1)
                self.add_output('MaxMach', shape=1)
                self.add_output('GroundHitVelocity', shape=1)
                self.add_output('LaunchRodVelocity', shape=1)
                self.add_output('FlightTime', shape=1)
                self.add_output('MaxStability', shape=1)
                self.add_output('LaunchRodClearanceStability', shape=1)

                self.openRocket = None


        def solve_nonlinear(self, params, unknowns, resids):
                # Instantiate OpenRocket if it has not been already
                if self.openRocket == None:
                    dir = path.dirname(path.realpath(__file__))
                    jarpath = dir.replace("scripts","openmeta-OpenRocket.jar")
                    self.openRocket = orhelper.OpenRocketInstance(jarpath)

                # opens Open Rocket
                orh = orhelper.Helper()

                # Load document
                doc = orh.load_doc('rocket.ork')

                # Run OpenRocket simulation (first sim has a faulty motor)
                sim = doc.getSimulation(1)
                simOptions = sim.getOptions() # get handle for simulation options class
                simOptions.setRandomSeed(0) # get rid of randomization
                simOptions.setWindSpeedAverage( params['WindSpeed'] ) # set wind speed

                orh.run_simulation(sim)
                flightData = sim.getSimulatedData()
                data = orh.get_timeseries(sim, ['Time', 'Altitude', 'Stability margin calibers'] )
                events = orh.get_events(sim)

                # derive stability info
                launchRodCleared = events['Launch rod clearance']
                index_launchRodCleared = np.where(data['Time'] == launchRodCleared)
                stability_launchRodCleared = data['Stability margin calibers'][index_launchRodCleared]

                # export flight data
                unknowns['MaxVelocity'] = flightData.getMaxVelocity()
                unknowns['MaxAltitude'] = flightData.getMaxAltitude()
                unknowns['MaxAcceleration'] = flightData.getMaxAcceleration()
                unknowns['MaxMach'] = flightData.getMaxMachNumber()
                unknowns['GroundHitVelocity'] = flightData.getGroundHitVelocity()
                unknowns['LaunchRodVelocity'] = flightData.getLaunchRodVelocity()
                unknowns['FlightTime'] = flightData.getFlightTime()
                unknowns['MaxStability'] = np.nanargmax(data['Stability margin calibers'])
                unknowns['LaunchRodClearanceStability'] = stability_launchRodCleared


        def __del__(self):
            self.openRocket.__exit__( None, None, None )
