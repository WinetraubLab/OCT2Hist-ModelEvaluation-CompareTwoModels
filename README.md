# Model Compare
This module compares image quality between two models.
Evaluation is duble blind, user doesn't know which image is being examined.

In order to properly evaluate two models it is recommended to compare 50 images from test and then running the tool again on 50 images from training set.

## To get started
1. Run main_web.py
2. Using web browser log on to http://localhost/ModelCompareSetup

## Inputs
Model Compare Inputs are:
1. Model A virtual histology images - placed at static/model_A/
2. Model B virtual histology images - placed at static/model_B/. Model B is sometimes refered to as refference model.
3. Ground truth histology images - placed at static/ground_truth/

## Outputs
After a human evaluation the following will be presented on the web page
1. Overall statistics - what were the preferences of the user.
2. Detailed response - what user selected for each image pair.
