# Solar Panel Rotator
 This app, built with streamlit, performs simple rotate operation on input images. 😎

## Steps of Orientation Prediction
### This section mainly show the main steps of panels orientation prediction. There are four main steps, including:
#### Step 1: Predict solar panel. 

At first, solar panel can be detected through existing models such as YOLO, Faster RCNN. Our solar panel detector only predicts the orientation of panel based on the detected results instead of detecting solar panels.
<img width=450 height=450 src="https://github.com/Robert-Mar/Solar-Panel-Rotator/blob/main/results/predict_solar_panel.png">
 
#### Step 2: Cut the target from the image.

 Crop the pictures to facilitate the prediction of the single small solar panel in the back.
 
#### Step 3: Predict rotation angle.

Input the cropped images to the model, and then output prediction angle.
<img width=450 height=450 src="https://github.com/Robert-Mar/Solar-Panel-Rotator/blob/main/results/predict_rotate_angle.png">

#### Step 4: Adjust rotation angle and get the orientation of panels.

In order to get the orientation of panel, we need to add or subtract 90 degrees from the prediction angle, the output of step 3.
<img width=450 height=450 src="https://github.com/Robert-Mar/Solar-Panel-Rotator/blob/main/results/draw_orientation.png">

 
### Dependencies
This code uses the following libraries
- python 3.7+
- streamlit
- numpy
- matplotlib
- pillow
- opencv-python

## Run
Run the code below to run the local version of Solar Panel Rotator.
```
streamlit run main.py
```
