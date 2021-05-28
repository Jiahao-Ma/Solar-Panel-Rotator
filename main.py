from io import BytesIO
from altair.vegalite.v4.schema.core import Root
import streamlit as st
import os, copy
import numpy as np
from PIL import Image
from tool import bbox2cntwh, vis_bbox, getBBox, plot_orientation, rotate_bound
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg


def show_original_image(ROOT, folder, file):
    cli_width = st.slider('Adjust Image Size:', 128, 512, 128)
    st.markdown("** Before Rotate **")
    clip_image_path = os.path.join(ROOT, folder, file)
    cli_image = np.array(Image.open(clip_image_path))
    st.image(cli_image, caption='{}'.format(clip_image_path), width=cli_width)
    if st.checkbox('Show/Hidden Original Image Size:'):
        st.write('Original Image\'s height: ', cli_image.shape[0], ' width: ',cli_image.shape[1])
    return cli_image, cli_width

def show_clip_image(cli_image, cli_width):
    st.markdown("** After Rotate **")
    ro_angle = st.slider('Angle:', 0, 360, 0)
    rotate_image = rotate_bound(cli_image, ro_angle)
    rotate_image_ori = copy.copy(rotate_image)
    # draw red line in middle
    rotate_image[rotate_image.shape[0]//2, :, :] = [255, 0, 0]
    rotate_image[int(rotate_image.shape[0]/5), :, :] = [0, 255, 0]
    rotate_image[int(rotate_image.shape[0]*4/5), :, :] = [0, 255, 0]
    
    st.image(rotate_image, caption='Rotated Result', width=cli_width)
    if st.checkbox('Show/Hidden Rotated Image Size:'):
        st.write('Rotated Image\'s height: ', rotate_image.shape[0], ' width: ',rotate_image.shape[1])
    return rotate_image_ori, ro_angle

def download_image(image, name):
    """Generates a link allowing the PIL image to be downloaded
	in:  PIL image
	out: result(bool): determine if download success
	"""
    buffered = BytesIO()
    try:
        image.save(name)
        return True
    except:
        return False

def Islabel(file, filelist):
    """ Judge if the image has been labeled
    """
    file = os.path.basename(file)
    for f in filelist:
        f = os.path.basename(f)
        if len(f.split('_')) == 5 and f[:len(file.split('.')[0])] == file.split('.')[0]:
            return True
    return False

def IsAlllabel(filelist):
    """ Judge if all the images of folders are label
    """
    ori_img_num = 0
    rotate_img_num = 0
    for f in filelist:
        f = os.path.basename(f)
        if len(f.split('_')) == 5:
            rotate_img_num += 1
        elif len(f.split('_')) == 4:
            ori_img_num += 1 
    if ori_img_num == rotate_img_num:
        return True
    else:
        return False

def TraverseImageFolder(path):
# Before rendering the website, traverse all the pictures to determine whether they have been label
    score = 0
    for p in os.listdir(path):
        if len(p.split('_')) == 4:
            score += 1
            continue
        else:
            if len(os.listdir(os.path.join(path,p))) == 0:
                c_p = 'N_' + p
                os.rename(os.path.join(path, p), os.path.join(path, c_p))

            elif IsAlllabel(os.listdir(os.path.join(path,p))):
                c_p = 'L_' + p
                os.rename(os.path.join(path, p), os.path.join(path, c_p))
    return score

ROOT = r'.\datasets'
###################################
# Refresh folder and Show process
###################################
score = TraverseImageFolder(ROOT)
st.sidebar.title('Score: {} / {}'.format(score, len(os.listdir(ROOT))))
st.sidebar.progress(score/len(os.listdir(ROOT)))

    

###################################
# Title, markdown, introduction
###################################
html_temp = """
<div style="background-color:tomato;padding:5px;id=center">
<h2 style="text-align:center"> <b>Image Rotator Explorer</b></h2>
</div>
"""
st.markdown(html_temp, unsafe_allow_html=True)

###################################
# Set dataset path
###################################
# Determine input dataset
st.title('Panel Rotator')
st.subheader("""
This app, built with streamlit, performs simple rotate operation on input images.  :sunglasses:
""")
st.header('Determine Input Dataset')
st.write('This sectoin mainly shows the precaution for rotation when labeling. Firstly, you neeed to input the Datatset Location or single image location.')

###################################
# Set default folder
###################################
st.sidebar.title('User Dataset Input')

ROOT = st.sidebar.text_input('Default Dataset Folder:', '{}'.format(ROOT))
if not os.path.exists(ROOT):
    st.error('No such folder')

folder_lists = os.listdir(ROOT)
st.sidebar.write('This Dataset Folder has ', len(folder_lists), ' Images. \n')

# shuffle?
# if st.button('Shuffle'):
#     random.shuffle(folder_lists)

###################################
# Set data foulder
###################################
folder = st.sidebar.selectbox('Solar Panel Dataset Folder:',folder_lists)
st.sidebar.write('Selected Dataset:', folder)

###################################
# Set image
###################################
file_lists = os.listdir(os.path.join(ROOT, folder))
file = st.sidebar.selectbox('List images of folder:', file_lists)
if len(file_lists) == 0:
    st.warning('This folder is empty. Select another folder')
else:
    st.write('Image comes from ', os.path.join(ROOT, folder, file))

###################################
# Set single image path
###################################
st.subheader('If you don\'t have a dataset in this format, offered by Marko. Select checkbox below and input your image path. ')
if st.checkbox('Input single image path'):
    # single_img_path = st.text_input('Image Path:', '')
    st.error('This function disappears.')

st.header('Image Rotate')
st.write('This sectoin mainly shows the results of rotation when labeling. Select the width of image and adjust the rotation angle.')

###################################
# hidden original image
###################################
Original_Path = r'F:\SOLAR\data\Perth\Images'
Original_Path = st.text_input('Original Image Path:', '{}'.format(Original_Path))
ori_image_lists = os.listdir(Original_Path)
if len(folder.split('_')) == 4:
    showing_image = folder[2:] + '.jpg'
else:
    showing_image = folder + '.jpg'
if not st.checkbox('Hidden Original Image'):
    if showing_image in ori_image_lists:
        p = os.path.join(Original_Path, showing_image)
        ori_width = st.slider('Width:', 512, 128)
        st.image(Image.open(p), caption='{}'.format(showing_image), width=ori_width)

###################################
# next? or previous?
###################################
st.write('The Number of Images in this folder: ', len(file_lists))
if len(file_lists) == 0:
    index = 0
else:
    index = len(file_lists)
index = st.sidebar.number_input('Select your image by serial number', min_value=1, max_value=index)
# if no files in this folder, return None
try:
    file = file_lists[index-1]
except:
    file = 'None'
st.write('Image path:  ', '* {} *'.format(os.path.join(ROOT, folder, file)))
IsDownload = False
if len(file.split('_')) == 5:
    st.info('This image is labeled result!')
    IsDownload = True
elif Islabel(file, file_lists):
    st.info('This image is labeled!')
    IsDownload = True

###################################
# hidden original image
###################################
if len(file_lists) == 0:
    st.error("No Image to be showed.")
else:
    
    st.write('\n\n')
    
    cli_image, cli_width = show_original_image(ROOT, folder, file)
    ro_image, ro_angle = show_clip_image(cli_image, cli_width)
    
    if st.button('Download'):
        if not IsDownload:
            save_name = os.path.basename(file).split('.')[0] + "_{}.jpg".format(ro_angle)
            save_path = os.path.join(ROOT, folder, save_name)
            result = download_image(Image.fromarray(ro_image), save_path)
            if result:
                st.success('{} saved successfully'.format(save_path))
            else:
                st.error('Download Failed.')
        else:
            st.warning('This Image is labeled result. Can not download again!')
    
st.title('Steps of Orientation Prediction')
st.subheader("""
This section mainly show the main steps of panels orientation prediction. There are four main steps, including:
""")
st.markdown(" * (1) Predict solar panel.")
st.markdown(" * (2) Cut the target from the image.")
st.markdown(" * (3) Predict rotation angle.")
st.markdown(" * (4) Adjust rotation angle and get the orientation of panels.")

#########################################
#          Adjust predict image
#########################################
st.sidebar.title('Orientation Predict')
pred_image_width = st.sidebar.select_slider('Select Predict Image Width', options=[256, 512, 640], value=512)
Fill_up_the_screen = st.sidebar.checkbox('Fill up the screen')


Original_Path = r'F:\SOLAR\data\Perth\Images'
ori_image_lists = os.listdir(Original_Path)

if len(folder.split('_')) == 4:
    predict_image = folder[2:] + '.jpg'
else:
    predict_image = folder + '.jpg'


#########################################
#         Show original image
#########################################
if showing_image in ori_image_lists:    
    p = os.path.join(Original_Path, predict_image)
    st.header('Original Image')
    st.image(Image.open(p), caption='{}'.format(predict_image), width=pred_image_width, use_column_width=Fill_up_the_screen)

#########################################
#         Get predict bbox
#########################################
bbox = getBBox(os.path.join(ROOT, folder))
bbox_cnt, bbox_wh = bbox2cntwh(bbox)

#########################################
#  (1)Show image with predicted bboxes
#########################################
# define default parameters
if st.sidebar.checkbox('Step1: Draw Settings'):
    st.sidebar.markdown('** Line Width and Text Size Adjust: **')
    line_width = st.sidebar.select_slider('Line Width:', options=[0.2, 0.5, 0.8, 1, 1.2, 1.5, 1.8, 2], value=1)
    text_size = st.sidebar.slider('Text Size:', min_value=1, max_value=8, value=4)
else:
    line_width = 1
    text_size = 4
if st.checkbox('Step1: Predict solar panel'):

    if len(bbox_cnt) == 0:
        st.warning('This image has no solar panel.')
    else:
        
        pred_img_bbox = vis_bbox(Image.open(p), bbox_cnt, bbox_wh, line_width=line_width, text_size=text_size)

        st.image(pred_img_bbox, caption='', width=pred_image_width, use_column_width=Fill_up_the_screen)

#########################################
#  (2) Crop image
#########################################
if st.sidebar.checkbox('Step2: Draw Settings'):
    crop_img_width = st.sidebar.slider('Crop Image Size:', min_value=30, max_value=80, value=50)
else:
    crop_img_width = 50
if st.checkbox('Step2: Cut the target from the image.'):
    if len(file_lists) == 0:
        st.error('This image has no solar panels.')
    else:
        for file in file_lists:
            if len(file.split('_')) == 4:
                cut_img_p = os.path.join(ROOT, folder, file)
                st.image(Image.open(cut_img_p), caption=p, width=crop_img_width)

#########################################
#  (3) Rotation angle predict
#########################################   
if st.sidebar.checkbox('Step3,4: Draw Settings'):
    LINE_LEN = st.sidebar.slider('Line Length:', min_value=30, max_value=50, value=40, step=1)
    color1 = st.sidebar.selectbox('Base Line Endpoint Color', options=['red', 'blue', 'yellow', 'purple', 'black'])
    color2 = st.sidebar.selectbox('Rotate Line Endpoint Color', options=['red', 'blue', 'yellow', 'purple', 'black'])
    scale1 = st.sidebar.select_slider('Base Point Size', options=[0.2, 0.5, 0.8, 1.0, 1.5, 2.], value=1.0)
    scale2 = st.sidebar.select_slider('Rotate Point Size', options=[0.2, 0.5, 0.8, 1.0, 1.5, 2.], value=1.0)
    line_width = st.sidebar.select_slider('Line Width',options=[0.2, 0.5, 0.8, 1.0, 1.5, 2.], value=1.0)
else:
    LINE_LEN=40
    color1='red'
    color2='blue'
    scale1=1.0
    scale2=1.5
    line_width=1.0

if st.checkbox('Step3: Predict rotation angle.'):
    if len(file_lists) == 0:
        st.error('This image has no solar panels.')
    else:
        file_lists_with_angle = [ p for p in file_lists if len(p.split('_')) == 5]
        if len(file_lists_with_angle) == 0:
            st.warning('No any angle predict results.')
        else:
            pred_img_orien = Image.open(p)
            pred_img_orien = plot_orientation(pred_img_orien, file_lists_with_angle, LINE_LEN=LINE_LEN, c1=color1, c2=color2, 
                                            scale1=scale1, scale2=scale2, line_width=line_width, draw_orientaion=False, draw_base_line = True)
            st.image(pred_img_orien, caption='Predict Rotate Angle', 
                    width=pred_image_width, use_column_width=Fill_up_the_screen)

#########################################
#  (3) Predict Orientation of panel
#########################################               
if st.checkbox('Step4: Predict orientation of panel'):
    if len(file_lists) == 0:
        st.error('This image has no solar panels.')
    else:
        file_lists_with_angle = [ p for p in file_lists if len(p.split('_')) == 5]
        if len(file_lists_with_angle) == 0:
            st.warning('No any angle predict results.')
        else:
            col1, _, _, col2 = st.beta_columns(4)
            with col2:
                draw_base_line = not st.checkbox('Hide Base Line')
            pred_img_orien = Image.open(p)
            pred_img_orien = plot_orientation(pred_img_orien, file_lists_with_angle, LINE_LEN=LINE_LEN, c1=color1, c2=color2, 
                                            scale1=scale1, scale2=scale2, line_width=line_width, draw_orientaion=True, draw_base_line = draw_base_line)
            with col1:
                st.image(pred_img_orien, caption='Draw Orientation', 
                        width=pred_image_width, use_column_width=Fill_up_the_screen)
    