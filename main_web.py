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
import json

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
        
        # Dir folders and read file paths
        model_A_file_paths = glob.glob('static/model_A/*.*')
        model_B_file_paths = glob.glob('static/model_B/*.*')
        ground_truth_file_paths = glob.glob('static/ground_truth/*.*')
        
        # Extract file names only
        model_A_file_names = [os.path.basename(file_path) for file_path in model_A_file_paths]
        model_B_file_names = [os.path.basename(file_path) for file_path in model_B_file_paths]
        ground_truth_file_names = [os.path.basename(file_path) for file_path in ground_truth_file_paths]
        
        # Make sure each file appears in all three folders
        if ( 
            (len(model_A_file_names) != len(model_B_file_names)) or 
            (len(model_A_file_names) != len(ground_truth_file_names)) ):
            print('Error: different number of files in model_A, model_B and ground_truth folders')
            return
        for A_file_name in  model_A_file_names:
            if not A_file_name in model_B_file_names:
                print(A_file_name + " exists in model A but not in model B")
                return
            if not A_file_name in ground_truth_file_names:
                print(A_file_name + " exists in model A but not in ground truth")
                return
              
        # Permute order
        random.shuffle(model_A_file_names)
        
        # Log
        print('These are the files to be used')
        print(model_A_file_names)
        
        # Save image list to hidden varible
        form.image_list.data = json.dumps(model_A_file_names)
        
        # Initalize current image to the start of the stack
        form.current_viewed_image_number.data = 0
        
        # Initalize selections to empty list
        form.selections.data = json.dumps(list())
    else:
        # User entered response before
                
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
        selection_list = json.loads(form.selections.data) # Get list from hidden varible
        selection_list.append(response)
        form.selections.data = json.dumps(selection_list)
        
        # Move the id number one step
        form.current_viewed_image_number.data = int(form.current_viewed_image_number.data) + 1
    
    # Get image list from hidden varible
    image_list = json.loads(form.image_list.data)
    
    # Check if additional images remain, if not present end screen
    # TODO
    
    # Prepare to present the next image, first select if image one is A or B
    current_viewed_image_name = image_list[form.current_viewed_image_number.data]
    if random.randint(0,1) == 0:
        form.is_one_A.data = False
        option_1_image_path = "/static/model_B/" + current_viewed_image_name
        option_2_image_path = "/static/model_A/" + current_viewed_image_name
    else:
        form.is_one_A.data = True
        option_1_image_path = "/static/model_A/" + current_viewed_image_name
        option_2_image_path = "/static/model_B/" + current_viewed_image_name
    ground_truth_image_path = "/static/ground_truth/" + current_viewed_image_name
    
    # Present form to user
    return render_template('model_compare_ui.html', form=form, 
        image_index = form.current_viewed_image_number.data+1,
        total_number_of_images = len(image_list),
        option_1_image_path=option_1_image_path, 
        option_2_image_path=option_2_image_path, 
        ground_truth_image_path=ground_truth_image_path)


## Start Application ##############################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
