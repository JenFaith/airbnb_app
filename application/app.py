# Import Statements
import pandas as pd
from flask import Flask, render_template, request
# from .models import predictor


# Instantiate Application
def create_app():
    """
    Function to deploy heroku application.
    Contains assorment of functions which control the inputs and outputs
    of interractive web application.
    """
    app = Flask(__name__)
    
    @app.route("/", methods = ['GET', 'POST'])
    def main_page():
        """
        Controls main, welcome page.
        """
        return "Yep, app is working! :D"

    return app