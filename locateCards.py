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
screen = Image.open(r"C:\Users\vlebo\Desktop\Screen Poker\screen_cards.jpeg")
screen_crop = screen.crop((500,420, 880, 520))
#screen_crop.show()


#Convert to a OpenCV-compatible format 
opencv_image = PIL_to_cv2(screen_crop)


#Convert the image to one with only black or white pixels
gray_img = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
#blur_img = cv2.GaussianBlur(gray_img,(5,5),0)
thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
cv2.imshow('Gris', thresh_img)
cv2.waitKey()


#Get the contours of the image, draw them on the image to show they are correct
allcontours = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = allcontours[0]
cv2.drawContours(opencv_image, contours, -1, (0,255,0), 3)


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

for i in im_cartes:
    plt.imshow(i)
    plt.show()

cv2.imwrite("carte.png", PIL_to_cv2(im_cartes[0]))
spade = cv2.imread(r"C:\Users\vlebo\Desktop\Symbole\spade.jpeg")
diamond = cv2.imread(r"C:\Users\vlebo\Desktop\Symbole\diamond.jpeg")
club = cv2.imread(r"C:\Users\vlebo\Desktop\Symbole\club.jpeg")
heart = cv2.imread(r"C:\Users\vlebo\Desktop\Symbole\heart.jpeg")

symbols = [spade, diamond, club, heart]

for s in symbols:
    res = cv2.matchTemplate(PIL_to_cv2(im_cartes[0]), s, cv2.TM_SQDIFF_NORMED)
    threshold = .1
    loc = numpy.where(res >= threshold)
    print(loc)



 

    