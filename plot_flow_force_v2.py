import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Read in flow rate data files with Pandas
flow_data = pd.read_csv('20170217data/flow_20170217_5ml_70mm-min_1.9umPAC_onlyplungercoat_2nd.csv')
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

# Read in flow rate data files with Pandas
force_data = pd.read_csv('20170217data/force_travel_20170217_5ml_70mm-min_1.9umPAC_onlyplungercoat_2nd.csv')
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

# Slice off the data after machine stops moving, therefore travel will not change anymore
max_travel_index = force_time0['travel'].idxmax()
force_time0 = force_time0[:max_travel_index + 1 - length + 1]

# Set time 0
time = force_data.loc[length-1, 'time']
force_time0['time'] = force_time0['time'] -time

force_time0 = force_time0.dropna()

# Find the limit of the x and y axis
# Find the index of the row with largest flow value
max_flow_index = flow_time0['flow'].idxmax()
# Find the maximum force
max_flow = flow_time0.loc[max_flow_index, 'flow']
# Find the index of the row with smallest flow value
min_flow_index = flow_time0['flow'].idxmin()
# Find the maximum force
min_flow = flow_time0.loc[min_flow_index, 'flow']

# Find the index of the row with largest load value
max_force_index = force_time0['load'].idxmax()
# Find the maximum force
max_force = force_time0.loc[max_force_index, 'load']
# Find the index of the row with smallest load value
min_force_index = force_time0['load'].idxmin()
# Find the maximum force
min_force = force_time0.loc[min_force_index, 'load']

# Find maximum time
time_flow = flow_data.loc[len(flow_data.index)-1, 'time']
time_force = force_data.loc[len(force_data.index)-1, 'time']
time_max = max(time_flow, time_force)


# Plot flow rate and force verse time
fig = plt.figure()
ax1 = fig.add_subplot(111)
lns1 = ax1.plot(flow_time0['time'], flow_time0['flow'],  sns.xkcd_rgb["denim blue"], linestyle='-', label = 'flow rate')

ax2 = ax1.twinx()
lns2 = ax2.plot(force_time0['time'], force_time0['load'], sns.xkcd_rgb["medium green"], linestyle='-', label = 'force')

# Make the legend together
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)

ax1.grid()
ax1.set_xlabel("Time (sec)")
ax1.set_ylabel("Flow rate (mL/min)")
ax2.set_ylabel("Force (N)")
axis_margin = 0.5
ax2.set_ylim(min_force - axis_margin, max_force + axis_margin)
ax1.set_ylim(min_flow - axis_margin, max_flow + axis_margin)
ax1.set_xlim(-axis_margin, time_max + axis_margin)
plt.show()
