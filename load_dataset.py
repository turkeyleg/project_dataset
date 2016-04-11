import pandas as pd
import numpy as np
import os
import datetime as dt
import sqlite3
from zip_code_calc import ZipCodesUtil
import itertools


class DataGetter:
    def __init__(self, dataPath = None):
        self._dateparse = lambda dt : pd.datetime.strptime(dt, '%Y%m')
        self._dataPath = dataPath or r'C:\Users\jylkka_a\Downloads'
        self._state_codes = list(pd.read_csv('states.csv').Abbreviation)

    def getOrigData(self, year=2005, sample=True, rows= -1, db=True):
        path = os.path.join(self._dataPath, 'sample_orig_%d.txt' %(year))
        df = pd.read_csv(path, sep='|',
                         header=None,
                         index_col=False,
                         na_values = ['   ', '  '],
                         parse_dates=['first_paym_dt','maturity_dt'],
                         engine='c',
                         date_parser = self._dateparse,
                         names=['credit_score', 'first_paym_dt',
                                'first_time_hb_flag', 'maturity_dt',
                                'msa', 'mortg_ins_pct', 'nbr_units',
                                'occupancy_status', 'combined_loan2value',
                                'dti_ratio', 'upb', 'loan2value', 'interest_rate',
                                'channel', 'ppm_flag', 'product_type', 'property_state',
                                'property_type', 'postal_code', 'loan_sequence_number',
                                'loan_purpose', 'original_loan_term', 'numb_borrowers',
                                'seller_name', 'servicer_name'
                                 ],

                         # don't need servicer name, not useful
                         # product type is always FRM (fixed rate mortgage) on this dataset


                         usecols = ['credit_score', 'first_paym_dt',
                                    'first_time_hb_flag', 'maturity_dt',
                                    'msa', 'mortg_ins_pct', 'nbr_units',
                                    'occupancy_status', 'combined_loan2value',
                                    'dti_ratio', 'upb', 'loan2value', 'interest_rate',
                                    'channel', 'ppm_flag', 'property_state',
                                    'property_type', 'postal_code', 'loan_sequence_number',
                                    'loan_purpose', 'original_loan_term', 'numb_borrowers',
                                    'seller_name'
                                     ]


                                   # ['credit_score', 'first_paym_dt',
                                   #  'first_time_hb_flag', 'maturity_dt',
                                   #  'msa', 'mortg_ins_pct', 'nbr_units',
                                   #  'occupancy_status', 'combined_loan2value',
                                   #  'dti_ratio', 'upb', 'loan2value', 'interest_rate',
                                   #  'channel', 'ppm_flag', 'product_type', 'property_state',
                                   #  'property_type', 'postal_code', 'loan_sequence_number',
                                   #  'loan_purpose', 'original_loan_term', 'numb_borrowers',
                                   #  'seller_name', 'servicer_name'
                                   #   ]

                         )

        # df['first_time_hb_flag'] = df['first_time_hb_flag'].astype('category', categories=['Y','N'])
        # df['nbr_units'] = df['nbr_units'].astype('category', categories=[1, 2, 3, 4])
        # df['numb_borrowers'] = df['numb_borrowers'].astype('category', categories=[1, 2])
        # df['occupancy_status'] = df['occupancy_status'].astype('category', categories=['O','S','I'])
        # df['channel'] = df['channel'].astype('category', categories=['T','R','B','C'])
        # df['ppm_flag'] = df['ppm_flag'].astype('category', categories=['Y','N'])
        # df['loan_purpose'] = df['loan_purpose'].astype('category', categories=['P','C','N'])
        # df['property_state'] = df['property_state'].astype('category', categories=self._state_codes)
        # df['property_type'] = df['property_type'].astype('category', categories=['CO','LH','PU',
        #                                                                          'MH','SF','CP'])













        df.set_index('loan_sequence_number', inplace=True)

        return df

    def getSvcgData(self, year=2005, sample=True, rows = -1):
        path = os.path.join(self._dataPath, 'sample_svcg_%d.txt' %(year))
        df = pd.read_csv(path, sep='|', header=None, index_col=False,
                                 engine='c',
                                 low_memory=False,
                                 na_values=['   ', '      ',''],
                                 verbose=True,

                                 names=['loan_sequence_number', 'monthly_reporting_period', 'current_actual_upb',
                                        'current_loan_delinq_status', 'loan_age', 'remaining_months2maturity',
                                        'repurchase_flag', 'modification_flag','zero_balance_code','zero_balance_eff_dt',
                                        'current_interest_rate', 'current_deferred_upb', 'ddlpi', 'mi_recoveries',
                                        'net_sales_proceeds','non_mi_recoveries','expenses'],
                                 usecols = ['loan_sequence_number', 'monthly_reporting_period', 'current_actual_upb',
                                            'current_loan_delinq_status', 'loan_age', 'remaining_months2maturity',
                                            'zero_balance_eff_dt', 'ddlpi', 'current_deferred_upb'
                                            ],
                                 dtype = {'current_actual_upb':float, 'loan_age':np.int,
                                         'current_loan_delinq_status':str, 'current_deferred_upb':float,
                                         'remaining_months2maturity':np.int, 'zero_balance_eff_dt':str}
                                 ,converters={'zero_balance_eff_dt':lambda zbed: zbed.strip()}

                                 )



        for col in ('monthly_reporting_period', 'zero_balance_eff_dt', 'ddlpi'):
            try:
                #print col
                df[col] = pd.to_datetime(df[col], format='%Y%m', errors='coerce'
                                         #,utc=False
                                         )
            except Exception as e:
                print e
                pass
        #print 'set index'
        #df['monthly_reporting_period'] = df['monthly_reporting_period'].dt.to_period('M')
        df.set_index(['loan_sequence_number', 'monthly_reporting_period'], inplace=True)
        # for col in ('current_loan_delinq_status', 'repurchase_flag', 'modification_flag', 'zero_balance_code',
        #             'net_sales_proceeds'):#     df[col] = df[col].astype('category')

        return df

    def getDataset(self, year_range=[2000,2002]):
        print 'Getting origination data ...'
        svcgData = pd.concat([self.getSvcgData(year) for year in range(*year_range)], copy=False)
        print 'Getting servicing data ...'
        origData = pd.concat([self.getOrigData(year) for year in range(*year_range)], copy=False)
        print 'Merging origination and servicing data ...'
        merged = pd.merge(origData, svcgData, left_index=True, right_index=True)

        # only convert this column to category once you have all the values
        merged['current_loan_delinq_status'] = merged['current_loan_delinq_status'].astype('category')
        merged['seller_name'] = merged['seller_name'].astype('category')

        merged['first_time_hb_flag'] = merged['first_time_hb_flag'].astype('category', categories=['Y','N'])
        merged['nbr_units'] = merged['nbr_units'].astype('category', categories=[1, 2, 3, 4])
        merged['numb_borrowers'] = merged['numb_borrowers'].astype('category', categories=[1, 2])
        merged['occupancy_status'] = merged['occupancy_status'].astype('category', categories=['O','S','I'])
        merged['channel'] = merged['channel'].astype('category', categories=['T','R','B','C'])
        merged['ppm_flag'] = merged['ppm_flag'].astype('category', categories=['Y','N'])
        merged['loan_purpose'] = merged['loan_purpose'].astype('category', categories=['P','C','N'])
        merged['property_state'] = merged['property_state'].astype('category', categories=self._state_codes)
        merged['property_type'] = merged['property_type'].astype('category', categories=['CO','LH','PU',
                                                                                         'MH','SF','CP'])

        print 'Done merging'
        print merged.info(memory_usage='deep')
        return merged



db = False
#con = sqlite3.connect('dataset.db')

if db:
    print 'getting origination data ...'
    origData = pd.concat(dg.getOrigData(year) for year in range(2000,2003))
    origData = origData.sample(frac=.5)


    try:
        origData.to_sql('orig', con)
        con.commit()
    except Exception as e:
        print e

#print 'getting servicing data ...'

if db:
    try:
        for year in range(2000,2003):
            print 'getting svcg data for year %d' %(year)
            svcData = dg.getSvcgData(year)
            print 'inserting into db for year %d' %(year)
            svcData.to_sql('svcg', con, if_exists='append')
            con.commit()
            del svcData
    except Exception as e:
        print e



q = '''
        select * from orig join svcg on orig.loan_sequence_number = svcg.loan_sequence_number
    '''


#print merged.zero_balance_eff_dt.unique()

