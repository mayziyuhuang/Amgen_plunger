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
# When the travel is not zero anymore, consider it starts moving
# Set the one data point ahead of it as time zero

# Find the index that need to be cut off
flow_time_less0 = flow_data[flow_data['flow'] <= 0.008]
flow_time_less0['dsample'] = flow_time_less0['sample'] - flow_time_less0['sample'].shift(-1)
length = flow_time_less0['dsample'].idxmin()


# Define force_time0 dataframe
flow_time0 = flow_data.iloc[length:]

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
