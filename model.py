from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from load_dataset import DataGetter
from transform_data import calc_delinq_next_month, calc_first_delinq

dg = DataGetter()
df = dg.getDataset()
calc_first_delinq(df)
calc_delinq_next_month(df)

y = df['first_delinq_next_month']
X = df.drop('first_delinq_next_month', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, random_state=42)


