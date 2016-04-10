from load_dataset import DataGetter
import pandas as pd
import datetime as dt




def calc_first_delinq(df):
    # any status code other than these is delinquent
    is_delinq = lambda x: (x not in ('0', 'XX', 'R'))
    # apply boolean indicating whether the loan status is delinquent
    df['is_delinquent'] = df['current_loan_delinq_status'].apply(is_delinq)
    # group by loan
    gb = df.groupby(level=0)
    # return monthly_reporting period (second element of index)
    # of the first instance of is_delinquent=True, if there are any
    get_first_delinq = lambda x: x.idxmax()[1] if x.any() else pd.NaT
    first_delinq = gb.is_delinquent.apply(get_first_delinq)
    first_delinq.name = 'first_delinquency'

    # add the first delinquency to the main dataframe
    df = pd.merge(df, pd.DataFrame(first_delinq), left_index=True, right_index=True)

    # now we want to drop all records where the date is after the date of first delinquency,
    # because we are only trying to predict first delinquency

    # get the monthly reporting date from the datetime index
    i=df.index.to_series().apply(lambda x: x[1])
    # get boolean series indicating where monthly_reporting_date is after first delinquency
    past_delinq = (~ pd.isnull(df.first_delinquency)) & (df.first_delinquency < i)
    past_delinq = df[past_delinq]
    past_delinq_idx = past_delinq.index
    df.drop(past_delinq_idx, inplace=True)
    df.first_delinquency.name
    print 'return transformed data'

def calc_delinq_next_month(df):
    gb = df.groupby(level='loan_sequence_number')
    df['first_delinq_next_month'] = gb['is_delinquent'].shift(-1)
    df.dropna(subset=['first_delinq_next_month'], inplace=True)
    df['first_delinq_next_month'] = df['first_delinq_next_month'].astype(bool)



if __name__ == '__main__':
    # home
    # dataPath = r'C:\Users\aaron\Downloads'

    # work
    dataPath = r'C:\Users\jylkka_a\Downloads'

    dg = DataGetter(dataPath=dataPath)
    df = dg.getDataset()
    print 'got dataset, now munging'
    calc_first_delinq(df)
    calc_delinq_next_month(df)
    #print df.first_delinquency.name
    print 'done'