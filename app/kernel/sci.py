from joblib import dump, load
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder, 
from sklearn.metrics import mean_absolute_percentage_error as mape, mean_absolute_error as mae
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline



ordinal_encoder = load('ordinal_encoder.joblin')

pipeline = load('pipe_rfr.joblib')
