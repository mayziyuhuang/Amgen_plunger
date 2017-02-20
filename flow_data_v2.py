import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Read in flow rate data files with Pandas
date = '20170217'
datatype = 'flow'
volume = '3ml'
speed = '70mm-min'
thickness = '1.9umPAC'
coatingposition = 'onlyplungercoat'
trial = '3rd'

flow_data = pd.read_csv(date + 'data/' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + '_' + trial + '.csv' )
#flow_data = pd.read_csv('20170217data/flow_20170217_3ml_70mm-min_1.9umPAC_onlyplungercoat_3rd.csv')
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

index_part1 = flow_time_less0["sample"].iloc[-1]
index_total = flow_data["sample"].iloc[-1]

if index_total - index_part1 > 1000:
    flow_time0 = flow_data.iloc[index_part1:]
    length = index_part1
else:
    # Since after stop the machine, the sensor still records the flow rate
    # can not use the same method to cut off the zero part
    # Comparing the sample number, when the dsample is not -1 anymore, that is when the flow rate becomes non zero for a long time
    flow_time_less0['dsample'] = flow_time_less0['sample'] - flow_time_less0['sample'].shift(-1)
    flow_time_less0 = flow_time_less0[flow_time_less0.dsample < -25]
    length = flow_time_less0['dsample'].idxmax()

    # Define flow_time0 dataframe
    flow_time0 = flow_data.iloc[length:]

# Set time 0
time = flow_data.loc[length, 'time']
flow_time0['time'] = flow_time0['time'] -time






plt.plot(flow_time0['time'], flow_time0['flow'], marker='.',
         linestyle='none')
plt.xlabel('relative time (sec)')
plt.ylabel('flow rate (mL/min)')
plt.show()
