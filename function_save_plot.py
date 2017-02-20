import numpy as np
# Pandas, conventionally imported as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)
import function_plot_flow
import function_plot_force

def save_plot(date, datatype, volume, speed, thickness, coatingposition, trial):

    if datatype == 'flow':
        function_plot_flow.plot_flow(date, datatype, volume, speed, thickness, coatingposition, trial)
    elif datatype == 'force_travel':
        function_plot_force.plot_force(date, datatype, volume, speed, thickness, coatingposition, trial)
    else:
        print('Wrong datatype')

    plt.savefig(date + 'data/' + 'plot/' + datatype + '_' + date + '_' + volume + '_' + speed + '_' + thickness + '_' + coatingposition + '_' + trial + '.pdf')
    plt.show()

    return None


#date = '20170217'
#datatype = 'force_travel'
#volume = '3ml'
#speed = '70mm-min'
#thickness = '1.9umPAC'
#coatingposition = 'onlyplungercoat_'
#trial = '3rd'
