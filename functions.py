import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

def extract_data(date, datatype, volume, speed, thickness, coatingposition, trial):

    if datatype == 'flow':
        flow_data = pd.read_csv(date + 'data/' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + trial + '.csv' )
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
        data = flow_time0


    elif datatype == 'force_travel':
        # Read in flow rate data files with Pandas
        force_data = pd.read_csv(date + 'data/' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + trial + '.csv' )
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
        #max_travel = force_time0.loc[max_travel_index, 'travel']

        #force_time0 = force_time0[force_time0['travel'] != max_travel]


        # Set time 0
        time = force_data.loc[length-1, 'time']
        force_time0['time'] = force_time0['time'] -time

        force_time0 = force_time0.dropna()
        data = force_time0
    else:
        print('Wrong datatype')

    return data

def plot_flow(date, datatype, volume, speed, thickness, coatingposition, trial):
    data = extract_data(date, datatype, volume, speed, thickness, coatingposition, trial)
    fig = plt.plot(data['time'], data['flow'], sns.xkcd_rgb["denim blue"], marker='.',
             linestyle='none')
    plt.xlabel('Time (sec)')
    plt.ylabel('Flow Rate (mL/min)')
    plt.title(volume + ' syringe with ' + thickness + ' ' + coatingposition + ' ' + trial + ' trial')
    #plt.show()

    return fig

def plot_force(date, datatype, volume, speed, thickness, coatingposition, trial):
    data = extract_data(date, datatype, volume, speed, thickness, coatingposition, trial)
    fig = plt.plot(data['travel'], data['load'], sns.xkcd_rgb["medium green"], marker='.',
             linestyle='none')
    plt.xlabel('Travel Distance (mm)')
    plt.ylabel('Load (N)')
    plt.title(volume + ' syringe with ' + thickness + ' ' + coatingposition + ' ' + trial + ' trial')

    #plt.show()

    return fig



def save_plot(date, datatype, volume, speed, thickness, coatingposition, trial):

    if datatype == 'flow':
        plot_flow(date, datatype, volume, speed, thickness, coatingposition, trial)
    elif datatype == 'force_travel':
        plot_force(date, datatype, volume, speed, thickness, coatingposition, trial)
    else:
        print('Wrong datatype')

    plt.savefig(date + 'data/' + 'plot/' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + trial + '.pdf')
    plt.show()

    return None
