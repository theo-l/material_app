# encoding: utf-8

import tkinter as tk

import ttk


def demo():
    root = tk.Tk()
    root.title("ttk.Notebook")

    nb = ttk.Notebook(root)

    page1 = ttk.Frame(nb)
    page2 = ttk.Frame(nb)

    nb.add(page1, text="One")
    nb.add(page2, text="Two")

    nb.pack(expand=1, fill=tk.BOTH)
    root.mainloop()

if __name__ == '__main__':
    demo()
