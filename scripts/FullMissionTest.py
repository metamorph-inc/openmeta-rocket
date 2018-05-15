from __future__ import print_function
from openmdao.api import Component, FileRef
from pprint import pprint
from os import listdir, path
import numpy as np
import orhelper

class FullMissionTest(Component):
        def __init__(self):
                super(FullMissionTest, self).__init__()

                self.pathToRocket = 'C:\Users\metamorph\Documents\OR_source\ork_files\simple.ork'
                self.openRocket = None
                self.imageDirectory = 'Rocket_Images.zip'

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
                self.add_output('Rocket_Images', FileRef('Rocket_Images.zip'), binary=True, pass_by_obj=True)


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
                doc = orh.load_doc(self.pathToRocket)

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
                launchRodCleared = events['Launch rod clearance']
                index_launchRodCleared = np.where(data['Time'] == launchRodCleared)
                stability_launchRodCleared = data['Stability margin calibers'][index_launchRodCleared]
                mass_launchRodCleared = data['Mass'][index_launchRodCleared]

                motorBurnout = events['Motor burnout']
                index_motorBurnout = np.where(data['Time'] == motorBurnout)
                mass_motorBurnout = data['Mass'][index_motorBurnout]

                # export flight data
                unknowns['MaxVelocity'] = flightData.getMaxVelocity()
                unknowns['MaxAltitude'] = flightData.getMaxAltitude()
                unknowns['MaxAcceleration'] = flightData.getMaxAcceleration()
                unknowns['MaxMach'] = flightData.getMaxMachNumber()
                unknowns['GroundHitVelocity'] = flightData.getGroundHitVelocity()
                unknowns['LaunchRodVelocity'] = flightData.getLaunchRodVelocity()
                unknowns['FlightTime'] = flightData.getFlightTime()
                unknowns['MaxStability'] = data['Stability margin calibers'][np.nanargmax(data['Stability margin calibers'])]
                unknowns['LaunchRodClearanceStability'] = stability_launchRodCleared
                unknowns['LaunchRodClearanceMass'] = mass_launchRodCleared
                unknowns['BurnoutMass'] = mass_motorBurnout

        def __del__(self):
            self.openRocket.__exit__( None, None, None )
