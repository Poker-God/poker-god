# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 16:15:54 2022

@author: theol
"""
import cv2 
import pytesseract
import numpy as np
import pyautogui
from time import sleep
import matplotlib.pyplot as plt
from matplotlib import image

def getNumber(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Otsu Tresholding automatically find best threshold value
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    
    # invert the image if the text is white and background is black
    count_white = np.sum(binary_image > 0)
    count_black = np.sum(binary_image == 0)
    if count_black > count_white:
        binary_image = 255 - binary_image
        
    # padding
    final_image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    txt = pytesseract.image_to_string(
        final_image, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')

    return txt

cptr = 0
while(1):
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'C:\Users\theol\file name.png')
    img = cv2.imread(r'C:\Users\theol\file name.png')
    
    img2 = img[450:700,90:250]
    plt.imshow(img2)
    rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    nbr = getNumber(rgb)
    print("nombre = "+ nbr) # Avec l'algorithme qui repère mieux les nombres
    ouich =  pytesseract.image_to_string(img2)
    print("Autre = "+ouich) # Avec l'algorithme qui repère mieux les lettres ( marche pas lui)
    sleep(1)
    cptr+=1
    plt.show()
    print(cptr)