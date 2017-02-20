import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

import functions as fun

compare = input('Thickness comparision (y/n):')
if compare == 'n':

    date = input('Date in yyyymmdd (20170217):')
    datatype = input('Datatype (flow, force_travel, both):')
    volume = input('Volume of the syringe (3ml, 5ml):')
    speed = input('Speed of the test stand (70mm-min):')
    thickness = input('Thickness of the parylene and type (1.9umPAC):')
    if thickness == '0um':
        coatingposition = ''
    else:
        coatingposition = input('Coating position (onlyplugercoat):') + '_'
    trial = input('Trial (1st, 2nd, 3rd):')

    fun.save_plot(date, datatype, volume, speed, thickness, coatingposition, trial)

elif compare == 'y':
    datatype = input('Datatype (flow, force_travel, both):')

    if datatype == 'flow':
        date = input('Date in yyyymmdd (20170217):')
        volume = input('Volume of the syringe (3ml, 5ml):')
        speed = input('Speed of the test stand (70mm-min):')
        trial = input('Trial (1st, 2nd, 3rd):')

        number = int(input('Number of the thickness you want to compare (2):'))

        max_flow_list = []
        min_flow_list = []
        time_list = []
        for n in range(number):
            k = n + 1
            thickness = input('Thickness' + str(k) + ' you want to compare:')
            if n == 0:
                coatingposition = ''
            else:
                coatingposition = input('Coating position (onlyplugercoat):') + '_'
                #thick_array[[n]] = thickness
                #data = fun.extract(date, datatype, volume, speed, thickness, coatingposition, trial)
            data, time_flow = fun.extract_data(date, datatype, volume, speed, thickness, coatingposition, trial)
            max_flow_index = data['flow'].idxmax()
            max_flow_list.append(data.loc[max_flow_index, 'flow'])
            min_flow_index = data['flow'].idxmin()
            min_flow_list.append(data.loc[min_flow_index, 'flow'])
            time_list.append(time_flow)
            fig = plt.plot(data['time'], data['flow'], marker='.', linestyle='none', label = thickness + coatingposition)

        plot_margin = 1
        plt.ylim(min(min_flow_list) - plot_margin, max(max_flow_list) + plot_margin)
        plt.xlim(-plot_margin, max(time_list)+ plot_margin)
        plt.xlabel('Time (sec)')
        plt.ylabel('Flow Rate (mL/min)')
        plt.legend(loc = 'upper right')
        plt.title(volume + ' syringe with different parylene thickness coating')
        plt.savefig(date + 'data/' + 'plot/' + 'compare_' + str(number) + '_' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + trial + '.pdf')
        plt.show()

    elif datatype == 'force_travel':
        date = input('Date in yyyymmdd (20170217):')
        volume = input('Volume of the syringe (3ml, 5ml):')
        speed = input('Speed of the test stand (70mm-min):')
        trial = input('Trial (1st, 2nd, 3rd):')

        number = int(input('Number of the thickness you want to compare (2):'))

        max_force_list = []
        min_force_list = []
        time_list = []
        for n in range(number):
            k = n + 1
            thickness = input('Thickness' + str(k) + ' you want to compare:')
            if n == 0:
                coatingposition = ''
            else:
                coatingposition = input('Coating position (onlyplugercoat):') + '_'
                #thick_array[[n]] = thickness
                #data = fun.extract(date, datatype, volume, speed, thickness, coatingposition, trial)
            data, time_force = fun.extract_data(date, datatype, volume, speed, thickness, coatingposition, trial)
            max_force_index = data['load'].idxmax()
            max_force_list.append(data.loc[max_force_index, 'load'])
            min_force_index = data['load'].idxmin()
            min_force_list.append(data.loc[min_force_index, 'load'])
            time_list.append(time_force)
            fig = plt.plot(data['travel'], data['load'], marker='.', linestyle='none', label = thickness + coatingposition)



        plot_margin = 1
        plt.ylim(min(min_force_list) - plot_margin, max(max_force_list) + plot_margin)
        plt.xlim(-plot_margin, max(time_list)+ plot_margin)
        plt.xlabel('Travel Distance (mm)')
        plt.ylabel('Load (N)')
        plt.legend(loc = 'upper right')
        plt.title(volume + ' syringe with different parylene thickness coating')
        plt.savefig(date + 'data/' + 'plot/' + 'compare_' + str(number) + '_' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + trial + '.pdf')
        plt.show()
    else:
        print('wrong datatype')

else:
    print('wrong')
