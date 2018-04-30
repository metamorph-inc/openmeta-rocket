from __future__ import print_function
from openmdao.api import Component
from pprint import pprint
import numpy as np

class Inverter(Component):
        def __init__(self):
                super(Inverter, self).__init__()

                # Input any numerical value
                self.add_param('x', val=0.0)

                # Output inverted input
                self.add_output('x_inverted', shape=1)


        def solve_nonlinear(self, params, unknowns, resids):
                # export inverted input
                unknowns['x_inverted'] = 1.0/params['x']
