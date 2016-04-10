from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex


class DataMapper:
    def __init__(self, data, map_key, map_value, show_plot=True, save_plot=False, plot_name=None):
        self.data = data
        self.map_key = map_key
        self.map_value = map_value
        self.show_plot = show_plot
        self.save_plot = save_plot
        self.plot_name = plot_name
        self.state_colors = {}

        # map state abbreviations to state names
        state_df = pd.read_csv('states.csv')
        self.state_codes = dict(zip(state_df['Abbreviation'], state_df['State']))

        # http://stackoverflow.com/questions/7586384/color-states-with-pythons-matplotlib-basemap
        # https://github.com/matplotlib/basemap/blob/master/examples/fillstates.py
        self.map = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

        self.map.readshapefile('st99_d00', name='states', drawbounds=True)

    def plot(self):
        state_values = dict(zip(self.data[self.map_key], self.data[self.map_value]))
        state_names = [shape_dict['NAME'] for shape_dict in self.map.states_info]

        v_min, v_max = 0., 1.
        cmap = plt.cm.hot
        ax = plt.gca()

        for state_code, value in state_values.iteritems():
            if state_code not in self.state_codes:
                continue
            state_name = self.state_codes[state_code]
            #seg = self.map.states[state_names.index(state_name)]

            # calculate state's color on heatmap based on the value
            color_rgb = cmap(1. - np.sqrt((value - v_min)/(v_max - v_min)))[:3]
            color_hex = rgb2hex(color_rgb)

            # get the shape from shape file
            state_shape = self.map.states[state_names.index(state_name)]


            # create polygon based on shape and color, add it to plot
            poly = Polygon(state_shape, facecolor=color_hex, edgecolor=color_hex)
            ax.add_patch(poly)

        plt.title('Default rates in' + self.plot_name)
        plt.legend()

        if self.save_plot:
            plt.savefig(self.plot_name or 'plot name')

        if self.show_plot:
            plt.show()



test = False
if test:
    test_df = pd.DataFrame({'states':['IA','MA','CA'], 'data':[.4,.8,.9]})
    dm = DataMapper(data=test_df, map_key='states', map_value='data')
    dm.plot()

from load_dataset import DataGetter
from transform_data import calc_first_delinq
dg = DataGetter()
df = dg.getDataset()
calc_first_delinq(df)


def calc_default_rates_by_state_and_year(df):
    df.reset_index(inplace=True)
    df['monthly_reporting_period_year'] = df['monthly_reporting_period'].dt.year
    # make boolean column indicating whether the loan's first delinquency occurs this year
    df['first_delinq_this_year'] = (df['first_delinquency'].dt.year == df['monthly_reporting_period_year'])
    gb = df.groupby(['monthly_reporting_period_year', 'property_state', 'loan_sequence_number'])
    # first delinquency this year field should be the same for all loan/year combinations
    assert ((gb['first_delinq_this_year'].all()) | (~ gb['first_delinq_this_year'].any())).all()
    df_loan_state_year = gb['first_delinq_this_year'].first()

    # roll up loans to year & state
    gb_year_state = df_loan_state_year.groupby(level=['monthly_reporting_period_year', 'property_state'])
    default_rates_year_state = gb_year_state.sum() / gb_year_state.count()

    return default_rates_year_state


dr = calc_default_rates_by_state_and_year(df)

for yr in range(2000, 2009):
    #yr = 2008
    dr_yr = pd.DataFrame({dr[yr].index.name: dr[yr].index, 'default_rates': dr[yr]})
    dm = DataMapper(data=dr_yr, map_key='property_state', map_value='default_rates', save_plot=True, plot_name=str(yr))
    try:
        dm.plot()
    except Exception as e:
        print e
        pass




