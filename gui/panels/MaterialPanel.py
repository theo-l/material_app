# encoding: utf-8
'''
材料管理控制面板类
'''
import ttk
import tkFileDialog
import tkMessageBox
from gui.panels.BasePanel import ControlPanel
from gui import util
from gui import messages as _
from gui.constants import MAX_TABLE_ROW

from model import MATERIAL_UTIL, Material


class MaterialPanel(ControlPanel):
    '''
    材料控制面板
    1. 从文件导入材料信息
    2. 显示材料信息表格

    '''

    def __init__(self, master):
        ControlPanel.__init__(self, master)
        self.bind('<Enter>', self.enter_handler)

        self.paint_panel()

    def enter_handler(self, event):
        self._fresh_page_data()

    def i_get_page_table_titles(self):
        return _.material_table_titles

    def i_get_page_obj_count(self):
        return MATERIAL_UTIL.getCount()

    def i_get_current_page_objs(self):
        start = (self.current_page - 1) * MAX_TABLE_ROW
        end = start + MAX_TABLE_ROW
        return MATERIAL_UTIL.getAllObjects()[start:end]

    def i_fill_page_data_table(self):
        for (row, obj) in enumerate(self.page_objs):
            rowData = self.page_table_entry_values[row]
            objFields = obj.get_ui_list()
            for col in xrange(self.max_table_col):
                rowData[col].set(objFields[col])

    def i_paint_main_head(self):
        ttk.Button(
            self, text=_.material_file_upload, command=self.__import_material_from_file).grid(row=1, column=0)

#         ttk.Button(self, text=_.refresh, command=self._fresh_page_data).grid(
#             row=mainHeadRow, column=2)

    def __import_material_from_file(self):
        materialFile = tkFileDialog.askopenfile(mode="r")

        if materialFile is None:
            return

        emptyLinePassed = False
        titleLineFound = False
        materialNameIndex = None
        materialTypeIndex = None
        import re
        for line in materialFile.readlines():
            fields = [item.strip(" \n").decode(util.ENCODING)
                      for item in re.split("[,;:]", line)]
            if not any(fields) and not emptyLinePassed:
                continue

            if not titleLineFound:
                materialNameIndex, materialTypeIndex = self.__check_title_line(
                    fields)
                if materialNameIndex and materialTypeIndex:
                    emptyLinePassed = True
                    titleLineFound = True
                    continue
                else:
                    return
            self.__process_material_line(
                fields, materialNameIndex, materialTypeIndex)

        MATERIAL_UTIL.commit()
        tkMessageBox.showinfo(
            _.material_upload_info_title, _.material_upload_info_msg)
        self.init_dynamic_data()

    def __check_title_line(self, fields):
        nameIndex, typeIndex = (None, None)
        for (index, field) in enumerate(fields):
            if field == _.material_name_field:
                nameIndex = index
            if field == _.material_type_field:
                typeIndex = index

        if nameIndex and typeIndex:
            return (nameIndex, typeIndex)
        else:
            tkMessageBox.showwarning(
                _.material_upload_error_title, _.material_upload_error_msg)

    def __process_material_line(self, fields, nameIndex, typeIndex):
        mateial = Material.new_(fields[nameIndex], fields[typeIndex])
        MATERIAL_UTIL.add(mateial)
