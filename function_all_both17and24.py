import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

def extract_flow_data(date, volume, speed, thickness, coatingposition, syringe, trial):
    if date == '20170224':
        file_name = date + 'data/' + 'flow' + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + syringe + '_' + 'syringe_' + trial + '_run_full.xls'
        excel_file = pd.ExcelFile(file_name)
        df = excel_file.parse('DataLog')
    elif date == '20170217':
        df =  pd.read_csv(date + 'data/' + 'flow' + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + trial + '.csv' )


    df.columns = ['sample', 'time', 'flow']
    df.loc[:, 'flow'] *= -1

    df_time_less0 = df[df['flow'] <= 0.008]
    index_part1 = df_time_less0["sample"].iloc[-1]
    index_total = df["sample"].iloc[-1]

    if index_total - index_part1 > 1000:
        df_time0 = df.iloc[index_part1:]
        length = index_part1
    else:
        df_time_less0['dsample'] = df_time_less0['sample'] - df_time_less0['sample'].shift(-1)
        df_time_less0 = df_time_less0[df_time_less0.dsample < -25]
        length = df_time_less0['dsample'].idxmax()
        if length > 6000:
            length = df_time_less0['dsample'].idxmin()
        df_time0 = df.iloc[length:]
    time = df.loc[length, 'time']
    df_time0['time'] = df_time0['time'] - time
    data = df_time0

    maxtime = df_time0['time'].iloc[-1]

    max_flow_index = data['flow'].idxmax()
    max_y = data.loc[max_flow_index, 'flow']
    max_x = data.loc[max_flow_index, 'time']
    min_flow_index = data['flow'].idxmin()
    min_y = data.loc[min_flow_index, 'flow']
    min_x = data.loc[min_flow_index, 'time']

    return data, maxtime, min_x, min_y, max_x, max_y

def extract_flow_data_stop(date, volume, speed, thickness, coatingposition, syringe, trial):
    file_name = date + 'data/' + 'flow' + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + syringe + '_' + 'syringe_' + trial + '_run_full.xls'
    excel_file = pd.ExcelFile(file_name)
    df = excel_file.parse('DataLog')

    df.columns = ['sample', 'time', 'flow']
    df.loc[:, 'flow'] *= -1

    df_time_less0 = df[df['flow'] <= 0.008]
    index_part1 = df_time_less0["sample"].iloc[-1]
    index_total = df["sample"].iloc[-1]

    if index_total - index_part1 > 1000:
        df_time0 = df.iloc[index_part1:]
        length = index_part1
    else:
        df_time_less0['dsample'] = df_time_less0['sample'] - df_time_less0['sample'].shift(-1)
        df_time_less0 = df_time_less0[df_time_less0.dsample < -25]
        length1 = df_time_less0['dsample'].idxmin()
        df_time = df_time_less0.sort(['dsample'])
        df_time = df_time[1:]
        length2 = df_time['dsample'].idxmin()
        length = min(length1, length2)

        df_time0 = df.iloc[length:]
    time = df.loc[length, 'time']
    df_time0['time'] = df_time0['time'] - time
    data = df_time0

    maxtime = df_time0['time'].iloc[-1]

    max_flow_index = data['flow'].idxmax()
    max_y = data.loc[max_flow_index, 'flow']
    max_x = data.loc[max_flow_index, 'time']
    min_flow_index = data['flow'].idxmin()
    min_y = data.loc[min_flow_index, 'flow']
    min_x = data.loc[min_flow_index, 'time']

    return data, maxtime, min_x, min_y, max_x, max_y

