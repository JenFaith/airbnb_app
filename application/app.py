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
            message = f"ERROR: The URL /run_model is accessed directly. Try going to home page '/' to submit form"
        # if user goes to /form and hits submit, they go to this page!
        # in here user input gets stored into to_predict, and then to_predict gets run in model
        if request.method == 'POST':
            bedrooms = int(request.values["bedrooms"])
            bathrooms = float(request.values["bathrooms"])
            accomodates = int(request.values["accomodates"])
            # We will be adding a few more dropdowns above
            amenities = request.form.getlist('feature_checkbox')  # need to get this to print out T/F list
            #basics = 
            to_predict = [bedrooms, bathrooms, accomodates, amenities]
            message = model_output(to_predict)
        return message
    
# FAKE RESULT =  [[4, 1.5], 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def model_output(user_input):
        mod_input = []
        # for i in range(0,2):
        #     mod_input.append(to_predict.iloc[i])
        # list of ammenities
        all_ammenities = [
            "clean_fee","wifi","ac","kitchen","heat","family_friendly",
            "essentials","hair_dryer","iron","smoke_detector",
            "shampoo","hangers","fire_ext","laptop_friendly",
            "first_aid","indoor_fire","tv","cable_tv","elevator"]
        # Append unchanging variables to list first
        mod_input.extend(user_input[:2])
        input = user_input[3]
        # For loop through conditional varibles 
        for option in all_ammenities:
            if any(option in s for s in input):
                mod_input.append(1)
            else:
                mod_input.append(0)
        return str(mod_input)
    return app