# Solar Panel Rotator
 This app, built with streamlit, performs simple rotate operation on input images. 😎

## Steps of Orientation Prediction
### This section mainly show the main steps of panels orientation prediction. There are four main steps, including:
- (1) Predict solar panel.

 <img width=350 height=350 src="https://github.com/Robert-Mar/Solar-Panel-Rotator/blob/main/results/predict_solar_panel.png">
 
- (2) Cut the target from the image.

<img width=250 height=250 src="https://github.com/Robert-Mar/Solar-Panel-Rotator/blob/main/results/SinglePanels.png">
 
- (3) Predict rotation angle.

<img width=350 height=350 src="https://github.com/Robert-Mar/Solar-Panel-Rotator/blob/main/results/predict_rotate_angle.png">

- (4) Adjust rotation angle and get the orientation of panels.

<img width=350 height=350 src="https://github.com/Robert-Mar/Solar-Panel-Rotator/blob/main/results/draw_orientation.png">

 
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
