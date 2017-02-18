import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Read in flow rate data files with Pandas
force_data = pd.read_csv('force_travel_20170217_3ml_70mm-min_0um_2nd.csv')
force_data.columns = ['reading', 'load', 'travel', 'time']

force_data.loc[:,'travel'] *= -1

plt.plot(force_data['travel'], force_data['load'], marker='.',
         linestyle='-')
plt.xlabel('travel distance (mm)')
plt.ylabel('load (N)')
plt.show()
