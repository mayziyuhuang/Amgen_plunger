import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Read in flow rate data files with Pandas
flow_data = pd.read_csv('20170217data/flow_20170217_5ml_70mm-min_0um_2nd.csv')
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

### THIS DOES NOT WORK WITH DATA flow_20170217_5ml_70mm-min_0um_2nd
# There is no data less than 0.008 after the experiment ended
# The flow_time_less0 is the part that need to be cut off
# If the last row of flow_time_less0 - last row of flow_data < 1000
# Use the method above
# If not cut off the flow_time_less0

plt.plot(flow_time0['time'], flow_time0['flow'], marker='.',
         linestyle='none')
plt.xlabel('relative time (sec)')
plt.ylabel('flow rate (mL/min)')
plt.show()

#testing
#testing2

#git clone URL
#git status
#after making changes
#git add *
#git commit -m "message"
#git status
#git push

#git status
#git pull