def extract_force_data(date, volume, speed, thickness, coatingposition, syringe, trial):
    if date == '20170224':
        file_name = date + 'data/' + 'force_travel' + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + syringe + '_' + 'syringe_' + trial + '_run_full.xlsx'
        excel_file = pd.ExcelFile(file_name)
        df = excel_file.parse('Sheet4')
    elif date == '20170217':
        df =  pd.read_csv(date + 'data/' + 'force_travel' + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + trial + '.csv' )



    df.columns = ['reading', 'load', 'travel', 'time']
    df.loc[:, 'travel'] *= -1

    df_time_less0 = df[df['travel'] <= 0]
    length = len(df_time_less0.index)
    df_time0 = df.iloc[length-1:]

    max_travel_index = df_time0['travel'].idxmax()
    maxtravel = df_time0.loc[max_travel_index, 'travel']
    df_time0 = df_time0[:max_travel_index + 1 - length + 1]

    time = df.loc[length - 1, 'time']
    df_time0['time'] = df_time0['time'] - time
    df_time0 = df_time0.dropna()

    data = df_time0

    maxtime = df_time0['time'].iloc[-1]

    max_force_index = data['load'].idxmax()
    max_y = data.loc[max_force_index, 'load']
    max_x = data.loc[max_force_index, 'travel']
    min_force_index = data['load'].idxmin()
    min_y = data.loc[min_force_index, 'load']
    min_x = data.loc[min_force_index, 'travel']

    return data, maxtime, min_x, min_y, max_x, max_y, maxtravel


def plot_flow(date, volume, speed, thickness, coatingposition, syringe, trial, stop):
    if stop == 'n':
        data = extract_flow_data(date, volume, speed, thickness, coatingposition, syringe, trial)
    elif stop == 'y':
        data = extract_flow_data_stop(date, volume, speed, thickness, coatingposition, syringe, trial)

    df = data[0]
    fig = plt.plot(df['time'], df['flow'], sns.xkcd_rgb["denim blue"], marker='.',
             linestyle='none')

    #plot max flow value and min flow value
    fig = plt.plot(data[4], data[5], 'ro')
    fig = plt.text(data[4], data[5] + 0.75, str(data[5]))
    fig = plt.plot(data[2], data[3], 'ro')
    fig = plt.text(data[2], data[3] - 0.75, str(data[3]))

    plt.xlabel('Time (sec)')
    plt.ylabel('Flow Rate (mL/min)')
    plt.title(volume + ' ' + syringe + ' syringe with ' + thickness + ' ' + coatingposition + ' ' + trial + ' trial ' + speed)

    plt.savefig(date + 'data/' + 'plot/' + 'flow' + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + syringe + '_' + 'syringe_' + trial + '_run_full.pdf')

    return plt.show()

def plot_force(date, volume, speed, thickness, coatingposition, syringe, trial):
    data = extract_force_data(date, volume, speed, thickness, coatingposition, syringe, trial)
    df = data[0]
    fig = plt.plot(df['travel'], df['load'], sns.xkcd_rgb["medium green"], marker='.',
             linestyle='none')

    #plot max flow value and min flow value
    fig = plt.plot(data[4], data[5], 'ro')
    fig = plt.text(data[4] + 0.75, data[5], str(data[5]))
    fig = plt.plot(data[2], data[3], 'ro')
    fig = plt.text(data[2] - 0.75, data[3], str(data[3]))

    plt.xlabel('Travel Distance (mm)')
    plt.ylabel('Load (N)')
    plt.title(volume + ' ' + syringe + ' syringe with ' + thickness + ' ' + coatingposition + ' ' + trial + ' trial ' + speed)
    plt.savefig(date + 'data/' + 'plot/' + 'force_travel' + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + syringe + '_' + 'syringe_' + trial + '_run_full.pdf')

    return plt.show()

