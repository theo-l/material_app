# encoding: utf-8
'''
对话框使用方法
'''
import tkinter as tk
import tkMessageBox
import tkFileDialog
import tkSimpleDialog
import tkCommonDialog


def callback():
    if tkMessageBox.askyesno("Verify", "Do you really want to quit?"):
        tkMessageBox.showwarning("Yes", "Quit not yet implemented")
    else:
        tkMessageBox.showinfo("No", "Quit has been cancelled")

errmsg = "Sorry, no Spam allowed!"
tk.Button(text="Quit", command=callback).pack(fill=tk.X)
tk.Button(text="Spam", command=(
    lambda: tkMessageBox.showerror("Spam", errmsg))).pack(fill=tk.X)
tk.mainloop()
