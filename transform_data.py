from load_dataset import DataGetter
import pandas as pd
import datetime as dt



# home
# dataPath = r'C:\Users\aaron\Downloads'

# work
dataPath = r'C:\Users\jylkka_a\Downloads'


print dt.datetime.now()
dg = DataGetter(dataPath = dataPath)
df = dg.getDataset()


is_delinq = lambda x: (x not in ('0', 'XX', 'R'))
# apply boolean indicating whether the loan status is delinquent
df['is_delinquent'] = df['current_loan_delinq_status'].apply(is_delinq)

gb = df.groupby(level=0)
# should return a series, for each loan give the index of the first thing that's delinquent
get_first_delinq = lambda x: x.idxmax()[1] if x.any() else pd.NaT
first_delinq = gb.is_delinquent.apply(get_first_delinq)
first_delinq.name = 'first_delinquency'
merged = df.merge(df, pd.DataFrame(first_delinq), left_index=True, right_index=True)
# get the monthly reporting date from the datetime index
i=merged.index.to_series().apply(lambda x: x[1])
past_delinq = (~ df.isnull(merged.first_delinquency)) & (i > merged.first_delinquency )
print merged.shape
print past_delinq.sum()
past_delinq = merged[past_delinq]
past_delinq_idx = past_delinq.index
merged.drop(past_delinq_idx, inplace=True)
print merged.shape
print 'ready'
#gb['is_delinquent'].idxmax() if gb['is_delinquent'].any() else None


# returns row of first default
# merged.loc[merged['is_defaulted'].idxmax()]

# pd.isnull(merged.zero_balance_eff_dt.unique()[0])
