from results import get_results
import xgboost as xgb
import pandas as pd
import pickle
import numpy as np

from sklearn.model_selection import cross_validate, train_test_split
from sklearn.multioutput import MultiOutputClassifier

from hyperopt import hp, tpe, fmin
from hyperopt import Trials
from hyperopt import STATUS_OK

model_name = "XGBoost"
loaddir = "feature_extraction/data/features/"

#read data
df = pd.read_csv(loaddir + 'features.csv', index_col=0)

def create_target(text):
    text = text.strip('][')
    text = text.split(', ')
    return [int(i) for i in text]

df["target"] = df["target"].apply(create_target)

df_train, df_test = train_test_split(df, test_size=0.1, random_state=0)

train_x = df_train.drop(["target"], axis = 1)
train_y = df_train["target"]

test_x = df_test.drop(["target"], axis = 1)
test_y = df_test["target"]


model = xgb.XGBClassifier()
print(train_y)
print(train_x.values)
clf = MultiOutputClassifier(model).fit(train_x, train_y)

pred = clf.predict_proba(test_x)
print(test_y["target"])
print(pred)
