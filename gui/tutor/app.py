# encoding: utf-8

import ttk
import tkinter as tk


root = tk.Tk()
btn = tk.Button(root, text="Click", command=root.quit)
btn.pack()
print btn.bindtags()
virtuals = btn.event_info()
for virtual in virtuals:
    print virtual, btn.event_info(virtual)
root.mainloop()
