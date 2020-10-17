# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 13:34:21 2020

@author: 91807
"""


import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def recognize(image):
    t = []
    num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for i in range(len(image)):
        text = pytesseract.image_to_string(image[i], lang = 'eng')
        q = ''
        c = 0
        for j in range(len(text)):
            if c == 10:
                break
            if c == 0 or c == 1 or c == 4 or c == 5:
                if text[j].isalpha():
                    q += text[j]
            elif text[j] in num:
                q += text[j]
            c = len(q)
        t.append((q, image[i]))
    return t