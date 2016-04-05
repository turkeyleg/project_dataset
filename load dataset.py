import pandas as pd
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
                                 names=['loan_sequence_number', 'monthly_reporting_period', 'current_actual_upb',
                                        'current_loan_delinq_status', 'loan_age', 'remaining_months2maturity',
                                        'repurchase_flag', 'modification_flag','zero_balance_code','zero_balance_eff_dt',
                                        'current_interest_rate', 'current_deferred_upb', 'ddlpi', 'mi_recoveries',
                                        'net_sales_proceeds','non_mi_recoveries','expenses']

                                 )
        try:
            for col in ('monthly_reporting_period', 'zero_balance_eff_dt'):
                print col
                df[col] = pd.to_datetime(df[col], format='%Y%m')
        except:
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

print 'getting origination data ...'
origData = pd.concat(dg.getOrigData(year) for year in range(2000,2003))

con = sqlite3.connect('dataset.db')
try:
    origData.to_sql('orig', con)
    con.commit()
except Exception as e:
    print e

#print 'getting servicing data ...'
db = False
if db:
    try:
        for year in range(2000,2003):
            print 'getting svcg data for year %d' %(year)
            svcData = dg.getSvcgData(year)
            print 'inserting into db for year %d' %(year)
            svcData.to_sql('svcg', con, if_exists='append')
            con.commit()
    except Exception as e:
        print e

print 'done'

# print 'setting indices ...'
# origData.index = origData['loan_sequence_number']
# svcData.index = svcData['loan_sequence_number']

#print 'merging ...'
#df = pd.merge(origData, svcData, on='loan_sequence_number')

