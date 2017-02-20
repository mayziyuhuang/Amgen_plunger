import numpy as np
# Pandas, conventionally imported as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

def plot_force(date, datatype, volume, speed, thickness, coatingposition, trial):

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

    # Find the index of the row with largest load value
    max_force_index = force_time0['load'].idxmax()
    # Find the maximum force
    max_force = force_time0.loc[max_force_index, 'load']

    fig = plt.plot(force_time0['travel'], force_time0['load'], sns.xkcd_rgb["medium green"], marker='.',
             linestyle='none')
    plt.xlabel('Travel Distance (mm)')
    plt.ylabel('Load (N)')
    plt.title(volume + ' syringe with ' + thickness + ' ' + coatingposition + ' ' + trial + ' trial')

    #plt.show()

    return fig

#date = '20170217'
#datatype = 'force_travel'
#volume = '3ml'
#speed = '70mm-min'
#thickness = '1.9umPAC'
#coatingposition = 'onlyplungercoat_'
#trial = '3rd'

#plot_force(date, datatype, volume, speed, thickness, coatingposition, trial)

#plt.savefig(date + 'data/' + 'plot/' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + trial + '.pdf')
#plt.show()
