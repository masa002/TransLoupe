import os
import sys
import time
import threading

from PIL import ImageGrab
from PIL import Image

import pyocr
from googletrans import Translator

import tkinter as tk

def resourcePath(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(filename)

def ocr(x, y, lang):
    while True:
        # screenshot
        img = ImageGrab.grab(bbox=(x+5, y+30, x+305, y+60))
        # ocr
        line_boxs=tools[0].image_to_string(img,lang=lang,builder=pyocr.builders.LineBoxBuilder())

        texts = []
        for line_box in line_boxs:
            texts.append(line_box.content)

        return texts

def translate(txt, dest):
    return translator.translate(txt, dest=dest).text

def main():
    old_text = ''
    while True:
        try:
            # get lang setting
            lang = langs[var.get()]
            for text in ocr(frame.winfo_x(), frame.winfo_y(), lang[0]):
                # diff check
                if text != old_text:
                    text = translate(text, lang[1])
                    old_text = text

                    txt.delete(0, tk.END)
                    txt.insert(tk.END, text)

                    time.sleep(0.5)
        except:
            return

        time.sleep(1)

def window():
    # add invisible label
    lbl = tk.Label(background='snow')
    lbl.place(x=0, y=0, width=300, height=30)

    # add radio buttons
    radio1 = tk.Radiobutton(frame, text="JPN -> ENG", value=0, variable=var, font=font)
    radio1.place(x=10, y=90)
    radio2 = tk.Radiobutton(frame, text="ENG -> JPN", value=1, variable=var, font=font)
    radio2.place(x=160, y=90)
    radio3 = tk.Radiobutton(frame, text="JPN -> THA", value=2, variable=var, font=font)
    radio3.place(x=10, y=130)
    radio4 = tk.Radiobutton(frame, text="THA -> JPN", value=3, variable=var, font=font)
    radio4.place(x=160, y=130)
    radio5 = tk.Radiobutton(frame, text="ENG -> THA", value=4, variable=var, font=font)
    radio5.place(x=10, y=170)
    radio6 = tk.Radiobutton(frame, text="THA -> ENG", value=5, variable=var, font=font)
    radio6.place(x=160, y=170)

    # start main loop
    frame.mainloop()


if __name__ == '__main__':
    # translator setting
    translator = Translator()

    # ocr settings
    pyocr.tesseract.TESSERACT_CMD = resourcePath('resources/Tesseract-OCR/tesseract.exe')
    tools = pyocr.get_available_tools()

    # gui settings
    frame = tk.Tk()
    var = tk.IntVar()
    var.set(0)
    font = ('Helvetica', 12)
    iconfile = './resources/icon.ico'
    frame.iconbitmap(default=iconfile)
    frame.title("TransLoupe") 
    frame.geometry('300x250')
    frame.wm_attributes('-transparentcolor', 'snow')
    frame.resizable(0,0)

    # add output label
    txt = tk.Entry()
    txt.place(x=0, y=30, width=300, height=30)

    # def langs
    langs = {0: ['jpn', 'en'], 1: ['eng', 'ja'], 2: ['jpn', 'th'], 3: ['tha', 'ja'], 4: ['eng', 'th'], 5: ['tha', 'en']}

    # create thread and start
    thread = threading.Thread(target=main)
    thread.start()
    window()
    thread.join()