import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

def extract_flow_data(date, datatype, volume, speed, thickness, coatingposition, syringe, trial):
    file_name = date + 'data/' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + syringe + '_' + 'syringe_' + trial + '_run_full.xls'
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

def extract_force_data(date, datatype, volume, speed, thickness, coatingposition, syringe, trial):
    file_name = date + 'data/' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + syringe + '_' + 'syringe_' + trial + '_run_full.xlsx'
    excel_file = pd.ExcelFile(file_name)
    df = excel_file.parse('Sheet4')

    df.columns = ['reading', 'load', 'travel', 'time']
    df.loc[:, 'travel'] *= -1

    df_time_less0 = df[df['travel'] <= 0]
    length = len(df_time_less0.index)
    df_time0 = df.iloc[length-1:]

    max_travel_index = df_time0['travel'].idxmax()
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

    return data, maxtime, min_x, min_y, max_x, max_y


def plot_flow(date, datatype, volume, speed, thickness, coatingposition, syringe, trial):
    data = extract_flow_data(date, datatype, volume, speed, thickness, coatingposition, syringe, trial)
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

    plt.savefig(date + 'data/' + 'plot/' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + syringe + '_' + 'syringe_' + trial + '_run_full.pdf')

    return plt.show()

def plot_flow(date, datatype, volume, speed, thickness, coatingposition, syringe, trial):
    data = extract_force_data(date, datatype, volume, speed, thickness, coatingposition, syringe, trial)
    df = data[0]
    fig = plt.plot(df['travel'], df['load'], sns.xkcd_rgb["medium green"], marker='.',
             linestyle='none')

    #plot max flow value and min flow value
    fig = plt.plot(data[4], data[5], 'ro')
    fig = plt.text(data[4], data[5] + 0.75, str(data[5]))
    fig = plt.plot(data[2], data[3], 'ro')
    fig = plt.text(data[2], data[3] - 0.75, str(data[3]))

    plt.xlabel('Travel Distance (mm)')
    plt.ylabel('Load (N)')
    plt.title(volume + ' ' + syringe + ' syringe with ' + thickness + ' ' + coatingposition + ' ' + trial + ' trial ' + speed)
    plt.savefig(date + 'data/' + 'plot/' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + syringe + '_' + 'syringe_' + trial + '_run_full.pdf')

    return plt.show()