def plot_flow_force(date, volume, speed, thickness, coatingposition, syringe, trial, stop):
    if stop == 'n':
        flow = extract_flow_data(date, volume, speed, thickness, coatingposition, syringe, trial)
    elif stop == 'y':
        flow = extract_flow_data_stop(date, volume, speed, thickness, coatingposition, syringe, trial)
    force = extract_force_data(date, volume, speed, thickness, coatingposition, trial, syringe)

    # Find maximum time
    time_max = max(flow[1], force[1])
    # Plot flow rate and force verse time
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    lns1 = ax1.plot(flow['time'], flow['flow'],  sns.xkcd_rgb["denim blue"], marker = '.', linestyle = 'none', label = 'flow rate')

    ax2 = ax1.twinx()
    lns2 = ax2.plot(force['time'], force['load'], sns.xkcd_rgb["medium green"], marker = '.', linestyle = 'none', label = 'force')

    # Make the legend together
    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc= "upper right")

    fig = ax1.plot(flow[4], flow[5], 'ro')
    fig = ax1.text(flow[4], flow[5] + 0.75, str(flow[5]))

    fig = ax1.plot(flow[2], flow[3], 'ro')
    fig = ax1.text(flow[2], flow[3] - 0.75, str(flow[3]))
    fig = ax2.plot(force[4], force[5], 'ro')
    fig = ax2.text(force[4] + 0.75, force[5], str(force[5]))

    fig = ax2.plot(force[2], force[3], 'ro')
    fig = ax2.text(force[2] - 0.75, force[3], str(force[3]))



    ax1.grid()
    ax1.set_xlabel("Time (sec)")
    ax1.set_ylabel("Flow rate (mL/min)")
    ax2.set_ylabel("Force (N)")
    axis_margin = 1
    ax2.set_ylim(force[3] - axis_margin, force[5] + axis_margin)
    ax1.set_ylim(flow[3] - axis_margin, flow[5] + axis_margin)
    ax1.set_xlim(-axis_margin, time_max + axis_margin)
    plt.title(volume + ' ' + syringe + ' syringe with ' + thickness + ' ' + coatingposition + ' ' + trial + ' trial ' + speed)

    plt.savefig(date + 'data/' + 'plot/' + 'both' + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + syringe + '_' + 'syringe_' + trial + '_run_full.pdf')


    return plt.show()

def compare_syringe(date, datatype, volume, speed, thickness, coatingposition, number):
    number = int(number)
    if datatype == 'flow':
        max_list = []
        min_list = []
        time_list = []
        name = ''
        for n in range(number):
            k = n + 1
            syringe = input('Syringe' + str(k) + ':' )
            trial = input('Which trial: ')
            stop = input('stop ? (y/n):')
            if stop == 'n':
                data = extract_flow_data(date, volume, speed, thickness, coatingposition, syringe, trial)
            elif stop == 'y':
                data = extract_flow_data_stop(date, volume, speed, thickness, coatingposition, syringe, trial)
            max_list.append(data[5])
            min_list.append(data[3])
            time_list.append(data[1])
            name += syringe
            name += 'syringe_'
            name += trial
            name += 'trial_'
            df = data[0]
            fig = plt.plot(df['time'], df['flow'], marker='.', linestyle='none', label = syringe + ' syringe_' + trial)
            fig = plt.plot(data[4], data[5], 'ro')
            fig = plt.text(data[4], data[5] + 0.75, str(data[5]))
            fig = plt.plot(data[2], data[3], 'ro')
            fig = plt.text(data[2], data[3] - 0.75, str(data[3]))
        plot_margin = 1
        plt.ylim(min(min_list) - plot_margin, max(max_list) + plot_margin)
        plt.xlim(-plot_margin, max(time_list)+ plot_margin)
        plt.xlabel('Time (sec)')
        plt.ylabel('Flow Rate (mL/min)')
        plt.legend(loc = 'upper right')
        plt.title('Flow rate for different syringes')
        plt.savefig(date + 'data/' + 'plot/' + 'compare_syringe' + '_' + datatype + '_' + date + '_' + name + volume + '_' + speed + '_' + thickness + '.pdf')
    elif datatype == 'force_travel':
        max_list = []
        min_list = []
        travel_list = []
        name = ''
        for n in range(number):
            k = n + 1
            syringe = input('Syringe' + str(k) + ':' )
            trial = input('Which trial: ')
            data = extract_force_data(date, volume, speed, thickness, coatingposition, syringe, trial)
            max_list.append(data[5])
            min_list.append(data[3])
            travel_list.append(data[6])
            name += syringe
            name += 'syringe_'
            name += trial
            name += 'trial_'
            df = data[0]
            fig = plt.plot(df['travel'], df['load'], marker='.', linestyle='none', label = syringe + ' syringe_' + trial)
            fig = plt.plot(data[4], data[5], 'ro')
            fig = plt.text(data[4] + 0.75, data[5], str(data[5]))
            fig = plt.plot(data[2], data[3], 'ro')
            fig = plt.text(data[2] - 0.75, data[3], str(data[3]))
        plot_margin = 1
        plt.ylim(min(min_list) - plot_margin, max(max_list) + plot_margin)
        plt.xlim(-plot_margin, max(travel_list)+ plot_margin)
        plt.xlabel('Travel Distance (mm)')
        plt.ylabel('Load (N)')
        plt.legend(loc = 'upper right')
        plt.title('Force for different syringes')
        plt.savefig(date + 'data/' + 'plot/' + 'compare_syringe' + '_' + datatype + '_' + date + '_' + name + volume + '_' + speed + '_' + thickness + '.pdf')
    else:
        print('wrong datatype')

    return plt.show()

