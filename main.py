import os
import sys
import time
import threading

from PIL import ImageGrab
from PIL import Image

import pyocr
import langid
from googletrans import Translator

import tkinter as tk
    

def resourcePath(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(filename)

def ocr(width, height, lang):
    img = ImageGrab.grab(bbox=(width, height, width+100, height+100))
    img.save('screenshot.jpg')

    line_boxs=tools[0].image_to_string(
        img,
        lang=lang,
        builder=pyocr.builders.LineBoxBuilder()
    )

    texts_data = []
    for line_box in line_boxs:
        pos1, pos2 = line_box.position
        text_data = {'text': line_box.content, 'pos1': pos1, 'pos2': pos2}
        texts_data.append(text_data)

    return texts_data

def translate(txt, dest='ja'):
    return translator.translate(txt, dest=dest).text

def main():
    while True:
        try:
            var.get()
            ocr(frame1.winfo_x(), frame1.winfo_y(), 'eng')
        except:
            return
    
    texts_data = ocr('tha')
    i = 0
    while True:
        try:
            print(translate(texts_data[i]['text']))
            i += 1
        except:
            break

def window():
    radio1 = tk.Radiobutton(frame1, text='JPN -> ENG', value=0, variable=var, font=font)
    radio1.place(x=10, y=10)
    radio2 = tk.Radiobutton(frame1, text='ENG -> JPN', value=1, variable=var, font=font)
    radio2.place(x=160, y=10)
    radio3 = tk.Radiobutton(frame1, text='JPN -> THA', value=2, variable=var, font=font)
    radio3.place(x=10, y=50)
    radio4 = tk.Radiobutton(frame1, text='THA -> JPN', value=3, variable=var, font=font)
    radio4.place(x=160, y=50)
    radio5 = tk.Radiobutton(frame1, text='ENG -> THA', value=4, variable=var, font=font)
    radio5.place(x=10, y=90)
    radio6 = tk.Radiobutton(frame1, text='THA -> ENG', value=5, variable=var, font=font)
    radio6.place(x=160, y=90)

    button = tk.Button(frame1, text='click', command=main, font=font)
    button.place(x=100, y=110, width=100)

    frame1.mainloop()

if __name__ == '__main__':
    translator = Translator()

    path = 'C:\\Program Files\\Tesseract-OCR\\'
    os.environ['PATH'] = os.environ['PATH'] + path
    pyocr.tesseract.TESSERACT_CMD = resourcePath("resources/Tesseract-OCR/tesseract.exe")
    
    tools = pyocr.get_available_tools()

    frame1 = tk.Tk()
    var = tk.IntVar()
    var.set(0)
    font = ("Helvetica", 12)
    iconfile = './resources/icon.ico'

    frame1.iconbitmap(default=iconfile)
    frame1.title('TransLoupe') 
    frame1.geometry("300x400")

    langs = ['jpn', 'eng', 'tha']

    thread = threading.Thread(target=main)
    thread.start()

    window()
    thread.join()