import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

import functions_2nd as fun

plot_type = input ('Plot type: \n1. compare first trial of different syringe \n2. compare same syringe differetn trials \n3. compare same syringe non-stop and stop trials \n4. compare different thickness \n5. plot flow rate and load for same syringe same trial \n6. plot flow rate for one trial \n7. plot load for one trial: \n')

if plot_type == '5' or '6' or '7':
    if plot_type == '5':
        datatype = both
    elif plot_type == '6':
        datatype = flow
    elif plot_type == '7':
        datatype = force_travel
    else:
        print('wrong datatype')

    date = input('Date in yyyymmdd:')
    volume = input('Volume of the syringe (3ml, 5ml):')
    speed = input('Speed of the test stand (70mm-min):')
    thickness = input('Thickness of the parylene and type (1.9umPAC):')
    if thickness == '0um':
        coatingposition = ''
    else:
        where = input('Coating position is onlyplungercoat (y/n):')
        if where == 'y':
            coatingposition = 'onlyplungercoat_'
        else:
            print('wrong')
    syringe = input('Which syringe (1st, 2nd, 3rd, 4th, 5th):')
    trial = input('Trial (1st, 2nd, 3rd):')

    fun.save_plot(date, datatype, volume, speed, thickness, coatingposition, trial, syringe)

elif plot_type == '1':
    number = input('Number of the data you want to compare (2):')
    date = input('Date in yyyymmdd (20170217):')
    datatype = input('Datatype (flow, force_travel):')
    volume = input('Volume of the syringe (3ml, 5ml):')
    speed = input('Speed of the test stand (70mm-min):')
    thickness = input('Thickness of the parylene and type (1.9umPAC):')
    if thickness == '0um':
        coatingposition = ''
    else:
        where = input('Coating position is onlyplungercoat (y/n):')
        if where == 'y':
            coatingposition = 'onlyplungercoat_'
        else:
            print('wrong')
    trial = '1st'
    fun.compare_syringe(date, datatype, volume, speed, thickness, coatingposition, number)

elif plot_type == '4':
    number = input('Number of the data you want to compare (2):')
    date = input('Date in yyyymmdd (20170217):')
    datatype = input('Datatype (flow, force_travel):')
    volume = input('Volume of the syringe (3ml, 5ml):')
    speed = input('Speed of the test stand (70mm-min):')

    fun.compare_thickness(date, datatype, volume, speed, number)

#elif plot_type == '2' or '4':



else:
    print('wrong')
