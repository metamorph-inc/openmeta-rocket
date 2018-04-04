Open Rocket Simulation Script Tips
===================================

### The Basics

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

with orhelper.OpenRocketInstance("..\openmeta-OpenRocket.jar"):
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
