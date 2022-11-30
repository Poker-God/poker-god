# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 14:19:16 2022

@author: vlebo
"""

#Import the libraries
from PIL import Image
import cv2
import numpy
import matplotlib.pyplot as plt
import pyautogui

#Some functions to facilitate conversion between the PIL and cv2 image formats
def cv2_to_PIL(img):
    img_convert = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img_convert)
    return im_pil

def PIL_to_cv2(img):
    img_convert = img.convert('RGB')
    im_cv2 = numpy.array(img_convert)
    im_cv2 = im_cv2[:, :, ::-1].copy()
    return im_cv2


#Get the screenshot, and crop it to only include the cards (5 max)
screen = Image.open(r"C:\Users\vlebo\Documents\SEMESTRE 7\Software Engineering\Screen Poker\screen_cards.jpeg")
#screen_crop = screen
screen_crop = screen.crop((500,420, 880, 520))
#screen_crop.show()


#Convert to a OpenCV-compatible format 
opencv_image = PIL_to_cv2(screen_crop)


#Convert the image to one with only black or white pixels
gray_img = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
#blur_img = cv2.GaussianBlur(gray_img,(5,5),0)
thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#cv2.imshow('Gris', thresh_img)
#cv2.waitKey()


#Get the contours of the image, draw them on the image to show they are correct
allcontours = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = allcontours[0]
cv2.drawContours(opencv_image, contours, -1, (255,255,0), 3)


#Crop the original cropped image to get each card individually in an image file
im_cartes = []
for i in contours:
    left = [x[0][0] for x in i]
    bottom = [x[0][1] for x in i]
    minleft = min(left)
    maxleft = max(left)
    minbottom = min(bottom)
    maxbottom = max(bottom)
    #print(minleft,minbottom, maxleft, maxbottom)
    im_temp = screen_crop.crop((minleft,minbottom, maxleft, maxbottom))
    im_cartes.append(im_temp)

for i in range(len(im_cartes)):
    im_cartes[i] = cv2_to_PIL(cv2.resize(PIL_to_cv2(im_cartes[i]), (76,100), interpolation = cv2.INTER_AREA))
    plt.imshow(im_cartes[i])
    plt.show()

cv2.imwrite("carte.png", PIL_to_cv2(im_cartes[0]))
spade = cv2.imread(r"C:\Users\vlebo\Documents\SEMESTRE 7\Software Engineering\Symboles 2\spade.png")
diamond = cv2.imread(r"C:\Users\vlebo\Documents\SEMESTRE 7\Software Engineering\Symboles 2\diamond.png")
club = cv2.imread(r"C:\Users\vlebo\Documents\SEMESTRE 7\Software Engineering\Symboles 2\club.png")
heart = cv2.imread(r"C:\Users\vlebo\Documents\SEMESTRE 7\Software Engineering\Symboles 2\heart.png")

symbols = [spade, diamond, club, heart]


def differentiate_red_black(PILimg):
    px = PILimg.load()
    color = ""
    if px[13,44][0] > 200 and px[13,44][1] < 100 and px[13,44][2] < 100:
        color = "red"
    elif px[13,44][0] <10 and px[13,44][1] < 10 and px[13,44][2] < 10:
        color = "black"
    else:
        color = "unknown"
    return color

def differentiate_red(PILimg):
    px = PILimg.load()
    color = ""
    if px[7,36][0] > 200 and px[7,36][1] < 100 and px[7,36][2] < 100:
        color = "heart"
    else:
        color = "diamond"
    return color

def differentiate_black(PILimg):
    px = PILimg.load()
    color = ""
    if px[8, 41][0] < 100 and px[8, 41][1] < 100 and px[8, 41][2] < 100:
        color = "spade"
    else:
        color = "club"
    return color

def symbol(PILimg):
    color = differentiate_red_black(PILimg)
    if color == "red":
        symbol = differentiate_red(PILimg)
    elif color == "black":
        symbol = differentiate_black(PILimg)
    else:
        symbol = "unknown"
    return symbol

for i in im_cartes:
    print(symbol(i))




 

    