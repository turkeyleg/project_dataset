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

    def getOrigData(self, year=2005, sample=True, rows= -1, db=True):
        path = os.path.join(self._dataPath, 'sample_orig_%d.txt' %(year))
        df = pd.read_csv(path, sep='|',
                         header=None,
                         index_col=False,
                         parse_dates=['first_paym_dt','maturity_dt'],
                         engine='c',
                         dtype= {'postal_code':str},
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
                                                             ]

                         )





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

        print df.zero_balance_eff_dt.dtype

        for col in ('monthly_reporting_period', 'zero_balance_eff_dt', 'ddlpi'):
            try:
                print col
                df[col] = pd.to_datetime(df[col], format='%Y%m', errors='coerce'
                                         #,utc=False
                                         )
            except Exception as e:
                print e
                pass
        print 'set index'
        df.set_index(['loan_sequence_number', 'monthly_reporting_period'], inplace=True)
        # for col in ('current_loan_delinq_status', 'repurchase_flag', 'modification_flag', 'zero_balance_code',
        #             'net_sales_proceeds'):#     df[col] = df[col].astype('category')

        return df

# home
# dataPath = r'C:\Users\aaron\Downloads'

# work
dataPath = r'C:\Users\jylkka_a\Downloads'


print dt.datetime.now()
dg = DataGetter(dataPath = dataPath)

db = False
con = sqlite3.connect('dataset.db')

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

print 'trying to get sql'
#df = pd.concat(result for result in pd.read_sql(q, con, chunksize=10000))
print 'done'
# print 'setting indices ...'
# origData.index = origData['loan_sequence_number']
# svcData.index = svcData['loan_sequence_number']

#print 'merging ...'
#df = pd.merge(origData, svcData, on='loan_sequence_number')

svcgData = pd.concat([dg.getSvcgData(year) for year in range(2000,2002)], copy=False)
origData = pd.concat([dg.getOrigData(year) for year in range(2000,2002)], copy=False)
merged = pd.merge(origData, svcgData, left_index=True, right_index=True)
print 'done merging'
#print merged.zero_balance_eff_dt.unique()

is_delinq = lambda x: (x not in ('0', 'XX', 'R'))
merged['is_delinquent'] = merged['current_loan_delinq_status'].apply(is_delinq)

gb = merged.groupby(level=0)
# should return a series, for each loan give the index of the first thing that's delinquent
get_first_delinq = lambda x: x.idxmax() if x.any() else None
gb.is_delinquent.apply(get_first_delinq)
#gb['is_delinquent'].idxmax() if gb['is_delinquent'].any() else None


# returns row of first default
# merged.loc[merged['is_defaulted'].idxmax()]

# pd.isnull(merged.zero_balance_eff_dt.unique()[0])