# encoding: utf-8

import Tkinter as tk
import tkMessageBox
import ttk
import re
import gui.messages as _
from gui.constants import  PRE_PAGE, PRE_LOGO, NEXT_PAGE, NEXT_LOGO, ENCODING




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
    if flag == PRE_PAGE:
        btn.config(command=handler)
    elif flag == NEXT_PAGE:
        btn.config(command=handler)
    btn.grid(row=row, column=column)
    return btn


def make_pre_button(root, row, column, handler=None):
    "创建上一页导航按钮"

    if handler is None:
        handler = root._pre_page
    return make_pagination_button(root, PRE_LOGO, row, column, PRE_PAGE, handler=handler)


def make_next_button(root, row, column, handler=None):
    "创建下一页导航按钮"
    if handler is None:
        handler = root._next_page
    return make_pagination_button(root, NEXT_LOGO, row, column, NEXT_PAGE, handler=handler)


def split_csv_line(line):
    '''
    method used to split csv file's line by common seperators
    :param line:
    :return:
    '''
    return [item.strip(' \n').decode(ENCODING) for item in re.split('[,:;\t]', line)]


def parse_material_file_title_index(material_fields):
    '''
    parse material csv file to get titles corresponding index to upload Material object
    :param material_fields:
    :return:
    '''
    material_name_index, material_type_index = (None, None)
    for (index, field_name) in enumerate(material_fields):
        if field_name == _.material_name_field:
            material_name_index = index
        if field_name == _.material_type_field:
            material_type_index = index

    if not material_name_index or not material_type_index:
        tkMessageBox.showwarning(_.material_upload_error_title, _.material_upload_error_msg)

    return (material_name_index, material_type_index)


# 整数Entry值验证器
def int_validator(action, index, text):
    print(action, index, text)
    if not text:
        return True

    if not text.isdigit():
        tkMessageBox.showwarning(_.material_count_warning_title, _.material_count_non_num_msg % text)
        return False

    if int(text) == 0:
        tkMessageBox.showwarning(_.material_count_warning_title, _.material_count_le_zero_warning_msg)
        return False
    return True
