"""Functions to make model predictions"""

from pickle import load

# Load model
# This should be located near the top of the app.create_app function so that
# the model is loaded only once upon instantiation
# TODO - Cut and paste into app.create_app to
model = load('filename')


def predict(user_data):
    """
    Makes a prediction using data input by user on web app.

    arguments:
    user_data -- list of user input

    """

    return  # model.predict()


# Run tests on functions
if __name__ == "__main__":

    predict((0, 'test', True))
