# Solar Panel Rotator
 This app, built with streamlit, performs simple rotate operation on input images. 😎

## Steps of Orientation Prediction
### This section mainly show the main steps of panels orientation prediction. There are four main steps, including:
- (1) Predict solar panel.
 ![image](https://user-images.githubusercontent.com/52849989/120014184-56055100-c014-11eb-8860-6376a0ce7e92.png)

- (2) Cut the target from the image.
- (3) Predict rotation angle.
- (4) Adjust rotation angle and get the orientation of panels.

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
