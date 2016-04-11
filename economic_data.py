import Quandl
import pandas as pd

# https://www.quandl.com/data/FRED/ALSTHPI-All-Transactions-House-Price-Index-for-Alabama
def get_house_price_index_by_state(state_code, from_quandl=True):
    if from_quandl:
        dataset_code = "FRED/%sSTHPI" %(state_code)
        df = Quandl.get(dataset_code)
        return df
    else:
        return pd.read_csv('FRED_HPI_%s' %(state_code))

states = list(pd.read_csv('states.csv')['Abbreviation'])

# df = pd.concat([get_house_price_index_by_state(state) for state in states], keys=states)

import os
import time
path = r'C:\Users\jylkka_a\Downloads'
go = True
if go:
    for state in states:
        try:
            if state == 'PR':
                continue
            full_path = os.path.join(path, state)
            if os.path.exists(full_path):
                print '%s exists, continuing:' %(state)
                continue
            df = get_house_price_index_by_state(state)
            df.to_csv(full_path)
        except Exception as e:
            print state
            print e
            time.sleep(1000)
