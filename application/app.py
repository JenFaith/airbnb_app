# Import Statements
import pandas as pd
from flask import Flask, render_template, request
# from .models import jen_model


# Instantiate Application
def create_app():
    """
    Function to deploy heroku application.
    Contains assorment of functions which control the inputs and outputs
    of interractive web application.
    """
    app = Flask(__name__)


    # Commented out original main page, can change back
    # @app.route("/", methods = ['GET', 'POST'])
    # def main_page():
    #     """
    #     Controls main, welcome page.
    #     """
    #     return "Yep, app is working! :D"

    @app.route('/') # as easy as changing path to /form and make a link to it in main page
    def form():
        return render_template('form.html')

    @app.route('/run_model', methods=['POST', 'GET'])
    def data():
        # if user types in /run_model they get this error message
        if request.method == 'GET':
            return f"ERROR: The URL /run_model is accessed directly. Try going to home page '/' to submit form"
        # if user goes to /form and hits submit, they go to this page!
        # in here user input gets stored into to_predict, and then to_predict gets run in model
        if request.method == 'POST':
            bedrooms = int(request.form["bedrooms"])
            bathrooms = float(request.form["bathrooms"])
            accomodates = int(request.form["accomodates"])

            # This is one way we tried to get it to work.
            clean_fee = request.form["clean_fee"]
            ac = request.form["ac"]
            kitchen = request.form["kitchen"]

            # This is another way.
            ammenities = request.form.getlist('feature_checkbox')  # need to get this to print out T/F list
            to_predict = (bedrooms, bathrooms, accomodates, clean_fee, ac, kitchen, ammenities)
            # pred_price = jen_model.predict(to_predict)
            return str(to_predict)  # The price should be {pred_price} change this to return jen model info!!!!

    return app
