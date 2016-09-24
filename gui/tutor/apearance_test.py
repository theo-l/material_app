# encoding: utf-8
import tkinter
from gui.tutor import style

root = tkinter.Tk()
label = tkinter.Label(root, text="Hello Config world")
label.config(style.label_config)
label.pack(expand=tkinter.YES, fill=tkinter.BOTH)
tkinter.mainloop()
