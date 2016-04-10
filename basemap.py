import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex


# make a mapping between state codes and state names

state_df = pd.read_csv('states.csv')
state_dict = dict(zip(state_df['State'], state_df['Abbreviation']))


# http://stackoverflow.com/questions/7586384/color-states-with-pythons-matplotlib-basemap
# https://github.com/matplotlib/basemap/blob/master/examples/fillstates.py
map = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

map.readshapefile('st99_d00', name='states', drawbounds=True)

data = pd.DataFrame({'states':['Vermont','Missouri','Colorado'], 'numbers':[.5,.9,.2]})
data_dict = dict(zip(data['states'], data['numbers']))
#data_dict2 = {key: data_dict[state_dict[key]] for key in data_dict.keys()}

colors = {}
statenames = []
cmap = plt.cm.hot
vmin, vmax = 0., 1.
for shapedict in map.states_info:
    statename = shapedict['NAME']
    if statename not in data_dict.keys():
        continue
    else:
        datum = data_dict[statename]
    colors[statename] = cmap(1.-np.sqrt((datum-vmin)/(vmax-vmin)))[:3]
    statenames.append(statename)







ax = plt.gca()
# for nshape, seg in enumerate(map.states):
#     try:
#         color = rgb2hex(colors[statenames[nshape]])
#         color = 'red'
#         poly = Polygon(seg, facecolor=color, edgecolor=color)
#         print color
#         print seg
#         print statenames[nshape]
#         ax.add_patch(poly)
#         print 'nailed it'
#     except Exception as e:
#         #print e, color, nshape
#         pass

# state_names = [shape_dict['NAME'] for shape_dict in map.states_info]
#
# for state in colors.keys():
#     seg = map.states[state_names.index(state)]
#     color = 'red'
#     color = rgb2hex(colors[state])
#     poly = Polygon(seg, facecolor=color, edgecolor=color)
#     ax.add_patch(poly)



smiley_states = ['Wyoming','Iowa','Nevada','Arizona','New Mexico','Texas','Louisiana','Mississippi','Alabama',
                 'Tennessee']

state_names = [shape_dict['NAME'] for shape_dict in map.states_info]

for state in smiley_states:
    seg = map.states[state_names.index(state)]
    color = 'blue' if state in ('Wyoming','Iowa') else 'red'
    #color = rgb2hex(colors[state])
    poly = Polygon(seg, facecolor=color, edgecolor=color)
    ax.add_patch(poly)





# seg = map.states[state_names.index('Colorado')]
# print seg
#
# poly = Polygon(seg, facecolor='red',edgecolor='red')
# ax.add_patch(poly)
'nailed it?'
plt.show()



