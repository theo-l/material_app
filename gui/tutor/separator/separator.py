# encoding: utf-8

import ttk
import Tkinter as tk

root = tk.Frame()

# for i in xrange(10):
#     tk.Entry(root).grid(row=i, column=1)

# ttk.Label(root, width=2).grid(column=2, rowspan=10)
ttk.Separator(root, orient=tk.VERTICAL).grid(pady=1,
                                             column=0, rowspan=10, sticky=tk.N + tk.S)
# ttk.Label(root, padding=2).grid(row=0, columnspan=10)
# ttk.Separator(root, orient=tk.HORIZONTAL).grid(
#     row=1, columnspan=10, sticky=tk.W + tk.E)
# ttk.Label(root, padding=2).grid(row=2, columnspan=10)


root.grid()


root.mainloop()
