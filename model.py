from __future__ import division
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import Imputer
from sklearn.base import TransformerMixin
from load_dataset import DataGetter
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
from transform_data import calc_delinq_next_month, calc_first_delinq


class DataFrameImputer(TransformerMixin):

    def __init__(self):
        """Impute missing values.

        Columns of dtype object are imputed with the most frequent value
        in column.

        Columns of other types are imputed with mean of column.

        """
    def fit(self, X, y=None):

        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') or hasattr(X[c], 'cat') else X[c].mean() for c in X],
            index=X.columns)

        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)














dg = DataGetter()
df = dg.getDataset(year_range=[2000, 2003])
calc_first_delinq(df)
calc_delinq_next_month(df)

# smaller just for playing with it
#df = df.sample(frac=.2)

y = df['first_delinq_next_month']
X = df.drop('first_delinq_next_month', axis=1)

# build limited feature set
model_features = ['current_actual_upb', 'credit_score', 'loan_age', 'property_state'
                  ,'dti_ratio'
                  #,'remaining_months2maturity'
                  ,'interest_rate'
                  ,'loan2value'
                  ]
X = X[model_features]
le = LabelEncoder()
X['property_state'] = le.fit_transform(X['property_state'])
# X.dropna(subset=['property_state'], inplace=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, random_state=42)

# _imp = DataFrameImputer()
# X_train = _imp.fit_transform(X_train)
# X_test = _imp.transform(X_test)

imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
X_train = imp.fit_transform(X_train)
X_test = imp.transform(X_test)

bench = 1. - y_test.sum() / y_test.count()

print 'Training Decision Tree Classifier'
dtc = DecisionTreeClassifier()
dtc.fit(X_train, y_train)
score = dtc.score(X_test, y_test)

print 'Decision Tree Classifier model score of %f vs benchmark score of %f' %(score, bench)

print 'Training Logistic Regression Classifier'
lr = LogisticRegression(verbose=False)
lr.fit(X_train, y_train)
score = lr.score(X_test, y_test)

print 'Logistic Regression model score of %f vs benchmark score of %f' %(score, bench)

print 'Training Random Forest Classifier'
rfc = RandomForestClassifier()
rfc.fit(X_train, y_train)
score = rfc.score(X_test, y_test)

print 'Random Forest model score of %f vs benchmark score of %f' %(score, bench)

# print most important features
import pprint
feature_importances = zip(model_features, rfc.feature_importances_)
feature_importances.sort(key=lambda x:x[1], reverse=True)
pprint.pprint(feature_importances)