def compare_thickness(date, datatype, volume, speed, number):
    number = int(number)
    if datatype == 'flow':
        max_list = []
        min_list = []
        time_list = []
        name = ''
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
            syringe = input('Syringe' + str(k) + ':' )
            trial = input('Which trial: ')
            stop = input('stop ? (y/n):')
            if stop == 'n':
                data = extract_flow_data(date, volume, speed, thickness, coatingposition, syringe, trial)
            elif stop == 'y':
                data = extract_flow_data_stop(date, volume, speed, thickness, coatingposition, syringe, trial)
            max_list.append(data[5])
            min_list.append(data[3])
            time_list.append(data[1])
            name += thickness
            name += '_'
            name += syringe
            name += 'syringe_'
            name += trial
            name += 'trial_'
            df = data[0]
            fig = plt.plot(df['time'], df['flow'], marker='.', linestyle='none', label = syringe + ' syringe_' + thickness + coatingposition + trial)
            fig = plt.plot(data[4], data[5], 'ro')
            fig = plt.text(data[4], data[5] + 0.75, str(data[5]))
            fig = plt.plot(data[2], data[3], 'ro')
            fig = plt.text(data[2], data[3] - 0.75, str(data[3]))
        plot_margin = 1
        plt.ylim(min(min_list) - plot_margin, max(max_list) + plot_margin)
        plt.xlim(-plot_margin, max(time_list)+ plot_margin)
        plt.xlabel('Time (sec)')
        plt.ylabel('Flow Rate (mL/min)')
        plt.legend(loc = 'upper right')
        plt.title(volume + ' syringe with different parylene thickness coating')
        plt.savefig(date + 'data/' + 'plot/' + 'compare_thickness' + '_' + datatype + '_' + date + '_' + name + volume + '_' + speed + '.pdf')
    elif datatype == 'force_travel':
        max_list = []
        min_list = []
        travel_list = []
        name = ''
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
            syringe = input('Syringe' + str(k) + ':' )
            trial = input('Which trial: ')
            data = extract_force_data(date, volume, speed, thickness, coatingposition, syringe, trial)
            max_list.append(data[5])
            min_list.append(data[3])
            travel_list.append(data[6])
            name += thickness
            name += '_'
            name += syringe
            name += 'syringe_'
            name += trial
            name += 'trial_'
            df = data[0]
            fig = plt.plot(df['travel'], df['load'], marker='.', linestyle='none', label = syringe + ' syringe_' + thickness + coatingposition + trial)
            fig = plt.plot(data[4], data[5], 'ro')
            fig = plt.text(data[4] + 0.75, data[5], str(data[5]))
            fig = plt.plot(data[2], data[3], 'ro')
            fig = plt.text(data[2] - 0.75, data[3], str(data[3]))
        plot_margin = 1
        plt.ylim(min(min_list) - plot_margin, max(max_list) + plot_margin)
        plt.xlim(-plot_margin, max(travel_list)+ plot_margin)
        plt.xlabel('Travel Distance (mm)')
        plt.ylabel('Load (N)')
        plt.legend(loc = 'upper right')
        plt.title(volume + ' syringe with different parylene thickness coating')
        plt.savefig(date + 'data/' + 'plot/' + 'compare_thickness' + '_' + datatype + '_' + date + '_' + name + volume + '_' + speed + '.pdf')
    else:
        print('wrong datatype')

    return plt.show()

