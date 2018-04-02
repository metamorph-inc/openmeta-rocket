import numpy as np
import orhelper
from random import gauss
import math

with orhelper.OpenRocketInstance("openmeta-OpenRocket.jar"):
    # opens Open Rocket, runs simulation, and outputs common flight metrics
    orh = orhelper.Helper()

    # Load document
    doc = orh.load_doc('rocket.ork')

    # Run second OpenRocket simulation (first sim has a faulty motor)
    sim = doc.getSimulation(0)
    # Randomize various parameters
    opts = sim.getOptions()
    rocket = opts.getRocket()
    num = 5

    # Run num simulations and add to self
    for p in range(num):
        print 'Running simulation ', p

        opts.setLaunchRodAngle(math.radians( gauss(45, 5) ))    # 45 +- 5 deg in direction
        opts.setLaunchRodDirection(math.radians( gauss(0, 5) )) # 0 +- 5 deg in direction
        opts.setWindSpeedAverage( gauss(15, 5) )                # 15 +- 5 m/s in wind
        for component_name in ('Nose cone', 'Body tube'):       # 5% in the mass of various components
            component = orh.get_component_named( rocket, component_name )
            mass = component.getMass()
            component.setMassOverridden(True)
            component.setOverrideMass( mass * gauss(1.0, 0.05) )

        orh.run_simulation(sim)


        # Get events
        events = orh.get_events(sim)
        data = orh.get_timeseries(sim, ['Time','Altitude'])

        # find altitude of apogee
        apogeeTime = events["Apogee"]
        apogeeIndex = int(np.where(data["Time"]==apogeeTime)[0])
        apogeeAltitude = data["Altitude"][apogeeIndex]

        print "Apogee Altitude: %.3f meters" % (apogeeAltitude)
