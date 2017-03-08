import numpy as np
import scipy.special

# This is how we import the module of Matplotlib we'll be using
import matplotlib.pyplot as plt

# Some pretty Seaborn settings
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

import math

#second
t_5ml = 29.57
t_3ml = 36.94

#cm
r_5ml = 0.585
r_3ml = 0.418

l_tube = 50
r_tube = 0.15875

l_sensor = 5
r_sensor = 0.1

#viscosity of water N*s/m^2
mu = 1.002e-7

#flow velocity cm/second
v = 7/60


# The t-values we want
t_5 = np.linspace(0, t_5ml, 200)
t_3 = np.linspace(0, t_3ml, 200)

l_5ml = 4.556 - v * t_5
l_3ml = 5.44 - v * t_3

load_5ml = 8 * mu * v * math.pi * (r_5ml **2) * (l_tube/(r_tube **2) + l_sensor/(r_sensor **2) + l_5ml/(r_5ml **2)) * 10000
load_3ml = 8 * mu * v * math.pi * (r_5ml **2) * (l_tube/(r_tube **2) + l_sensor/(r_sensor **2) + l_3ml/(r_3ml **2)) * 10000


plt.plot(t_5, load_5ml)
plt.plot(t_3, load_3ml)
plt.xlabel('$t$')
plt.ylabel('load ($10^{-4}$ N)')
plt.show()
