# encoding: utf-8

import Tkinter as tk
import tkMessageBox
import ttk

_PRE_PAGE = "pre"
_NEXT_PAGE = "next"
_PRE_LOGO = '<'
_NEXT_LOGO = '>'
ENCODING = 'utf-8'


def add_horizontal_separator(parent, columnspan, row):
    "创建一个空白行和水平分割符"
    ttk.Label(parent, padding=2).grid(row=row, columnspan=columnspan)
    ttk.Separator(parent, orient=tk.HORIZONTAL).grid(
        row=row + 1, columnspan=columnspan, sticky=tk.E + tk.W)


def add_horizontal_space(parent, columnspan, row):
    ttk.Label(parent, padding=2).grid(row=row, columnspan=columnspan)


def make_pagination_button(root, text, row, column, flag, handler):
    "创建通用导航按钮"
    btn = ttk.Button(root, text=text)
    if flag == _PRE_PAGE:
        btn.config(command=handler)
    elif flag == _NEXT_PAGE:
        btn.config(command=handler)
    btn.grid(row=row, column=column)
    return btn


def makePreButton(root, row, column, handler=None):
    "创建上一页导航按钮"

    if handler is None:
        handler = root._pre_page
    return make_pagination_button(root, _PRE_LOGO,  row, column, _PRE_PAGE, handler=handler)


def makeNextButton(root, row, column, handler=None):
    "创建下一页导航按钮"
    if handler is None:
        handler = root._next_page
    return make_pagination_button(root, _NEXT_LOGO,  row, column, _NEXT_PAGE, handler=handler)
