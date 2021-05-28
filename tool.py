import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
import streamlit as st
import os, math, cv2

def vis_image(img, ax=None):
    if ax == None:
        # fig = plt.figure(figsize=(15,10))
        fig = plt.figure()
        fig.set_tight_layout(True)
    ax = fig.gca()
    img = np.array(img)
    ax.imshow(img.astype(np.uint8))
    return fig, ax

@st.cache(persist=True)
def getBBox(path:str):
    bbox = list()
    for p in os.listdir(path):
        if len(p.split('_')) == 4:
            x1, y1, x2, y2 = p.split('.')[0].split('_')
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            bbox.append([x1, y1, x2, y2])
    return bbox

@st.cache(persist=True)
def vis_bbox(img, bbox_cnt, bbox_wh, label='panel', ax=None, line_width=1, text_size=5):
    
    if len(bbox_cnt) == 0:
        return img

    if ax == None:
        fig = plt.figure(figsize=(15,15), dpi=300)
        fig.set_tight_layout(True)

    ax = fig.gca()
    img = np.array(img)
    H,W,C = img.shape
    ax.imshow(img.astype(np.uint8))
    fig.set_size_inches(W/300., H/300.)
    plt.gca().xaxis.set_major_locator(plt.NullLocator()) 
    plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0) 
    plt.margins(0,0)

    canvas = FigureCanvasAgg(fig)
    
    for i, (cnt, wh) in enumerate(zip(bbox_cnt, bbox_wh)):
        width = wh[0]
        height = wh[1]
        x = int(cnt[0] - width/2)
        y = int(cnt[1] - height/2)
        xy = [x, y]
        ax.add_patch(plt.Rectangle(xy, width, height, fill = False, edgecolor='red', linewidth=line_width))

        caption = list()
        if label:
            caption.append(label)
        if len(caption) > 0:
            ax.text(xy[0], xy[1],
                    ':'.join(caption),
                    style='italic',
                    size=text_size,
                    bbox={'facecolor':'white', 'alpha':0.5, 'pad':0})
    
    canvas.draw()
    buf = canvas.buffer_rgba()
    return np.array(buf)

@st.cache(persist=True)
def bbox2cntwh(bbox:list):
    cnt = list()
    wh = list()
    for bb in bbox:
        x = (bb[0] + bb[2]) // 2
        y = (bb[1] + bb[3]) // 2
        cnt.append([x, y])
        w = bb[2] - bb[0]
        h = bb[3] - bb[1]
        wh.append([w, h])
    return cnt, wh


def xywh_angle(p:str):
    x1, y1, x2, y2, angle = p.split('.')[0].split('_')
    x1, y1, x2, y2, angle = int(x1), int(y1), int(x2), int(y2), int(angle)
    x = (x1 + x2) // 2
    y = (y1 + y2) // 2
    w = (x2 - x1)
    h = (y2 - y1)
    return x, y, w, h, angle 

def rotate(ori_p:list, p2:list, angle:float, mode='Counterclockwise'):
    x1, y1 = ori_p
    x2, y2 = p2
    if mode == 'Counterclockwise':
        new_x = (x2 - x1) * math.cos(angle * math.pi / 180) + (y2 - y1) * math.sin(angle * math.pi / 180) + x1
        new_y = (y2 - y1) * math.cos(angle * math.pi / 180) - (x2 - x1) * math.sin(angle * math.pi / 180) + y1
        return [new_x, new_y]
    elif mode == 'Clockwise':
        new_x = (x2 - x1) * math.cos(angle * math.pi / 180) - (y2 - y1) * math.sin(angle * math.pi / 180) + x1
        new_y = (y2 - y1) * math.cos(angle * math.pi / 180) + (x2 - x1) * math.sin(angle * math.pi / 180) + y1
        return [new_x, new_y]

def plot_orientation(img, CropImageLists, LINE_LEN=40, c1='red', c2='blue', 
    scale1=15, scale2=20, line_width=2.5, draw_orientaion=False, draw_base_line=True):

    fig = plt.figure(figsize=(15,15), dpi=300)
    fig.set_tight_layout(True)

    ax = fig.gca()
    img = np.array(img)
    H,W,C = img.shape
    ax.imshow(img.astype(np.uint8))
    fig.set_size_inches(W/300., H/300.)
    plt.gca().xaxis.set_major_locator(plt.NullLocator()) 
    plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0) 
    plt.margins(0,0)

    canvas = FigureCanvasAgg(fig)

    for p in CropImageLists:
        x, y, w, h, angle = xywh_angle(p)
        x1, y1 = x, y
        x2 = x1 + LINE_LEN
        y2 = y1
        x3, y3 = rotate([x1, y1], [x2, y2], angle = angle, mode = 'Counterclockwise')

        if draw_base_line:
            #draw base line
            ax.scatter([x1, x2],[y1, y2], c=c1, s=scale1)
            ax.plot([x1, x2], [y1, y2], linewidth=line_width, color=c1)
            #draw rotate line
            ax.scatter([x1, x3],[y1, y3], c=c1, s=scale1)
            ax.plot([x1, x3], [y1, y3], linewidth=line_width, color=c1)

        #draw orientaion
        if draw_orientaion:
            x4, y4 = rotate([x1, y1], [x3, y3], angle = 90.0, mode = 'Counterclockwise')
            ax.scatter([x1, x4],[y1, y4], c=c2, s=scale2)
            ax.plot([x1, x4], [y1, y4], linewidth=line_width, color=c2)
            x5, y5 = rotate([x1, y1], [x3, y3], angle = -90.0, mode = 'Counterclockwise')
            ax.scatter([x1, x5],[y1, y5], c=c2, s=scale2)
            ax.plot([x1, x5], [y1, y5], linewidth=line_width, color=c2)
    
    canvas.draw()
    buf = canvas.buffer_rgba()
    return np.array(buf)


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))