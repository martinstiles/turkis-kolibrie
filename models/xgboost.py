from results import get_results
import xgboost as xgb
import pandas as pd
import pickle

from hyperopt import hp, tpe, fmin
from hyperopt import Trials
from hyperopt import STATUS_OK

model_name = "XGBoost"
loaddir = "feature_extraction/data/features/"

#read data
df = pd.read_pickle(loaddir + "features.pickle")
print(df)
