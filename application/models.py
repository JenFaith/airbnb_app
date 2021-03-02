# File to run model

# IMPORT STATEMENTS
from datetime import datetime
import pandas as pd
import numpy as np
import requests
import datetime
from datetime import datetime
import joblib

# IMPORTS FOR MODEL
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# IMPORT FILES
train = pd.read_csv("data/archive-2/train.csv", index_col='id')
test = pd.read_csv("data/archive-2/test.csv", index_col='id')


def cleaned_dataframe(df):
    """
    1. Adds feature columns to df
    2. Deals with all null values
    3. Turns ratings into categorical column
    4. Converts "Host_since" into a measure of time
    """ 
    features = ['Wireless Internet','Air conditioning', 'Kitchen', 'Heating','Family/kid friendly', 'Essentials', 'Hair dryer', 'Iron', 
                'Smoke detector', 'Shampoo', 'Hangers', 'Hair dryer', 'Fire extinguisher', 'Laptop friendly workspace', 'First aid kit', 'Indoor fireplace',
                'TV','Cable TV', 'Elevator in building']
    
    # forloop to create all new columns
    for item in features:
        df[item]=np.where(df['amenities'].str.contains(item), 1, 0)
        
        
    # drop unnecessary column & columns with no host information
    # neighborhood will be dictated by zip and latitude/longitude
    df.drop(columns=['amenities', 'first_review', 'last_review', 'host_response_rate', 'neighbourhood'], axis=1, inplace=True)
    
    # drop rows with null values in certain columns
    df = df.dropna(axis=0, subset=['bathrooms', 'bedrooms', 'beds'])
    
    # dropped rows with no host information or now zip code
    df = df.dropna(axis=0, subset=['host_since', 'host_identity_verified', 'zipcode'])
    
    # Dealing with ratings column
    # Zero isn't a real rating in the columns
    # Temporarily assign rating_score with no previous reviews as 0 so it can later make it a category
    df['review_scores_rating']=np.where(df['number_of_reviews']==0, 0, df['review_scores_rating'])
    
    # drop remaining 800 rows with no values
    df = df.dropna(axis=0, subset=['review_scores_rating'])
    
    # change reviews into categories
    df['review_scores_rating'] = df['review_scores_rating'].round(-1).astype('int').astype('str')
    
    # reassign 0 ratings as "no past ratings" category
    df['review_scores_rating']=np.where(df['number_of_reviews']==0, 'no past ratings', df['review_scores_rating'])
    
    # Convert "host_since" into column that measures # of days an individual has been a host
    for i in range(len(df['host_since'])):
        today = datetime.today()
        date_time_obj = datetime.strptime(df['host_since'].iloc[i], '%Y-%m-%d')
        df['host_since'].iloc[i] = (today - date_time_obj).days
    
    # Convert "host_since" from object to int
    df['host_since'] = df['host_since'].astype('int')
    
    
    #drop columns with low correlation
    df.drop(columns=['latitude', 'longitude', 'Smoke detector', 'number_of_reviews', 'Hangers','First aid kit', 'Elevator in building', 'Essentials', 'zipcode', 'thumbnail_url', 'description', 'name'], axis=1, inplace=True)
    return df

# Clean Copy of DF
trained = cleaned_dataframe(train)

# Instantiate Model w/ Cleaned Data
# Split into X, y, train/test
target = 'log_price'
y = trained[target]
X = trained.drop(columns=target)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Categorical columns to OneHotEncode
cat = X_train.select_dtypes(include=['object', 'bool']).columns

# Integer/Float Columns to Scale
num = X_train.select_dtypes(include=['int', 'float']).columns

# define model
model = RandomForestRegressor(n_estimators=200,
                                max_depth=20)

# define transform
transformer = ColumnTransformer(transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), cat),
                                              ('num', StandardScaler(), num)], remainder='passthrough')

# define pipeline
pipeline = Pipeline(steps=[('t', transformer), ('m',model)])
# fit the pipeline on the transformed data
pipeline.fit(X_train, y_train)

# save the model
filename = 'finalized_model.sav'
joblib.dump(pipeline, filename)
 
# verify saved model is workin
loaded_model = joblib.load(filename)
result = loaded_model.score(X_test, y_test)
print(result)
