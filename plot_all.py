import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

import function_all as func

plot_type = input ('Plot type: \n1. compare different syringe and/or trial \n2. compare same syringe non-stop and stop trials \n3. compare different thickness \n4. plot flow rate and load for same syringe same trial \n5. plot flow rate for one trial \n6. plot load for one trial: \n9. plot syringe different date, trial: \n')

if plot_type == '4':
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
    stop = input('stop ? (y/n):')
    func.plot_flow_force(date, volume, speed, thickness, coatingposition, syringe, trial, stop)

elif plot_type == '5':
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
    stop = input('stop ? (y/n):')
    func.plot_flow(date, volume, speed, thickness, coatingposition, syringe, trial, stop)

elif plot_type == '6':
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
    func.plot_force(date, volume, speed, thickness, coatingposition, syringe, trial)

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
    func.compare_syringe(date, datatype, volume, speed, thickness, coatingposition, number)

elif plot_type == '3':
    number = input('Number of the data you want to compare (2):')
    date = input('Date in yyyymmdd (20170217):')
    datatype = input('Datatype (flow, force_travel):')
    volume = input('Volume of the syringe (3ml, 5ml):')
    speed = input('Speed of the test stand (70mm-min):')

    func.compare_thickness(date, datatype, volume, speed, number)

elif plot_type == '9':
    number = input('Number of the data you want to compare (2):')
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
    func.compare_syringe_date(datatype, volume, speed, thickness, coatingposition, number)
