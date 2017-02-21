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

        #maxtime = flow_data.loc[len(flow_data.index)-1, 'time']
        maxtime = flow_time0['time'].iloc[-1]


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

        #maxtime = force_data.loc[len(force_data.index)-1, 'time']
        maxtime = force_time0['time'].iloc[-1]


    else:
        print('Wrong datatype')

    return data, maxtime

def plot_flow(date, datatype, volume, speed, thickness, coatingposition, trial):
    data, time_flow = extract_data(date, datatype, volume, speed, thickness, coatingposition, trial)
    fig = plt.plot(data['time'], data['flow'], sns.xkcd_rgb["denim blue"], marker='.',
             linestyle='none')
    # Find the index of the row with largest flow value
    max_flow_index = data['flow'].idxmax()
    # Find the maximum force
    max_flow = data.loc[max_flow_index, 'flow']
    max_flow_time = data.loc[max_flow_index, 'time']
    # Find the index of the row with smallest flow value
    min_flow_index = data['flow'].idxmin()
    # Find the maximum force
    min_flow = data.loc[min_flow_index, 'flow']
    min_flow_time = data.loc[min_flow_index, 'time']

    fig = plt.plot(max_flow_time, max_flow, 'ro')
    fig = plt.text(max_flow_time, max_flow + 0.75, str(max_flow))

    fig = plt.plot(min_flow_time, min_flow, 'ro')
    fig = plt.text(min_flow_time, min_flow - 0.75, str(min_flow))

    plt.xlabel('Time (sec)')
    plt.ylabel('Flow Rate (mL/min)')
    plt.title(volume + ' syringe with ' + thickness + ' ' + coatingposition + ' ' + trial + ' trial')
    #plt.show()

    return fig

def plot_force(date, datatype, volume, speed, thickness, coatingposition, trial):
    data, time_force = extract_data(date, datatype, volume, speed, thickness, coatingposition, trial)
    fig = plt.plot(data['travel'], data['load'], sns.xkcd_rgb["medium green"], marker='.',
             linestyle='none')
    # Find the index of the row with largest load value
    max_force_index = data['load'].idxmax()
    # Find the maximum force
    max_force = data.loc[max_force_index, 'load']
    max_force_travel = data.loc[max_force_index, 'travel']
    # Find the index of the row with smallest load value
    min_force_index = data['load'].idxmin()
    # Find the maximum force
    min_force = data.loc[min_force_index, 'load']
    min_force_travel = data.loc[min_force_index, 'travel']

    fig = plt.plot(max_force_travel, max_force, 'ro')
    fig = plt.text(max_force_travel + 0.75, max_force , str(max_force))

    fig = plt.plot(min_force_travel, min_force, 'ro')
    fig = plt.text(min_force_travel + 0.75, min_force , str(min_force))

    plt.xlabel('Travel Distance (mm)')
    plt.ylabel('Load (N)')
    plt.title(volume + ' syringe with ' + thickness + ' ' + coatingposition + ' ' + trial + ' trial')

    #plt.show()

    return fig


def plot_flow_force(date, volume, speed, thickness, coatingposition, trial):
    flow_time0, time_flow = extract_data(date, 'flow', volume, speed, thickness, coatingposition, trial)
    force_time0, time_force = extract_data(date, 'force_travel', volume, speed, thickness, coatingposition, trial)

    # Find the limit of the x and y axis
    # Find the index of the row with largest flow value
    max_flow_index = flow_time0['flow'].idxmax()
    # Find the maximum force
    max_flow = flow_time0.loc[max_flow_index, 'flow']
    max_flow_time = flow_time0.loc[max_flow_index, 'time']
    # Find the index of the row with smallest flow value
    min_flow_index = flow_time0['flow'].idxmin()
    # Find the maximum force
    min_flow = flow_time0.loc[min_flow_index, 'flow']
    min_flow_time = flow_time0.loc[min_flow_index, 'time']

    # Find the index of the row with largest load value
    max_force_index = force_time0['load'].idxmax()
    # Find the maximum force
    max_force = force_time0.loc[max_force_index, 'load']
    max_force_travel = force_time0.loc[max_force_index, 'travel']
    # Find the index of the row with smallest load value
    min_force_index = force_time0['load'].idxmin()
    # Find the maximum force
    min_force = force_time0.loc[min_force_index, 'load']
    min_force_travel = force_time0.loc[min_force_index, 'travel']


    # Find maximum time
    time_max = max(time_flow, time_force)
    # Plot flow rate and force verse time
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    lns1 = ax1.plot(flow_time0['time'], flow_time0['flow'],  sns.xkcd_rgb["denim blue"], marker = '.', linestyle = 'none', label = 'flow rate')

    ax2 = ax1.twinx()
    lns2 = ax2.plot(force_time0['time'], force_time0['load'], sns.xkcd_rgb["medium green"], marker = '.', linestyle = 'none', label = 'force')

    # Make the legend together
    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc= "upper right")

    fig = ax1.plot(max_flow_time, max_flow, 'ro')
    fig = ax1.text(max_flow_time, max_flow + 0.75, str(max_flow))

    fig = ax1.plot(min_flow_time, min_flow, 'ro')
    fig = ax1.text(min_flow_time, min_flow - 0.75, str(min_flow))
    fig = ax2.plot(max_force_travel, max_force, 'ro')
    fig = ax2.text(max_force_travel + 0.75, max_force , str(max_force))

    fig = ax2.plot(min_force_travel, min_force, 'ro')
    fig = ax2.text(min_force_travel + 0.75, min_force , str(min_force))



    ax1.grid()
    ax1.set_xlabel("Time (sec)")
    ax1.set_ylabel("Flow rate (mL/min)")
    ax2.set_ylabel("Force (N)")
    axis_margin = 1
    ax2.set_ylim(min_force - axis_margin, max_force + axis_margin)
    ax1.set_ylim(min_flow - axis_margin, max_flow + axis_margin)
    ax1.set_xlim(-axis_margin, time_max + axis_margin)
    plt.title(volume + ' syringe with ' + thickness + ' ' + coatingposition + ' ' + trial + ' trial')

    return fig



