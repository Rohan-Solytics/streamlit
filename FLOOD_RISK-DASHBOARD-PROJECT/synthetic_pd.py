import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import streamlit as st



def synthetic_pd_calc(data):

    # Define the target variable for PD (assuming it's already binary and named 'PD')
    # and ensure it's in the correct binary format
    data['PD'] = data['PD'].astype(int)

    # Define categorical features that need to be one-hot encoded
    categorical_features = ['Credit History', 'Borrower']  # replace with your actual categorical features

    # Define the continuous features
    continuous_features = ['PTI']  # replace with your actual continuous features

    # Define the LTV features for each year
    ltv_features_years = [f'LTV {year}' for year in range(2020, 2055, 5)]

    # Define the full features list
    full_features = continuous_features + categorical_features + ltv_features_years

    # Preprocess the categorical features with one-hot encoding
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(), categorical_features)
        ],
        remainder='passthrough'
    )

    # Include PolynomialFeatures for continuous variables
    polynomial_features = PolynomialFeatures(degree=2, include_bias=False)

    # Create a pipeline with preprocessing and logistic regression model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('polynomial_features', polynomial_features),
        ('classifier', LogisticRegression(max_iter=1000))
    ])

    # Train a separate logistic regression model for each LTV year and predict PD
    for year in range(2020, 2055, 5):
        # Select the LTV feature for the specific year and other continuous features
        ltv_feature_for_year = [f'LTV {year}']
        year_features = continuous_features + ltv_feature_for_year
        
        # Prepare the features and target
        X = data[year_features + categorical_features]
        y = data['PD']
        
        # Fit the pipeline to the data
        pipeline.fit(X, y)
        
        # Make predictions for PD for the given year
        data[f'PD {year}'] = pipeline.predict_proba(X)[:, 1]


    df = pd.DataFrame(data)
    # predicted_df = data
    # Save the updated dataset with PD predictions to a new CSV file
    data.to_csv('datasets/prob_def_df.csv', index=False)
    # data = data.drop(['flood_risk'], axis=1)
    return df

def synthetic_pd_flood_calc(data):
    # Define the target variable for PD (assuming it's already binary and named 'PD')
    # and ensure it's in the correct binary format
    data['PD'] = data['PD'].astype(int)

    # Define categorical features that need to be one-hot encoded
    categorical_features = ['Credit History', 'Borrower']  # replace with your actual categorical features

    # Define the continuous features
    continuous_features = ['PTI', 'flood_risk']  # replace with your actual continuous features

    preprocessor = ColumnTransformer(
            transformers= [
                ('cat', OneHotEncoder(), categorical_features),
                ('num', 'passthrough', continuous_features)
            ]
        )
        
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression())
    ])


    # All other code remains the same until the training loop
    # Train a separate logistic regression model for each LTV year and predict PD
    for year in range(2020, 2055, 5):
        # Select the LTV feature for the specific year
        ltv_feature_for_year = f'LTV {year}'
        # Define the feature set for this iteration
        features = continuous_features + [ltv_feature_for_year] + categorical_features
        
        # target = 'PD'
        # Prepare the feature matrix and target vector
        X = data[features]
        y = data['PD']
        
        # Create the preprocessing and training pipeline 
        
        
        #Train the model
        pipeline.fit(X, y)
        #Make predictions for the probability of default in the given year 
        data[f'PD_FR_{year}'] = pipeline.predict_proba(X)[:, 1]
        # Save the updated dataframe to a new CSV file
    data.to_csv('datasets/chicago_flood_risk.csv', index=False)
    return data

    