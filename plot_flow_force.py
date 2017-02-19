import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Read in flow rate data files with Pandas
flow_data = pd.read_csv('20170217data/flow_20170217_3ml_70mm-min_0um_2nd.csv')
flow_data.columns = ['sample', 'time', 'flow']

# The flow sensor can sense the flow in two direction
# Make the flow rate to be positive
flow_data.loc[:,'flow'] *= -1

# Slice off the time < 0
# When there is no flow through the flow meter, the reading is not zero, but 0.002, 0.008
# When the flow is not zero anymore, consider the syringe starts moving
# Set the one data point ahead of it as time zero

# Find the index that need to be cut off
# Find all the flow rate that is less than 0.008 which considered to be not moving
flow_time_less0 = flow_data[flow_data['flow'] <= 0.008]
# Since after stop the machine, the sensor still records the flow rate
# can not use the same method to cut off the zero part
# Comparing the sample number, when the dsample is not -1 anymore, that is when the flow rate becomes non zero for a long time
flow_time_less0['dsample'] = flow_time_less0['sample'] - flow_time_less0['sample'].shift(-1)
length = flow_time_less0['dsample'].idxmin()


# Define flow_time0 dataframe
flow_time0 = flow_data.iloc[length:]


# Set time 0
time = flow_data.loc[length, 'time']
flow_time0['time'] = flow_time0['time'] -time


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

# Set time 0
time = force_data.loc[length-1, 'time']
force_time0['time'] = force_time0['time'] -time

# Find the index of the row with largest load value
max_force_index = force_time0['load'].idxmax()
# Find the maximum force
max_force = force_time0.loc[max_force_index, 'load']

plt.plot(flow_time0['time'], flow_time0['flow'], marker='.', linestyle='-')
plt.plot(force_time0['time'], force_time0['load'], marker='.', linestyle='-')
plt.legend(('flow rate', 'force'), loc='lower right')

plt.xlabel('time (sec)')
plt.ylabel('flow rate (mL/min)')


#plt.ylabel('load (N)')
plt.show()