def compare_syringe_date(datatype, volume, speed, thickness, coatingposition, number):
    number = int(number)
    if datatype == 'flow':
        max_list = []
        min_list = []
        time_list = []
        name = ''
        for n in range(number):
            k = n + 1
            date = input ('date:')
            syringe = input('Syringe' + str(k) + ':' )
            trial = input('Which trial: ')
            stop = input('stop ? (y/n):')
            if stop == 'n':
                data = extract_flow_data(date, volume, speed, thickness, coatingposition, syringe, trial)
            elif stop == 'y':
                data = extract_flow_data_stop(date, volume, speed, thickness, coatingposition, syringe, trial)
            max_list.append(data[5])
            min_list.append(data[3])
            time_list.append(data[1])
            name += syringe
            name += 'syringe_'
            name += trial
            name += 'trial_'
            df = data[0]
            fig = plt.plot(df['time'], df['flow'], marker='.', linestyle='none', label = syringe + ' syringe_' + trial)
            fig = plt.plot(data[4], data[5], 'ro')
            fig = plt.text(data[4], data[5] + 0.75, str(data[5]))
            fig = plt.plot(data[2], data[3], 'ro')
            fig = plt.text(data[2], data[3] - 0.75, str(data[3]))
        plot_margin = 1
        plt.ylim(min(min_list) - plot_margin, max(max_list) + plot_margin)
        plt.xlim(-plot_margin, max(time_list)+ plot_margin)
        plt.xlabel('Time (sec)')
        plt.ylabel('Flow Rate (mL/min)')
        plt.legend(loc = 'upper right')
        plt.title('Flow rate for different syringes')
        plt.savefig(date + 'data/' + 'plot/' + 'compare_syringe' + '_' + datatype + '_' + date + '_' + name + volume + '_' + speed + '_' + thickness + '.pdf')
    elif datatype == 'force_travel':
        max_list = []
        min_list = []
        travel_list = []
        name = ''
        for n in range(number):
            k = n + 1
            date = input ('date:')
            syringe = input('Syringe' + str(k) + ':' )
            trial = input('Which trial: ')
            data = extract_force_data(date, volume, speed, thickness, coatingposition, syringe, trial)
            max_list.append(data[5])
            min_list.append(data[3])
            travel_list.append(data[6])
            name += syringe
            name += 'syringe_'
            name += trial
            name += 'trial_'
            df = data[0]
            fig = plt.plot(df['travel'], df['load'], marker='.', linestyle='none', label = syringe + ' syringe_' + trial)
            fig = plt.plot(data[4], data[5], 'ro')
            fig = plt.text(data[4] + 0.75, data[5], str(data[5]))
            fig = plt.plot(data[2], data[3], 'ro')
            fig = plt.text(data[2] - 0.75, data[3], str(data[3]))
        plot_margin = 1
        plt.ylim(min(min_list) - plot_margin, max(max_list) + plot_margin)
        plt.xlim(-plot_margin, max(travel_list)+ plot_margin)
        plt.xlabel('Travel Distance (mm)')
        plt.ylabel('Load (N)')
        plt.legend(loc = 'upper right')
        plt.title('Force for different syringes')
        plt.savefig(date + 'data/' + 'plot/' + 'compare_syringe' + '_' + datatype + '_' + date + '_' + name + volume + '_' + speed + '_' + thickness + '.pdf')
    else:
        print('wrong datatype')
    return plt.show()
