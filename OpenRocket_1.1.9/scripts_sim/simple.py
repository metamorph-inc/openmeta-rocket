# Simple demonstration of running an OpenRocket simulation from a python script
# Prints the event/time pairs from the simulation
# Tested with jpype 0.5.4.2 and java 6.0

import numpy as np
import orhelper

with orhelper.OpenRocketInstance('..\openmeta-OpenRocket.jar'):
    orh = orhelper.Helper()

    # Load document, run simulation and get events

    doc = orh.load_doc('..\ork_files\simple.ork')
    sim = doc.getSimulation(0)
    print sim
    events = orh.get_events(sim)
    print ""
    print events
