import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Read in flow rate data files with Pandas
flow_data = pd.read_csv('flow_20170217_3ml_70mm-min_0um_2nd.csv')
flow_data.columns = ['sample', 'time', 'flow']

flow_data.loc[:,'flow'] *= -1

plt.plot(flow_data['time'], flow_data['flow'], marker='.',
         linestyle='none')
plt.xlabel('relative time (sec)')
plt.ylabel('flow rate (mL/min)')
plt.show()

#testing
#testing2
