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
from gui.constants import MAX_TABLE_ROW, MATERIAL_SEARCH

from model import MATERIAL_UTIL, Material



def process_material_line(material_fields, name_index, type_index):
    material = Material.new_(material_fields[name_index], material_fields[type_index])
    MATERIAL_UTIL.add(material)

class MaterialPanel(ControlPanel):
    '''
    材料控制面板
    1. 从文件导入材料信息
    2. 显示材料信息表格
    3. Create material object
    4. search material object by name/type

    '''

    def __init__(self, master):
        ControlPanel.__init__(self, master)
        self.bind('<Enter>', self._enter_handler)
        # Material control panel only works with Material model
        self.search_type_var.set(MATERIAL_SEARCH)

    def i_paint_main_head(self):

        upload_button = ttk.Button(
            self.main_canvas, text=_.material_file_upload, command=self.__import_material_from_file)
        self.main_canvas.create_window(50, self.header_widget_current_y, window=upload_button)

        # a horizontal line
        self.main_canvas.create_line(0, 60, 300, 60)
        self.header_widget_current_y = 85
        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, _.material_name_label, width=60)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_name_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y
        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, _.material_type_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_new_type_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y
        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, _.material_unit_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_unit_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y
        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, _.material_count_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_count_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y
        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, _.material_price_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_price_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y
        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, _.material_note_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_note_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        submit_button = ttk.Button(self.main_canvas, text=_.create, command=self._create_material)
        self._create_widget(50, self.header_widget_current_y, submit_button)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.cancel_submit_button)

        # seperator between create and search
        self.main_canvas.create_line(0, 320, 300, 320)

        self.header_widget_current_y = 340
        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, _.search_key_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.search_key_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y
        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, _.material_type_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.search_material_type_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y
        self._create_widget(50, self.header_widget_current_y, self.search_button)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.reset_button)

        self.main_canvas.create_line(300, 0, 300, 600)

    def __import_material_from_file(self):
        materialFile = tkFileDialog.askopenfile(mode="r")

        if materialFile is None:
            return

        empty_line_passed = False
        title_line_found = False
        material_name_index = None
        material_type_index = None
        import re
        for line in materialFile.readlines():
            fields = util.split_csv_line(line)
            if not any(fields) and not empty_line_passed:
                continue

            if not title_line_found:
                material_name_index, material_type_index = util.parse_material_file_title_index(fields)
                if material_name_index and material_type_index:
                    empty_line_passed = True
                    title_line_found = True
                    continue
                else:
                    return
            process_material_line(
                fields, material_name_index, material_type_index)

        tkMessageBox.showinfo(
            _.material_upload_info_title, _.material_upload_info_msg)
        self._post_operate()

    def _create_material(self):

        self._search_reset()

        if not self.material_name or not self.material_new_type:
            tkMessageBox.showwarning(_.create_material_warning_title, _.create_material_name_type_required)
            return
        material = Material.new_(self.material_name, self.material_new_type, self.material_count, self.material_unit,
                                 self.material_price, self.material_note)
        print (self.material_name, self.material_new_type, self.material_count, self.material_unit, self.material_price,
               self.material_note)
        MATERIAL_UTIL.add(material)
        tkMessageBox.showinfo(_.create_material_info_title, _.create_material_info_succeed)

        self._post_operate()


    def _enter_handler(self, event):
        self._fresh_page_data()

    def i_get_page_table_titles(self):
        return _.material_table_titles

    def i_get_page_obj_count(self):
        if not self.search_key:
            return MATERIAL_UTIL.getCount()

        if not self.search_material_type:
            return MATERIAL_UTIL.getCountByName(self.search_key)

        return MATERIAL_UTIL.getCountByNameAndType(self.search_key, self.search_material_type)

    def i_get_current_page_objs(self):
        start = (self.current_page - 1) * MAX_TABLE_ROW
        end = start + MAX_TABLE_ROW
        if not self.search_key:
            return MATERIAL_UTIL.getAllObjects()[start:end]

        if not self.search_material_type:
            return MATERIAL_UTIL.getObjectByName(self.search_key)

        return [MATERIAL_UTIL.getObjectByNameAndType(self.search_key, self.search_material_type)]

    def i_fill_page_data_table(self):
        for (row, obj) in enumerate(self.page_objs):
            row_data = self.page_table_entry_values[row]
            obj_fields = obj.get_ui_list()
            for col in xrange(self.max_table_col):
                row_data[col].set(obj_fields[col])
