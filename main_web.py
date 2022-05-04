# Run this function to render the web page
from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask import request
from wtforms import HiddenField, SubmitField
from wtforms.validators import DataRequired
import time
from datetime import datetime
import glob,os
from shutil import copyfile
import random

app = Flask(__name__)
#Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'G2HWAV3MGfNTqsrYQg8EcMrdTimkZ724'
Bootstrap(app)

######################## Main Page ##################################################
@app.route('/')    
def main_page():  
    return render_template('main.html')

######################## Compare Two Models #########################################

## Setup 
# This web page will set up a comparison between two models and a ground truth
@app.route('/ModelCompareSetup/') 
def model_compare_setup():
    if not os.path.exists('static'): # Make dir if it doesn't exist
            os.makedirs('static')
    if not os.path.exists('static/model_A'): # Make dir if it doesn't exist
            os.makedirs('static/model_A')
    if not os.path.exists('static/model_B'): # Make dir if it doesn't exist
            os.makedirs('static/model_B')
    if not os.path.exists('static/ground_truth'): # Make dir if it doesn't exist
            os.makedirs('static/ground_truth')
    return render_template('model_Compare_setup.html', base_folder=os.getcwd())
    
## Comparison Body
class ModelComparisonForm(FlaskForm):
    one_is_better = SubmitField('Option 1 Better')
    two_is_better = SubmitField('Option 2 Better')
    both_options_are_bad = SubmitField('Both are Bad')
    both_options_are_good = SubmitField('Both are Good')
    
    # Hidden field containing the list of images and up to what image did we get
    image_list = HiddenField('Image List')
    current_viewed_image_number = HiddenField('Image Number') #Image's number in array
    
    # Hidden fields containing meta data on current selection
    is_one_A = HiddenField('Is Option 1 A')
    
    # Hidden fields containing selection history so far
    selections = HiddenField('Selections')
    

@app.route('/ModelCompare/', methods=['GET', 'POST'])    
def model_compare_main():
    form = ModelComparisonForm()
    
    if request.method == 'GET':
        # If this is the first time user views the form, initalize the questioner
        print('Init questions')
        
        # TODO
        
        # Initalize current image to the start of the stack
        form.current_viewed_image_number.data = 0
    else:
        # Figure out what user's response was
        response = ''
        if form.both_options_are_bad.data:
            response = 'Both Bad'
        elif form.both_options_are_good.data:
            response = 'Both Good'
        else:
            # User selected one of the images, but which one was it?
            one_is_better = form.one_is_better.data
            is_one_A = form.is_one_A.data == 'True'
            
            if one_is_better and is_one_A:
                response = 'A is better'
            elif one_is_better and not is_one_A:
                response = 'B is better'
            elif not one_is_better and is_one_A:
                response = 'B is better'
            elif not one_is_better and not is_one_A:
                response = 'A is better'
            else:
                print('Error, cannot figure out what user selected')
                return
        print(response) # print selection to the back-end
                
        # Log user response on the hidden field
        # TODO
        
        # Move the id number one step
        form.current_viewed_image_number.data = int(form.current_viewed_image_number.data) + 1
    
    # Check if additional images remain, if not present end screen
    # TODO
    
    # Prepare to present the next image, first select if image one is A or B
    if random.randint(0,1) == 0:
        form.is_one_A.data = False
    else:
        form.is_one_A.data = True
    
    # Present form to user
    return render_template('model_compare_ui.html', form=form)


## Start Application ##############################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
