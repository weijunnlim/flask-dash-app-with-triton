import xgboost as xgb
from explainerdashboard import ClassifierExplainer, ExplainerDashboard
from explainerdashboard.datasets import titanic_survive, titanic_names
from sklearn.model_selection import train_test_split
import pandas as pd

feature_descriptions = {
    "id": "Id of patient",
    "gender": "Gender of patient",
    "age": "Age of patient",
    "hypertension": "Indicates whether patient has hypertension",
    "heart_disease": "Indicates whether patient has heart disease", 
    "ever_married": "Indicates if patient has ever been married",
    "work_type": "Type of work",
    "Residence_type": "Type of residence",
    "avg_glucose_level" : "Average glucose level in blood",
    "bmi": "Body Mass Index", 
    "smoking_status": "Status of smoking",
}

dataset = pd.read_csv('healthcare-dataset-stroke-data.csv')

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
#print(dataset_clean_median.dtypes)
dataset_clean_median.to_csv('dataset_clean_median.csv', index=False)

X = dataset_clean_median.drop(['stroke', 'id'], axis=1) #all features
y = dataset_clean_median['stroke'] #target

X_train, X_test_val, y_train, y_test_val = train_test_split(X, y, test_size=0.2, random_state=123, stratify = y) #split into 118
X_test, X_val, y_test, y_val = train_test_split(X_test_val, y_test_val, test_size = 0.5, random_state= 123, stratify = y_test_val) #50% of 20% is 10%



#X_train, y_train, X_test, y_test = titanic_survive()
#train_names, test_names = titanic_names()
model = xgb.XGBClassifier(n_estimators=50, max_depth=5)
model.fit(X_train, y_train)

X_test = X_test.astype(int)

explainer = ClassifierExplainer(model, X_test, y_test, 
                                #cats=['work_type', 'smoking_status',
                                #    {'gender': ['Male', 'Female', 'Other']}],
                                #cats_notencoded={'Embarked': 'Stowaway'}, # defaults to 'NOT_ENCODED'
                                #descriptions=feature_descriptions, # adds a table and hover labels to dashboard
                                labels=['No/Low risk', 'At risk'], # defaults to ['0', '1', etc]
                                #idxs = , # defaults to X.index
                                #index_name = "patient", # defaults to X.index.name
                                #target = "stroke", # defaults to y.name
                                model_output = "raw",
                                )
# import shap
# explainer = shap.TreeExplainer(model)
# shap_values = explainer.shap_values(X)
# shap.force_plot(explainer.expected_value, shap_values[0, :], X.iloc[0, :])
# shap.save_html('force_plot.html', shap.force_plot(explainer.expected_value, shap_values[0, :], X.iloc[0, :]))
import pickle
with open('classifier_explainer.pkl', 'wb') as f:
    pickle.dump(explainer, f)
