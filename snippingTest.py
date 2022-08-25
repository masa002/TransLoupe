from tkinter import ttk
import tkinter

root=tkinter.Tk()
root.wm_attributes("-transparentcolor", "snow")
#root.attributes("-alpha",0.5)
ttk.Style().configure("TP.TFrame", background="snow")
f=ttk.Frame(master=root,style="TP.TFrame",width="1000",height="200")
f.pack()

label=ttk.Label(master=root,text="",foreground="red",background="snow")
label.place(x=150,y=150)
root.mainloop()