def save_plot(date, datatype, volume, speed, thickness, coatingposition, trial):

    if datatype == 'flow':
        plot_flow(date, datatype, volume, speed, thickness, coatingposition, trial)
    elif datatype == 'force_travel':
        plot_force(date, datatype, volume, speed, thickness, coatingposition, trial)
    elif datatype == 'both':
        plot_flow_force(date, volume, speed, thickness, coatingposition, trial)

    else:
        print('Wrong datatype')

    plt.savefig(date + 'data/' + 'plot/' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + trial + '.pdf')
    plt.show()

    return None


def compare_data(date, datatype, volume, speed, number):
    number = int(number)
    if datatype == 'flow':
        max_flow_list = []
        min_flow_list = []
        time_list = []
        for n in range(number):
            k = n + 1
            thickness = input('Thickness' + str(k) + ' you want to compare:')
            if thickness == '0um':
                coatingposition = ''
            else:
                where = input('Coating position is onlyplungercoat (y/n):')
                if where == 'y':
                    coatingposition = 'onlyplungercoat_'
                else:
                    print('wrong')
            trial = input('Trial (1st, 2nd, 3rd):')
            #thick_array[[n]] = thickness
            #data = fun.extract(date, datatype, volume, speed, thickness, coatingposition, trial)
            data, time_flow = extract_data(date, datatype, volume, speed, thickness, coatingposition, trial)
            max_flow_index = data['flow'].idxmax()
            max_flow = data.loc[max_flow_index, 'flow']
            max_flow_list.append(max_flow)
            max_flow_time = data.loc[max_flow_index, 'time']
            min_flow_index = data['flow'].idxmin()
            min_flow = data.loc[min_flow_index, 'flow']
            min_flow_list.append(min_flow)
            min_flow_time = data.loc[min_flow_index, 'time']
            time_list.append(time_flow)

            fig = plt.plot(data['time'], data['flow'], marker='.', linestyle='none', label = thickness + coatingposition + trial)
            fig = plt.plot(max_flow_time, max_flow, 'ro')
            fig = plt.text(max_flow_time, max_flow + 0.75, str(max_flow))
            fig = plt.plot(min_flow_time, min_flow, 'ro')
            fig = plt.text(min_flow_time, min_flow - 0.75, str(min_flow))

        plot_margin = 1
        plt.ylim(min(min_flow_list) - plot_margin, max(max_flow_list) + plot_margin)
        plt.xlim(-plot_margin, max(time_list)+ plot_margin)
        plt.xlabel('Time (sec)')
        plt.ylabel('Flow Rate (mL/min)')
        plt.legend(loc = 'upper right')
        plt.title(volume + ' syringe with different parylene thickness coating')
        plt.savefig(date + 'data/' + 'plot/' + 'compare_' + str(number) + '_' + datatype + '_' + date + '_' + volume + '_' + speed + '.pdf')
    elif datatype == 'force_travel':
        max_force_list = []
        min_force_list = []
        max_travel_list = []
        time_list = []
        for n in range(number):
            k = n + 1
            thickness = input('Thickness' + str(k) + ' you want to compare:')
            if thickness == '0um':
                coatingposition = ''
            else:
                where = input('Coating position is onlyplungercoat (y/n):')
                if where == 'y':
                    coatingposition = 'onlyplungercoat_'
                else:
                    print('wrong')
            trial = input('Trial (1st, 2nd, 3rd):')
                #thick_array[[n]] = thickness
                #data = fun.extract(date, datatype, volume, speed, thickness, coatingposition, trial)
            data, time_force = extract_data(date, datatype, volume, speed, thickness, coatingposition, trial)
            max_force_index = data['load'].idxmax()
            max_force = data.loc[max_force_index, 'load']
            max_force_list.append(max_force)
            max_force_travel = data.loc[max_force_index, 'travel']
            min_force_index = data['load'].idxmin()
            min_force = data.loc[min_force_index, 'load']
            min_force_list.append(min_force)
            min_force_travel = data.loc[min_force_index, 'travel']
            time_list.append(time_force)
            max_travel_index = data['travel'].idxmax()
            max_travel_list.append(data.loc[max_travel_index, 'travel'])
            fig = plt.plot(data['travel'], data['load'], marker='.', linestyle='none', label = thickness + coatingposition + trial)
            fig = plt.plot(max_force_travel, max_force, 'ro')
            fig = plt.text(max_force_travel + 0.75, max_force , str(max_force))
            fig = plt.plot(min_force_travel, min_force, 'ro')
            fig = plt.text(min_force_travel + 0.75, min_force , str(min_force))

        plot_margin = 1
        plt.ylim(min(min_force_list) - plot_margin, max(max_force_list) + plot_margin)
        plt.xlim(-plot_margin, max(max_travel_list)+ plot_margin)
        plt.xlabel('Travel Distance (mm)')
        plt.ylabel('Load (N)')
        plt.legend(loc = 'upper right')
        plt.title(volume + ' syringe with different parylene thickness coating')
        plt.savefig(date + 'data/' + 'plot/' + 'compare_' + str(number) + '_' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + trial + '.pdf')
    else:
        print('wrong datatype')


    return plt.show()
