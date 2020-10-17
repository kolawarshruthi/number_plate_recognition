# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:39:06 2020

@author: 91807
"""
import cv2
import torch
from ssd import build_ssd
from data import BaseTransform
from object_detection import detect
from ocr import recognize
import numpy as np
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from tkinter import filedialog
import sqlite3
import os
window=Tk()
window.geometry("1890x830")
window.title("My Project")

imge=Image.open("C:/Users/91807/Downloads/nature2.jpg")
photo=ImageTk.PhotoImage(imge)
lab=Label(image=photo)
lab.pack()


window.resizable(width=True, height=True)

img = None
text = []

def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename

def open_img():
    global img
    x = openfn()
    img2 = Image.open(x)
    img = np.array(img2)
    img2 = img2.resize((300, 300), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)
    panel = Label(window, image=img2)
    panel.image = img2
    panel.place(x = 500, y = 150)

def database():
    global text
    t = ''
    for i in range(len(text)):
        t += text[i][0] + '\n'
    messagebox.showinfo("The Vechile Number", 'The Vechile Numbers detected are:\n' + t)
    conne = sqlite3.connect("final_project.db")
    with conne:
        cursor = conne.cursor()
    for i in range(len(text)):
        try:
            gray= cv2.cvtColor(text[i][1], cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            cursor.execute('CREATE TABLE IF NOT EXISTS Abcd(PlateNumber TEXT primary key, Image BLOB)')
            cursor.execute('INSERT INTO Abcd(PlateNumber, Image) VALUES(?, ?)', (text[i][0], thresh))
            conne.commit()
        except Exception:
            print("This vechile Number is alredy Stored in database")

def call_detect():
    global img, text
    net = build_ssd('test', 300, 3)
    net.load_state_dict(torch.load('ssd300_0712_5000.pth', map_location = lambda storage, loc : storage))
    transform = BaseTransform(net.size, (104/256.0, 117/256.0, 123/256.0))
    new_images = detect(img, net.eval(), transform)
    text = recognize(new_images)

'''
def showresult():
    global text
    messagebox.showinfo("The Vechile Number", 'The Vechile Numbers detected are:\n' + text)
    database()
'''

def exit1():
    exit()

#Lable
label1=Label(window,text="Vechile plate number detection",relief="solid",fg='white',bg='black',font=("",20,""))
label1.place(x=600,y=100)
label1=Label(window,text="Number plate detection is sloved\n by machine learning and by using \nTinker for GUI .",relief="flat",fg='white',bg='black',font=("",17,""))
label1.place(x=600,y=700)

#input
button6 = Button(window, text="INPUT",fg="white",bg="green",font=("",12,""), command=open_img)
button6.place(x=300, y=250)
#detect
button2=Button(window,text="DETECT",relief="solid",fg="white",bg="coral",font=("",12,""),command=call_detect)
button2.place(x=300,y=350)
#show result
button3=Button(window,text="SHOW RESULT",relief="flat",fg="white",bg="brown",font=("",12,""),command=database)
button3.place(x=300,y=450)
#returning to database
window.bind("<Return>",database)

button1=Button(window,text="EXIT",relief="solid",fg="white",bg="red",font=("",12,""),command=exit1)
button1.place(x=300,y=550)
window.mainloop()