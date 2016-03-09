import pandas as pd
import os
import datetime as dt
from zip_code_calc import ZipCodesUtil
import itertools


class DataGetter:
    def __init__(self, dataPath = None):
        self._dateparse = lambda dt : pd.datetime.strptime(dt, '%Y%m')
        self._dataPath = dataPath or r'C:\Users\jylkka_a\Downloads'

    def getOrigData(self, year=2005, sample=True, rows= -1):
        path = os.path.join(self._dataPath, 'sample_orig_%d.txt' %(year))
        df = pd.read_csv(path, sep='|', #headers=None,
                         #index_col = 'loan_sequence_number',
                         header=None,
                         index_col=False,
                         parse_dates=['first_paym_dt','maturity_dt'],
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



        df.index_col = 'loan_sequence_number'

        return df

    def getSvcgData(self, year=2005, sample=True, rows = -1):
        path = os.path.join(self._dataPath, 'sample_svcg_%d.txt' %(year))
        df = pd.read_csv(monthly_path, sep='|', header=None, index_col=False,
                                 #parse_dates=['monthly_reporting_period','zero_balance_eff_dt','ddlpi'],
                                 date_parser=self._dateparse,
                                 low_memory=False,
                                 #dtype={'monthly_reporting_period':pd.datetime, 'current_actual_upb':float,
                                       # 'zero_balance_eff_dt':pd.datetime, 'ddlpi':pd.datetime,
                                 #       'remaining_months2maturity':int},
                                 names=['loan_sequence_number', 'monthly_reporting_period', 'current_actual_upb',
                                        'current_loan_delinq_status', 'loan_age', 'remaining_months2maturity',
                                        'repurchase_flag', 'modification_flag','zero_balance_code','zero_balance_eff_dt',
                                        'current_interest_rate', 'current_deferred_upb', 'ddlpi', 'mi_recoveries',
                                        'net_sales_proceeds','non_mi_recoveries','expenses']

                                 )

        for col in ('current_loan_delinq_status', 'repurchase_flag', 'modification_flag', 'zero_balance_code',
                    'net_sales_proceeds'):
            df[col] = df[col].astype('category')

        return df





# frames = [get_frame(date) for date in dates]
# df = pd.concat(frames, axis=1)
