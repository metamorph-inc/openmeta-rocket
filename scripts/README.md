Open Rocket Simulation Script Tips
===================================

## The Basics

When automating OR simulations in Python, the general flow is:
1. Open OpenRocket
2. Create instance of OR Helper class
3. Load the rocket's ORK file
4. Load a simulation stored in the ORK file
5. Optionally, modify simulation options and/or rocket design
6. Run simulation
7. Extract and analyze results

A very basic implementation of this is shown below. Notice that OpenRocket is opened
using Python's with statement. This is done to ensure that the JVM is properly shut down
after the script is done executing.

```python
import orhelper

with orhelper.OpenRocketInstance("OpenRocket.jar"):
    # Create instance of OR Helper class
    orh = orhelper.Helper()

    # Load rocket file
    doc = orh.load_doc("rocket.ork")

    # Load simulation from rocket file
    sim = doc.getSimulation(0)

    # Run simulation
    orh.run_simulation(sim)

    # Get flight data from simulation
    flightData = sim.getSimulatedData()

    print "Max Altitude: %.3f" % flightData.getMaxAltitude()
```

## Simulations in OpenMETA

```python
from __future__ import print_function
from openmdao.api import Component, FileRef
from pprint import pprint
import numpy as np
import orhelper

class WindTest(Component):
        def __init__(self):
                super(WindTest, self).__init__()

                # Input OR file and wind speed
                self.add_param('rocketFile', FileRef('rocket.ork'), binary=True, pass_by_obj=True)
                self.add_param('WindSpeedAverage', val=0.0)

                # Output Flight Metrics
                self.add_output('MaxAltitude', shape=1)

                # Open OpenRocket
                orhelper.OpenRocketInstance("openmeta-OpenRocket.jar")


        def solve_nonlinear(self, params, unknowns, resids):
                # Create instance of OR Helper class
                orh = orhelper.Helper()

                # Load the rocket's ORK file
                doc = orh.load_doc('rocket.ork')

                # Load a simulation stored in the ORK file
                sim = doc.getSimulation(0)

                # Modify simulation options and/or rocket design
                simOptions = sim.getOptions() # get handle for simulation options object
                simOptions.setRandomSeed(0) # remove simulation randomization
                simOptions.setWindSpeedAverage( params['WindSpeedAverage'] ) # set wind speed

                # Run simulation
                orh.run_simulation(sim)

                # Extract and analyze results
                flightData = sim.getSimulatedData() # get handle to flight data object
                unknowns['MaxAltitude'] = flightData.getMaxAltitude() # export maximum altitude
```


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


Time Series data
Events
