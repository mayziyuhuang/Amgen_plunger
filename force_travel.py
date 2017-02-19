import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Read in flow rate data files with Pandas
force_data = pd.read_csv('20170217data/force_travel_20170217_3ml_70mm-min_0um_2nd.csv')
force_data.columns = ['reading', 'load', 'travel', 'time']

# The test stand pushes the syring down so the travel indicator is negative
# Make the displacement to be positive
force_data.loc[:,'travel'] *= -1


# Slice off the time < 0
# When the travel is not zero anymore, consider it starts moving
# Set the one data point ahead of it as time zero

# Find the index that need to be cut off
force_time_less0 = force_data[force_data['travel'] <= 0]
length = len(force_time_less0.index)
# Define force_time0 dataframe
force_time0 = force_data.iloc[length-1:]


# Find the index of the row with largest load value
max_force_index = force_time0['load'].idxmax()
# Find the maximum force
max_force = force_time0.loc[max_force_index, 'load']

plt.plot(force_time0['travel'], force_time0['load'], marker='.',
         linestyle='-')
plt.xlabel('travel distance (mm)')
plt.ylabel('load (N)')
plt.show()
