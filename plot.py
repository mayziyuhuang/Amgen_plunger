import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

import functions_2nd as fun


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
        where = input('Coating position is onlyplungercoat (y/n):')
        if where == 'y':
            coatingposition = 'onlyplungercoat_'
        else:
            print('wrong')
    trial = input('Trial (1st, 2nd, 3rd):')

    fun.save_plot(date, datatype, volume, speed, thickness, coatingposition, trial)

elif compare == 'y':
    date = input('Date in yyyymmdd (20170217):')
    datatype = input('Datatype (flow, force_travel):')
    volume = input('Volume of the syringe (3ml, 5ml):')
    speed = input('Speed of the test stand (70mm-min):')
    number = input('Number of the data you want to compare (2):')

    fun.compare_data(date, datatype, volume, speed, number)

else:
    print('wrong')
