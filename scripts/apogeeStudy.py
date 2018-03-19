# Prints out the apogee obtained through simulating test.ork (generated using an OpenMETA PET) from a python script
# At this time, the path of test.ork must be entered manually
# Tested with jpype 0.5.4.2 and java 6.0

import numpy as np
import orhelper

with orhelper.OpenRocketInstance('..\openmeta-OpenRocket.jar'):
    orh = orhelper.Helper()

    # Load document
    doc = orh.load_doc('..\\results\\r2018-03-19--17-24-03_lx0yr0dg\\test.ork')

    # Run second OpenRocket simulation (first sim has a faulty motor)
    sim = doc.getSimulation(1)
    orh.run_simulation(sim)

    # Get events and test data for analysis
    events = orh.get_events(sim)
    data = orh.get_timeseries(sim, ['Time','Altitude'])

    # Use the Apogee event time to find the altitude from the Altitude time series data
    apogeeTime = events["Apogee"]
    apogeeIndex = int(np.where(data["Time"]==apogeeTime)[0])
    apogeeAltitude = data["Altitude"][apogeeIndex]

    print "Apogee Altitude: %.3f meters" % (apogeeAltitude)
