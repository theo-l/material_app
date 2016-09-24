# encoding: utf-8

import tkinter as tk

root = tk.Tk()

trees = [("The Larch!", 'light blue'),
         ("The Pine!", 'light green'),
         ("The Giant Redwood!", 'red')
         ]

for (tree, color) in trees:
    win = tk.Toplevel(root)

    win.title('Sing...')
    win.protocol("WM_DELETE_WINDOW", lambda: None)
#     win.iconbitmap('py-blue-trans-out.ico')

    msg = tk.Button(win, text=tree, command=win.destroy)
    msg.pack(expand=tk.YES, fill=tk.BOTH)
    msg.config(padx=10, pady=10, bd=10, relief=tk.RAISED)
    msg.config(bg='black', fg=color, font=('times', 30, 'bold italic'))

root.title("Lumberjack demo")
tk.Label(root, text="Main window", width=30).pack()
tk.Button(root, text="Quit All", command=root.quit).pack()
root.mainloop()
