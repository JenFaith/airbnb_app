"""Functions to make model predictions"""

import numpy as np
import pandas as pd
from joblib import load

# Load model
# This should be located near the top of the app.create_app function so that
# the model is loaded only once upon instantiation
model = load('finalized_model.sav')  # TODO - Cut and paste into app.create_app


def get_prediction(user_data):
    """
    Makes a prediction using data input by user on web app.

    Parameters
    ----------
    user_data : list
        Features used in Airbnb prediction model

    Returns
    -------
    float
        Prediction in USD per day (e.g. 124.32)
    """

    # Feature orders needed for model.predict's input data
    # The columns are required to be in the same order as the data input
    feature_order = [
        "property_type",
        "room_type",
        "accommodates",
        "bathrooms",
        "bed_type",
        "cancellation_policy",
        "cleaning_fee",
        "city",
        "host_has_profile_pic",
        "host_identity_verified",
        "host_since",
        "instant_bookable",
        "review_scores_rating",
        "bedrooms",
        "beds",
        "Wireless Internet",
        "Air conditioning",
        "Kitchen",
        "Heating",
        "Family/kid friendly",
        "Hair dryer",
        "Iron",
        "Shampoo",
        "Fire extinguisher",
        "Laptop friendly workspace",
        "Indoor fireplace",
        "TV",
        "Cable TV"
    ]

    # dictionary for forcing data types accepted by sklearn
    data_types = {
        "property_type":                object,
        "room_type":                    object,
        "accommodates":                 np.int64,
        "bathrooms":                    np.float64,
        "bed_type":                     object,
        "cancellation_policy":          object,
        "cleaning_fee":                 bool,
        "city":                         object,
        "host_has_profile_pic":         object,
        "host_identity_verified":       object,
        "host_since":                   np.int64,
        "instant_bookable":             object,
        "review_scores_rating":         object,
        "bedrooms":                     np.float64,
        "beds":                         np.float64,
        "Wireless Internet":            np.int64,
        "Air conditioning":             np.int64,
        "Kitchen":                      np.int64,
        "Heating":                      np.int64,
        "Family/kid friendly":          np.int64,
        "Hair dryer":                   np.int64,
        "Iron":                         np.int64,
        "Shampoo":                      np.int64,
        "Fire extinguisher":            np.int64,
        "Laptop friendly workspace":    np.int64,
        "Indoor fireplace":             np.int64,
        "TV":                           np.int64,
        "Cable TV":                     np.int64,
    }

    # dictionary to construct dataframe
    data = {feature: [datum]
            for feature, datum in zip(feature_order, user_data)}

    # transform input into dataframe for model prediction
    transformed_input = pd.DataFrame(data).astype(data_types)[feature_order]

    # make prediction using model
    prediction = model.predict(transformed_input)

    # return prediction in USD rounded to the penny
    return np.exp(prediction[0]).round(2)


# Run tests on functions
if __name__ == "__main__":

    user_input = [
        "Apartment",        # property_type
        "Entire home/apt",  # room_type
        3,                  # accommodates
        1.0,                # bathrooms
        "Real Bed",         # bed_type
        "strict",           # cancellation_policy
        True,               # cleaning_fee
        "NYC",              # city
        "t",                # host_has_profile_pic
        "f",                # host_identity_verified
        1369,               # host_since
        "f",                # instant_bookable
        90,                 # review_scores_rating
        0.0,                # bedrooms
        2.0,                # beds
        1,                  # Wireless Internet
        1,                  # Air conditioning
        0,                  # Kitchen
        1,                  # Heating
        0,                  # Family/kid friendly
        0,                  # Hair dryer
        0,                  # Iron
        0,                  # Shampoo
        1,                  # Fire extinguisher
        0,                  # Laptop friendly workspace
        0,                  # Indoor fireplace
        1,                  # TV
        0                   # Cable TV"
    ]
    print('Prediction: $', get_prediction(user_input))

    # TEST Some random test set values
    X_test = pd.read_csv('data/archive-2/test_2.csv',  # TODO - Change path
                         index_col='id').sample(10)
    print([get_prediction(X_test.iloc[i].tolist())
           for i in range(len(X_test))])
