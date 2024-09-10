import pandas as pd
import numpy as np


dataset = pd.read_csv('healthcare-dataset-stroke-data.csv')

#impute using median(since bmi is a numerical value not categorical)
from sklearn.impute import SimpleImputer
dataset_clean_median = dataset.copy()
imputer = SimpleImputer(strategy = 'median')
columns_to_impute = ['bmi']
dataset_clean_median[columns_to_impute] = imputer.fit_transform(dataset_clean_median[columns_to_impute])

#impute using most freq(for categorical var)
most_frequent = dataset_clean_median.loc[dataset_clean_median['smoking_status'] != 'Unknown', 'smoking_status'].mode()[0]
dataset_clean_median['smoking_status'] = dataset_clean_median['smoking_status'].replace('Unknown', most_frequent) #basically replace with never smoked

#convert categorical using one-hot encoding
dataset_clean_median = pd.get_dummies(dataset_clean_median, drop_first=True) #using one-hot encoding, remove the first level to reduce no of columns
# print(dataset_encoded_median.info()) # theres 1 gender type called 'Other'
print(dataset_clean_median.dtypes)
unique_values_all = dataset_clean_median.apply(pd.Series.unique)
print("Unique values in each column:\n", unique_values_all)