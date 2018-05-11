Open Rocket Simulation Script Tips
===================================
Simulating OpenRocket from Python scripts requires the [modified version of OpenRocket](https://github.com/metamorph-inc/openmeta-rocket/blob/master/openmeta-OpenRocket.jar) in this repo's main directory and the Python-Java bridge library called JPype.
Instructions for installing JPype can be found in the [JPype folder](https://github.com/metamorph-inc/openmeta-rocket/tree/master/JPype).

## The Basics

When automating OR simulations in Python, the general flow is:
1. Open OpenRocket
2. Create instance of OR Helper class
3. Load the rocket's ORK file
4. Load a simulation stored in the ORK file
5. Optionally, modify simulation options and/or rocket design
6. Run simulation
7. Extract and analyze results

A very basic implementation of this as an OpenMETA Python component is shown below. 

```python
from __future__ import print_function
from openmdao.api import Component, FileRef
from pprint import pprint
from os import path
import orhelper

class OpenRocketSim(Component):
        def __init__(self):
                super(OpenRocketSim, self).__init__()

                # Input File
                self.add_param('rocketFile', FileRef('rocket.ork'), binary=True, pass_by_obj=True)
                self.add_param('WindSpeed', val=0.0)

                # Output Flight Metrics
                self.add_output('MaxAltitude', shape=1)

                self.openRocket = None

        def solve_nonlinear(self, params, unknowns, resids):
                # Open OpenRocket if it has not been already
                if self.openRocket == None:
                    dir = path.dirname(path.realpath(__file__))
                    jarpath = dir.replace("scripts","openmeta-OpenRocket.jar")
                    self.openRocket = orhelper.OpenRocketInstance(jarpath)

                # Create instance of OR Helper class
                orh = orhelper.Helper()

                # Load ORK file
                doc = orh.load_doc('rocket.ork')

                # Load first OpenRocket simulation in file
                sim = doc.getSimulation(1)

                # Modify simulation options
                simOptions = sim.getOptions() # get handle for simulation options class
                simOptions.setRandomSeed(0) # get rid of randomization
                simOptions.setWindSpeedAverage( params['WindSpeed'] ) # set wind speed

                # Run Simulation
                orh.run_simulation(sim)

                # Export simulation result
                flightData = sim.getSimulatedData()
                unknowns['MaxAltitude'] = flightData.getMaxAltitude()

        def __del__(self):
            self.openRocket.__exit__( None, None, None )
```

This OpenMETA Python block accepts an ORK file and wind speed as input, and output the rocket's simulated Apogee.

### Simulation Options
```python
# Modify simulation options
simOptions = sim.getOptions() # get handle for simulation options class
simOptions.setRandomSeed(0) # get rid of randomization
simOptions.setWindSpeedAverage( params['WindSpeed'] ) # set wind speed
```
## Simulation Output Types
### Flight Data
```python
# Export simulation result
flightData = sim.getSimulatedData()
unknowns['MaxAltitude'] = flightData.getMaxAltitude()
```
### Events & Time Series Data
```python
data = orh.get_timeseries(sim, ['Time', 'Stability margin calibers', 'Mass'] )
events = orh.get_events(sim)
```
**_List Time Series Data Types_**

## orhelper Functions
#### OpenRocketInstance( path_to_jar )

### Helper Class
#### Helper()
#### load_doc( rocket_file )
#### run_simulation( simulation_handle )

## Helpful OpenRocket Functions

### OpenRocket Document Class
#### getSimulation( sim_number )


### Simulation Class
#### getSimulatedData()
#### getOptions()


## Changing Parameters with Simulation Options Class

| Parameter            | Get Parameter Value                    | Change Parameter Value                                 |
| -------------------- |----------------------------------------| -------------------------------------------------------|
| Altitude             | float **getLaunchAltitude**()          | void **setLaunchAltitude**( float altitude )           |
| ISA Atmosphere       | bool **getISAAtmosphere**()            | void **setISAAtmosphere**( bool isa )                  |
| Latitude             | float **getLaunchLatitude**()          | void **setLaunchLatitude**( float latitude )           |
| Longitude            | float **getLaunchLongitude**()         | void **setLaunchLongitude**( float longitude )         |
| Launch Rod Length    | float **getLaunchRodLength**()         | void **setLaunchRodLength**( float length )            |
| Launch Rod Angle     | float **getLaunchRodAngle**()          | void **setLaunchRodAngle**( float angle )              |
| Launch Rod Direction | float **getLaunchRodDirection**()      | void **setLaunchRodDirection**( float direction )      |
| Max Step Angle       | float **getMaximumStepAngle**()        | void **setMaximumStepAngle**( float maximumAngle )     |
| Motor                | String **getMotorConfigurationID**()   | void **setMotorConfigurationID**( String ID )          |
| Pressure             | float **getLaunchPressure**()          | void **setLaunchPressure**( float pressure )           |
| Temperature          | float **getLaunchTemperature**()       | void **setLaunchTemperature**( float temperature )     |
| Time Step            | float **getTimeStep**()                | void **setTimeStep**( float timestep )                 |
| Wind Speed (Average) | float **getWindSpeedAverage**()        | void **setWindSpeedAverage**( float windspeed )        |
| Wind Turbulence      | float **getWindTurbulenceIntensity**() | void **setWindTurbulenceIntensity**( float intensity ) |


## Getting Simulation Data with Flight Data Class

| Flight Data Type     | Get Value                        |
| -------------------- |----------------------------------|
| Max Velocity         | float **getMaxVelocity**()       |
| Max Altitude         | float **getMaxAltitude**()       |
| Max Acceleration     | float **getMaxAcceleration**()   |
| Max Mach             | float **getMaxMachNumber**()     |
| Ground Hit Velocity  | float **getGroundHitVelocity**() |
| Launch Rod Velocity  | float **getLaunchRodVelocity**() |
| Flight Time          | float **getFlightTime**()        |
| Time to Apogee       | float **getTimeToApogee**()      |

