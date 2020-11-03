import numpy as np
import matplotlib.pyplot as plt
import piecewise_scale   # adds piecewise-linear scale to matplotlib


x = np.arange(-1, 11, 0.01)
y = np.sin(x)

plt.plot(x, y, ls='-', lw=2)
plt.gca().set_xscale('piecewise-linear', fractions=[0., 0.8, 1.], values=[0, 5, 10])
plt.show()
