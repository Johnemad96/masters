import sys
import numpy
import argparse

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib.patches import Ellipse
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([0,3], [1,4], '-' , color="red")

plt.savefig("testplot",format="pdf")