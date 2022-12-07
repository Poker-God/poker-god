# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 15:48:39 2022

@author: vlebo
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel, QTextEdit
import sys
from PyQt5.QtGui import QPixmap
import getCards
from time import sleep
import pyautogui
from PIL.ImageQt import ImageQt


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Open File"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300


        self.InitWindow()


    def InitWindow(self):
        self.setStyleSheet("background-color: rgb(255, 251, 212);")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        vbox = QVBoxLayout()

        self.btn1 = QPushButton("Open Image")
        self.btn1.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btn1.clicked.connect(self.getImage)

        vbox.addWidget(self.btn1)
        
        self.btn2 = QPushButton("Take Screen")
        self.btn2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btn2.clicked.connect(self.prendreScreen)
        vbox.addWidget(self.btn2)


        self.label = QLabel("Hello")
        vbox.addWidget(self.label)
        self.label2 = QLabel("Les cartes sont : ")
        vbox.addWidget(self.label2)


        self.setLayout(vbox)

        self.show()

    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\Users\\vlebo\\Documents\\SEMESTRE 7\\Software Engineering', "Image files (*.jpeg *.png)")
        imagePath = fname[0]
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(QPixmap(pixmap))
        self.resize(pixmap.width(), pixmap.height())
        cards = getCards.get_cards_from_screen_link(imagePath)
        cards.reverse()
        self.label2.setText("Les cartes sont : " + str(cards))
        self.label2.setFont(QtGui.QFont('Calibri', 30))
    
    def prendreScreen(self):
        sleep(2)
        myScreenshot = pyautogui.screenshot()
        qim = ImageQt(myScreenshot)
        pixmap = QPixmap.fromImage(qim)
        pixmap = pixmap.scaled(1600,900)
        self.label.setPixmap(QPixmap(pixmap))
        self.resize(pixmap.width(), pixmap.height())
        cards = getCards.get_cards_from_screen_image(myScreenshot)
        cards.reverse()
        self.label2.setText("Les cartes sont : " + str(cards))
        self.label2.setFont(QtGui.QFont('Calibri', 30))
        
        



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())