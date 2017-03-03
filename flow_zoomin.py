import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

def extract_flow_data(date, volume, speed, thickness, coatingposition, syringe, trial):
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


def plot_flow_zoomin(date, volume, speed, thickness, coatingposition, syringe, trial, stop, zoomin):
    if stop == 'n':
        data = extract_flow_data(date, volume, speed, thickness, coatingposition, syringe, trial)
    elif stop == 'y':
        data = extract_flow_data_stop(date, volume, speed, thickness, coatingposition, syringe, trial)

    df = data[0]

    zoomin = input('zoom in range:')
    zoomin = float(zoomin)

    df = df[df.time < zoomin]


    max_flow_index = df['flow'].idxmax()
    max_y = df.loc[max_flow_index, 'flow']
    max_x = df.loc[max_flow_index, 'time']
    min_flow_index = df['flow'].idxmin()
    min_y = df.loc[min_flow_index, 'flow']
    min_x = df.loc[min_flow_index, 'time']


    fig = plt.plot(df['time'], df['flow'], sns.xkcd_rgb["denim blue"], marker='.',
             linestyle='none')

    #plot max flow value and min flow value
    fig = plt.plot(max_x, max_y, 'ro')
    fig = plt.text(max_x, max_y + 0.75, str(data[5]))
    fig = plt.plot(min_x, min_y, 'ro')
    fig = plt.text(min_x, min_y - 0.75, str(data[3]))

    plt.xlabel('Time (sec)')
    plt.ylabel('Flow Rate (mL/min)')
    plt.title(volume + ' ' + syringe + ' syringe with ' + thickness + ' ' + coatingposition + ' ' + trial + ' trial ' + speed)

    #plt.savefig(date + 'data/' + 'plot/' + 'flow' + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + syringe + '_' + 'syringe_' + trial + '_run_full.pdf')

    return plt.show()
