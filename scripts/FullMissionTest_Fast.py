from __future__ import print_function
from openmdao.api import Component, FileRef
from pprint import pprint
from os import listdir, path
import numpy as np
import orhelper

class FullMissionTest_Fast(Component):
        def __init__(self):
                super(FullMissionTest_Fast, self).__init__()

                self.pathToRocket = 'C:\Users\metamorph\Documents\openrocket-working\ork_files\simple.ork'
                self.openRocket = None

                # Input OR file and wind speed
                self.add_param('LaunchAltitude', val=0.0)
                self.add_param('LaunchLatitude', val=0.0)
                self.add_param('LaunchLongitude', val=0.0)
                self.add_param('LaunchRodLength', val=0.0)
                self.add_param('LaunchRodAngle', val=0.0)
                self.add_param('LaunchRodDirection', val=0.0)
                self.add_param('Pressure', val=0.0)
                self.add_param('Temperature', val=0.0)
                self.add_param('WindSpeedAverage', val=0.0)
                self.add_param('WindTurbulenceIntensity', val=0.0)

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
                self.add_output('LaunchRodClearanceMass', shape=1) # rocket mass at launch rod clearance
                self.add_output('BurnoutMass', shape=1) # rocket mass at motor burnout


        def solve_nonlinear(self, params, unknowns, resids):
                # Instantiate OpenRocket if it has not been already
                if self.openRocket == None:
                    dir = path.dirname(path.realpath(__file__))
                    jarpath = dir.replace("scripts","openmeta-OpenRocket.jar")
                    self.openRocket = orhelper.OpenRocketInstance(jarpath)

                # opens Open Rocket
                orh = orhelper.Helper()

                # Load document
                doc = orh.load_doc(self.pathToRocket)

                # Run OpenRocket simulation (first sim has a faulty motor)
                sim = doc.getSimulation(1)
                simOptions = sim.getOptions() # get handle for simulation options class
                simOptions.setRandomSeed(0) # get rid of randomization
                # Change simulation options input from OpenMETA
                simOptions.setLaunchAltitude(params['LaunchAltitude'])
                simOptions.setLaunchLatitude(params['LaunchLatitude'])
                simOptions.setLaunchLongitude(params['LaunchLongitude'])
                simOptions.setLaunchRodLength(params['LaunchRodLength'])
                simOptions.setLaunchRodAngle(params['LaunchRodAngle'])
                simOptions.setLaunchRodDirection(params['LaunchRodDirection'])
                simOptions.setLaunchPressure(params['Pressure'])
                simOptions.setLaunchTemperature(params['Temperature'])
                simOptions.setWindSpeedAverage(params['WindSpeedAverage'])
                simOptions.setWindTurbulenceIntensity(params['WindTurbulenceIntensity'])

                orh.run_simulation(sim)

                flightData = sim.getSimulatedData()
                data = orh.get_timeseries(sim, ['Time', 'Stability margin calibers', 'Mass'] )
                events = orh.get_events(sim)

                # derive stability and mass info
                try:
                    launchRodCleared = events['Launch rod clearance']
                    index_launchRodCleared = np.where(data['Time'] == launchRodCleared)
                    stability_launchRodCleared = data['Stability margin calibers'][index_launchRodCleared]
                    mass_launchRodCleared = data['Mass'][index_launchRodCleared]
                except:
                    # sometimes the simulation shuts down before launch rod clearance, so set values to -1 (error)
                    stability_launchRodCleared = -1
                    mass_launchRodCleared = -1

                try:
                    motorBurnout = events['Motor burnout']
                    index_motorBurnout = np.where(data['Time'] == motorBurnout)
                    stability_motorBurnout = data['Stability margin calibers'][index_motorBurnout]
                    mass_motorBurnout = data['Mass'][index_motorBurnout]
                except:
                    # sometimes the simulation shuts down before the motors burnout, so set burnout mass to -1 (error)
                    mass_motorBurnout = -1

                try:
                    index_maxStability = np.nanargmax(data['Stability margin calibers'])
                    maxStability =  data['Stability margin calibers'][index_maxStability]
                except:
                    # sometimes the simulation doesn't record stability, so set burnout mass to -1
                    maxStability = -1

                # export flight data
                unknowns['MaxVelocity'] = flightData.getMaxVelocity()
                unknowns['MaxAltitude'] = flightData.getMaxAltitude()
                unknowns['MaxAcceleration'] = flightData.getMaxAcceleration()
                unknowns['MaxMach'] = flightData.getMaxMachNumber()
                unknowns['GroundHitVelocity'] = flightData.getGroundHitVelocity()
                unknowns['LaunchRodVelocity'] = flightData.getLaunchRodVelocity()
                unknowns['FlightTime'] = flightData.getFlightTime()
                unknowns['MaxStability'] = maxStability
                unknowns['LaunchRodClearanceStability'] = stability_launchRodCleared
                unknowns['LaunchRodClearanceMass'] = mass_launchRodCleared
                unknowns['BurnoutMass'] = mass_motorBurnout

        def __del__(self):
            self.openRocket.__exit__( None, None, None )
