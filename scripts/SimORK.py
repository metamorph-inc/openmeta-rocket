from __future__ import print_function
from openmdao.api import Component, FileRef
from pprint import pprint
import numpy as np
from matplotlib import pyplot as plt
from glob import glob
import zipfile
import zlib
from os import path
import os
import orhelper

class SimORK(Component):
        def __init__(self):
                super(SimORK, self).__init__()

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
                self.add_output('LaunchRodClearanceMass', shape=1) # rocket mass at launch rod clearance
                self.add_output('BurnoutMass', shape=1) # rocket mass at motor burnout
                self.add_output('Rocket_Images', FileRef('Rocket_Images.zip'), binary=True, pass_by_obj=True)

                self.openRocket = None
                self.imageDirectory = 'Rocket_Images.zip'

        def plot(self, data, events):
                # plot and save Trajectory
                fig1 = plt.figure()
                index_at = lambda t : (np.abs(data['Time']-t)).argmin()

                ax = fig1.add_subplot(111)
                events_to_annotate = ['Motor burnout', 'Apogee', 'Launch rod clearance']
                plt.title('Trajectory')
                ax.plot(data['Time'], data['Altitude'], 'm-')
                ax.set_xlabel('Time (s)')
                ax.set_ylabel('Altitude (m)', color='m')
                ax.grid(True)

                for name, time in events.items():
                    if not name in events_to_annotate: continue
                    ax.annotate(name, xy=(time, data['Altitude'][index_at(time)] ), xycoords='data', xytext=(20, 10), textcoords='offset points', arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3"))

                plt.savefig('trajectory.png')
                plt.close(fig1) # must explictly close figures to avoid unnecessary memory consumption

                # plot and save Thrust Curve
                fig2 = plt.figure()
                ax2 = fig2.add_subplot(111)
                # trim down thrust data so only relevant part of curve is shown (after motor burnout, all zero)
                realThrust = np.nonzero(data['Thrust'])
                realThrustEnd = realThrust[0][-1]
                thrustIndicies = np.arange(realThrustEnd+20)
                events_to_annotate = ['Motor burnout', 'Launch rod clearance']

                plt.title('Thrust')
                ax2.plot(data['Time'][thrustIndicies], data['Thrust'][thrustIndicies], 'c-')
                ax2.set_xlabel('Time (s)')
                ax2.set_ylabel('Thrust (N)', color='c')
                ax2.grid(True)

                for name, time in events.items():
                    if not name in events_to_annotate: continue
                    ax2.annotate(name, xy=(time, data['Thrust'][index_at(time)] ), xycoords='data', xytext=(20, 10), textcoords='offset points', arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3"))

                plt.savefig('thrust.png')
                plt.close(fig2) # must explictly close figures to avoid unnecessary memory consumption

                # zip images
                with zipfile.ZipFile(self.imageDirectory, 'w', zipfile.ZIP_DEFLATED) as rocket_zip:
                    rocket_zip.write('trajectory.png')
                    rocket_zip.write('thrust.png')

                # after zipping, original files can be discarded
                os.remove('trajectory.png')
                os.remove('thrust.png')


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
                data = orh.get_timeseries(sim, ['Time', 'Altitude', 'Stability margin calibers', 'Mass', 'Thrust'] )
                events = orh.get_events(sim)
                self.plot(data, events)

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
