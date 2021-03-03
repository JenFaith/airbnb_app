"""Functions to make model predictions"""

import numpy as np
import pandas as pd
from joblib import load

# Load model
# This should be located near the top of the app.create_app function so that
# the model is loaded only once upon instantiation
# TODO - Cut and paste into app.create_app


def get_prediction(user_data, model):
    """
    Makes a prediction using data input by user on web app.

    Parameters
    ----------
    user_data : list
        Features used in Airbnb prediction model
    model : 
        Pretrained model used to make predictions

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
        "bathrooms",
        "cancellation_policy",
        "city",
        "host_since",
        "review_scores_rating",
        "bedrooms",
        "beds",
        "instant_bookable",
        "host_has_profile_pic",
        "host_identity_verified",
        "cleaning_fee",
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
        "Cable TV",
    ]

    # dictionary for forcing data types accepted by sklearn
    data_types = {
        "property_type":                object,
        "room_type":                    object,
        "bathrooms":                    np.float64,
        "cancellation_policy":          object,
        "city":                         object,
        "host_since":                   np.int64,
        "review_scores_rating":         object,
        "bedrooms":                     np.float64,
        "beds":                         np.float64,
        "instant_bookable":             bool,
        "host_has_profile_pic":         bool,
        "host_identity_verified":       bool,
        "cleaning_fee":                 bool,
        "Wireless Internet":            bool,
        "Air conditioning":             bool,
        "Kitchen":                      bool,
        "Heating":                      bool,
        "Family/kid friendly":          bool,
        "Hair dryer":                   bool,
        "Iron":                         bool,
        "Shampoo":                      bool,
        "Fire extinguisher":            bool,
        "Laptop friendly workspace":    bool,
        "Indoor fireplace":             bool,
        "TV":                           bool,
        "Cable TV":                     bool,
    }

    # Make sure the data is coming in correctly
    # This also serves as a simple backend data validation so the route returns
    # a value even if someone tries to spoof a data point
    try:
        assert len(user_data) == len(
            feature_order), 'User_data not long enough'

        # dictionary to construct dataframe
        data = {feature: [datum]
                for feature, datum in zip(feature_order, user_data)}
        assert len(data) == len(feature_order), 'dictionary size incorrect'

        # transform input into dataframe for model prediction
        transformed_input = pd.DataFrame(
            data).astype(data_types)[feature_order]

        # make prediction using model
        prediction = model.predict(transformed_input)
    except:
        print('-----ERROR IN TRANSFORMING INPUT-----')
        prediction = [0]

    # return prediction in USD rounded to the penny
    return np.exp(prediction[0]).round(2)
