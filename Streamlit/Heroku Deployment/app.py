#heroku create loan-prediction-ds3
#git add remote heroku https://git.heroku.com/loan-prediction-ds3.git
#git init
#git add .
#git commit -m "first commit"
#git push heroku master


import streamlit as st
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from PIL import Image

coltrans = ColumnTransformer([
      ('imputer-mod_onehot', Pipeline([
                                ('imputer-mod', SimpleImputer(strategy='most_frequent')),
                                ('onehot', OneHotEncoder(drop='first')),
                              ]), ['Gender', 'Married', 'Self_Employed']),
      ('imputer-mod', SimpleImputer(strategy='most_frequent'), ['Credit_History']),
      ('imputer-mean_scaling', Pipeline([
                                ('imputer-mean', SimpleImputer(strategy='mean')),
                                ('scaling', StandardScaler()),
                              ]), ['Dependents', 'LoanAmount', 'Loan_Amount_Term']),
      ('onehot', OneHotEncoder(drop='first'), ['Education', ]),
      ('scaling', StandardScaler(), ['ApplicantIncome', 'CoapplicantIncome', ]),
])

@st.cache
def get_data():
    X = pd.read_csv("https://raw.githubusercontent.com/Ramanand-Yadav/EligibilityForBankLoanMLProject/main/trainDataset.csv")
    X.drop('Loan_ID', axis = 1, inplace = True)

    Y = X['Loan_Status']
    X = X.drop('Loan_Status', axis=1)

    X['Dependents'].replace({'3+': 3}, inplace = True)
    X['Dependents'] = pd.to_numeric(X['Dependents'])
    Y = np.where(Y == 'Y', 1, 0)
    
    return X, Y

X, Y = get_data()
columns = X.columns
X = coltrans.fit_transform(X)


@st.cache
def get_model():
    model = LogisticRegression().fit(X, Y)
    return model

model = get_model()


img = Image.open('img1.jpg')
st.image(img)

st.header('Bank Loan Prediction')

data = {}

data['Gender'] = st.selectbox('Gender', ['Male', 'Female'])
data['Married'] = st.selectbox('Married', ['Yes', 'No'])
data['Dependents'] = st.number_input('Dependents', min_value=0)
data['Education'] = st.selectbox('Education', ['Graduate', 'Not Graduate'])

map = {'Job': 'No', 'Bussiness': 'Yes'}
data['Self_Employed'] = st.selectbox('Self_Employed', ['Job', 'Bussiness']) # format_func
data['Self_Employed'] = map[data['Self_Employed']]

data['ApplicantIncome'] = st.number_input('ApplicantIncome', min_value=0)
data['CoapplicantIncome'] = st.number_input('CoapplicantIncome', min_value=0)
data['LoanAmount'] = st.number_input('LoanAmount', min_value=0)
data['Loan_Amount_Term'] = st.number_input('Loan_Amount_Term', min_value=0)
data['Property_Area'] = st.selectbox('Property_Area', ['Rural', 'Urban', 'Semiurban	'])

map = {'Good': 1, 'Average': 0}
data['Credit_History'] = st.selectbox('Transaction Frequency', ['Good', 'Average']) # format_func
data['Credit_History'] = map[data['Credit_History']]


test_data = pd.DataFrame(data, index = [0], columns = columns)
st.dataframe(test_data)



if st.button('Submit'):
    test_data = coltrans.transform(test_data)
    pred = model.predict(test_data)[0]

    if pred == 1:
        st.success('Loan will Approve')
    else:
        st.error('Loan will not Approve')