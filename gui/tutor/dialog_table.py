# encoding: utf-8

import tkinter as tk
from tkFileDialog import askopenfilename
from tkColorChooser import askcolor
from tkMessageBox import askquestion, showerror, askokcancel
from tkSimpleDialog import askfloat

demos = {
    'Open': askopenfilename,
    'Color': askcolor,
    'Query': lambda:  askquestion("Warning", "You typed 'rm *'\n Confirm?"),
    'Error': lambda: showerror('Error!', "He's dead, Jim"),
    'Input': lambda: askfloat("Entry", "Enter credit card number")
}


class Quitter(tk.Frame):

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack()
        widget = tk.Button(self, text="Quit", command=self.quit)
        widget.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

    def quit(self):
        ans = askokcancel("Verify Exit", "Really Quit?")
        if ans:
            tk.Frame.quit(self)


class Demo(tk.Frame):

    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent, **options)
        self.pack()
        tk.Label(self, text="Basic demos").pack()
        for key in demos:
            func = (lambda key=key: self.printit(key))
            tk.Button(self, text=key, command=func).pack(
                side=tk.TOP, fill=tk.BOTH)
        Quitter(self).pack(side=tk.TOP, fill=tk.BOTH)

    def printit(self, name):
        print(name, 'returns =>', demos[name]())

if __name__ == '__main__':
    Demo().mainloop()
