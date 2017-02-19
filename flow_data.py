import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Read in flow rate data files with Pandas
flow_data = pd.read_csv('20170217data/flow_20170217_3ml_70mm-min_0um_2nd.csv')
flow_data.columns = ['sample', 'time', 'flow']

# The flow sensor can sense the flow in two direction
# Make the flow rate to be positive
flow_data.loc[:,'flow'] *= -1

plt.plot(flow_data['time'], flow_data['flow'], marker='.',
         linestyle='none')
plt.xlabel('relative time (sec)')
plt.ylabel('flow rate (mL/min)')
plt.show()

#testing
#testing2

#git clone URL
#git status
#after making changes
#git add *
#git commit -m "message"
#git status
#git push

#git status
#git pull
