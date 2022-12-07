# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 14:19:16 2022

@author: vlebo
"""

#Import the libraries
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from poker import Suit, Rank, Card


#Some functions to facilitate conversion between the PIL and cv2 image formats
def cv2_to_PIL(img):
    img_convert = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img_convert)
    return im_pil

def PIL_to_cv2(img):
    img_convert = img.convert('RGB')
    im_cv2 = np.array(img_convert)
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

cv2.imwrite("carte.png", PIL_to_cv2(im_cartes[2]))


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
        color = "♥"
    else:
        color = "♦"
    return color

def differentiate_black(PILimg):
    px = PILimg.load()
    color = ""
    if px[8, 41][0] < 100 and px[8, 41][1] < 100 and px[8, 41][2] < 100:
        color = "♠"
    else:
        color = "♣"
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

def getNumber(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Otsu Tresholding automatically find best threshold value
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    
    # invert the image if the text is white and background is black
    count_white = np.sum(binary_image > 0)
    count_black = np.sum(binary_image == 0)
    if count_black > count_white:
        binary_image = 255 - binary_image
        
    # padding
    final_image = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    txt = pytesseract.image_to_string(
        final_image, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')

    return txt

def darken_image(img):
    gray = cv2.cvtColor(PIL_to_cv2(img), cv2.COLOR_BGR2GRAY)
    im_gray = cv2_to_PIL(gray)
    enhancer = ImageEnhance.Brightness(im_gray)
    img2 = enhancer.enhance(1)
    enhancer = ImageEnhance.Contrast(img2)
    img2 = enhancer.enhance(3)
    return img2


def rank_letter(PILimg):
    dark_img = darken_image(PILimg)
    px = dark_img.load()
    if (px[8, 12][0] < 100 and px[8, 12][1] < 100 and px[8, 12][2] < 100
    and px[16, 12][0] < 100 and px[16, 12][1] < 100 and px[16, 12][2] < 100):
        rank = "Q"
    elif (px[8, 12][0] > 200 and px[8, 12][1] > 200 and px[8, 12][2] > 200
    and px[16, 12][0] > 200 and px[16, 12][1] > 200 and px[16, 12][2] > 200):
        rank = "A"
    elif (px[8, 12][0] < 100 and px[8, 12][1] < 100 and px[8, 12][2] < 100
    and px[16, 12][0] > 200 and px[16, 12][1] > 200 and px[16, 12][2] > 200):
        rank = "K"
    elif (px[8, 12][0] > 200 and px[8, 12][1] > 200 and px[8, 12][2] > 200
    and px[16, 12][0] < 100 and px[16, 12][1] < 100 and px[16, 12][2] < 100):
        if (px[10, 12][0] < 100 and px[10, 12][1] < 100 and px[10, 12][2] < 100):
            rank = "A"
        else:
            rank = "J"
    else:
        rank = "T"
    return rank
    
cmpt = 1
for i in im_cartes:
    s = symbol(i)
    im2 = i
    screen_crop = im2.crop((3,3, 25,30))
    img2 = screen_crop
    img2 = np.array(img2)
    rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\vlebo\AppData\Local\Tesseract-OCR\tesseract.exe"
    nbr = getNumber(rgb)
    nbr = nbr.replace("\n","")
    if nbr == "":
        nbr = rank_letter(i)
    elif nbr == "0":
        nbr = "T"
    card = Card(nbr+s)
    print(card)
    
    
    



 

    