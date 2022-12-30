# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 15:48:39 2022

@author: vlebo
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel, QLineEdit
import sys
from PyQt5.QtGui import QPixmap
import getCards
from time import sleep
import pyautogui
from PIL.ImageQt import ImageQt
import treys as t


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Open File"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.board = []


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
        
        self.textbox = QLineEdit(self)
        self.textbox.setStyleSheet("background-color: rgb(255, 255, 255);")
        vbox.addWidget(self.textbox)
        
        self.btn3 = QPushButton("Show odds")
        self.btn3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btn3.clicked.connect(self.show_odds)
        vbox.addWidget(self.btn3)
        
        self.label3 = QLabel("Score de la main : ")
        vbox.addWidget(self.label3)


        self.setLayout(vbox)

        self.show()

    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\Users\\vlebo\\Documents\\SEMESTRE 7\\Software Engineering', "Image files (*.jpeg *.png)")
        imagePath = fname[0]
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(QPixmap(pixmap))
        self.resize(pixmap.width(), pixmap.height())
        cartes_total = getCards.get_cards_from_screen_link(imagePath)
        cards = cartes_total[0]
        cards.reverse()
        self.board = cartes_total[1]
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
        cartes_total = getCards.get_cards_from_screen_image(myScreenshot)
        cards = cartes_total[0]
        cards.reverse()
        self.board = cartes_total[1]
        self.label2.setText("Cartes : " + str(cards))
        self.label2.setFont(QtGui.QFont('Calibri', 30))
    
    def show_odds(self):
        textboxValue = self.textbox.text()
        liste_hand = textboxValue.split(",")
        cartes = []
        for carte in liste_hand:
            carte_treys = t.Card.new(carte)
            cartes.append(carte_treys)
        board_card = [t.Card.new(i) for i in self.board]
        evaluator = t.Evaluator()
        evaluation = evaluator.evaluate(board_card, cartes)
        evaluation = (7462 - evaluation)/7462
        advice = ""
        if evaluation < 0.8:
            advice = "fold"
        else:
            advice = "call"
        self.label3.setText("Score de la main : " + str(evaluation) + ", advice = " + advice)
        self.label3.setFont(QtGui.QFont('Calibri', 30))
    




App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())