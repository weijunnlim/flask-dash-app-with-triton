import numpy as np
import pandas as pd

#dataset link: https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset 

dataset = pd.read_csv('healthcare-dataset-stroke-data.csv')
print("# of Rows, # of Columns: ",dataset.shape)
print("\nColumn Name           # of Null Values\n")
print(dataset.isnull().sum())

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

#train using xgboost
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier 
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, confusion_matrix

X = dataset_clean_median.drop(['stroke', 'id'], axis=1) #all features
y = dataset_clean_median['stroke'] #target

X_train, X_test_val, y_train, y_test_val = train_test_split(X, y, test_size=0.2, random_state=123, stratify = y) #split into 118
X_test, X_val, y_test, y_val = train_test_split(X_test_val, y_test_val, test_size = 0.5, random_state= 123, stratify = y_test_val) #50% of 20% is 10%


import xgboost as xgb
import optuna

def objective(trial):
    
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'gamma': trial.suggest_float('gamma', 0, 5),
        'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
        'reg_lambda': trial.suggest_float('reg_lambda', 0, 1),
    }
    
    model = xgb.XGBClassifier(**params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)
    accuracy = accuracy_score(y_pred, y_val)
    
    return accuracy

# Create a study and optimize
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=200)

print("Best parameters:", study.best_params)
print("Best score from optuna:", study.best_value)

#time to fit in the best params
best_params = study.best_params
best_model = xgb.XGBClassifier(
    **best_params,
    eval_metric='logloss',
    random_state=123
)
best_model.fit(X_train, y_train)

# Evaluating based on validation set
y_pred_val = best_model.predict(X_val)
y_pred_proba_val = best_model.predict_proba(X_val)[:, 1]

accuracy = accuracy_score(y_val, y_pred_val)
print(f"Val Accuracy: {accuracy}")
print("Val Classification Report:\n", classification_report(y_val, y_pred_val, zero_division=0)) #recall is ratio of correctly predicted positives to all observations
print("Val ROC-AUC Score:", roc_auc_score(y_val, y_pred_proba_val)) #trade off between true positive and false positive
#i used the actual y value which is 0 or 1 instead of a probability thats being predicted, so now this using proba, its more accurate

#youden j statistic

from sklearn.metrics import roc_curve
fpr, tpr, thresholds = roc_curve(y_val, y_pred_proba_val)
j_stat = tpr - fpr

optimal_threshold = thresholds[np.argmax(j_stat)]
print("Optimal Threshold:", optimal_threshold)

y_pred_matrix = (y_pred_proba_val > optimal_threshold).astype(int)
conf_matrix = confusion_matrix(y_val, y_pred_matrix)
print(conf_matrix)

from sklearn.metrics import f1_score
f1 = f1_score(y_val, y_pred_matrix) 

print("F1 Score:", f1)
accuracy = accuracy_score(y_val, y_pred_matrix)
print(f"Val Accuracy with opt threshold: {accuracy}")
print("Val ROC-AUC Score with opt threshold:", roc_auc_score(y_val, y_pred_matrix))

#finally test on test set
# Use the best model to make predictions on the test set
y_pred_test = best_model.predict(X_test)
y_pred_proba_test = best_model.predict_proba(X_test)[:, 1]
y_pred_proba_test = (y_pred_proba_test > optimal_threshold).astype(int)

# Evaluate the model based on the test set
test_accuracy = accuracy_score(y_test, y_pred_test)
test_roc_auc_score = roc_auc_score(y_test, y_pred_proba_test)

print(f"Test Accuracy: {test_accuracy}")
print("Test ROC-AUC Score:", test_roc_auc_score)

#lastly save the model
# Save the model
best_model.save_model('stroke_model.json')

