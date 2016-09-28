# encoding: utf-8
'''
材料入库控制面板类
'''
import ttk
import Tkinter as tk
import tkMessageBox
from gui.panels.BasePanel import ControlPanel
from gui import util
from gui import messages as _
from gui.constants import MATERIAL_SEARCH, USER_SEARCH, MAX_TABLE_ROW,IN_MATERIAL

from model import USER_UTIL, MATERIAL_UTIL, INMATERIAL_UTIL, User, Material, InMaterial


class InMaterialPanel(ControlPanel):
    '''
    材料入库控制面板
    1.  填充材料入库的材料名、型号、数目、入库人信息
    2.  绘制入库数据记录信息表格
    '''

    def __init__(self, master):
        ControlPanel.__init__(self, master)
        self.control_panel_type=IN_MATERIAL


    def paint_panel(self):

        self.i_paint_main_head()
        self.paint_data_table()

    def paint_data_table(self):

        self.data_table_frame = tk.Frame(self.main_canvas, width=680, height=580)
        self.main_canvas.create_window(
            320, 20, window=self.data_table_frame, anchor=tk.NW)

        self.page_table_entries = [
            [ttk.Entry(self.data_table_frame, width=self.TABLE_ENTRY_WIDTH,
                       textvariable=self.page_table_entry_values[j][i])
             for i in xrange(self.max_table_col)] for j in xrange(MAX_TABLE_ROW)
            ]

        current_row = 0
        for (col, name) in enumerate(self.page_table_titles):
            ttk.Label(self.data_table_frame, text=name, width=self.TABLE_ENTRY_WIDTH).grid(
                row=current_row, column=col)

        current_row += 1

        for row in xrange(MAX_TABLE_ROW):
            for col in xrange(self.max_table_col):
                self.page_table_entries[row][col].grid(
                    row=current_row, column=col)
            current_row += 1

        util.add_horizontal_separator(self.data_table_frame, 5, current_row)
        self._paint_table_pagination(current_row + 2)

    def _paint_table_pagination(self, row):

        util.makePreButton(self.data_table_frame, row, 0, handler=self._pre_page)
        ttk.Label(
            self.data_table_frame, textvariable=self.page_table_info_msg).grid(row=row, column=1)
        util.makeNextButton(
            self.data_table_frame, row, 2, handler=self._next_page)

    def i_paint_main_head(self):

        self.main_canvas = tk.Canvas(
            self, height=600, width=1000)

        self.main_canvas.grid(row=0, column=0, sticky=tk.NSEW)

        labelX = 30
        entryX = 150
        itemY = 35
        stepY = 30
        label_pattern = '%6s'

        self.main_canvas.create_text(
            labelX, itemY, width=60, text=label_pattern % _.material_name_label)
        material_name_entry = ttk.Entry(
            self.main_canvas, textvariable=self.material_name_var, width=13)
        material_name_entry.bind('<FocusOut>', self._reload_material_type)
        self.main_canvas.create_window(entryX, itemY, window=material_name_entry)

        itemY += stepY

        self.main_canvas.create_text(
            labelX, itemY, width=50, text=label_pattern % _.material_type_label)
        self.material_type_widget = ttk.Combobox(
            self.main_canvas, textvariable=self.material_type_var)
        self.material_type_widget.config(width=12)
        self.main_canvas.create_window(
            entryX, itemY, window=self.material_type_widget, height=20)

        itemY += stepY

        self.main_canvas.create_text(
            labelX, itemY, width=60, text=label_pattern % _.material_in_count_label)
        in_count_entry = ttk.Entry(
            self.main_canvas, textvariable=self.material_count_var, width=13, validate='key',
            validatecommand=(self.intValidator, '%d', '%i', '%P'))
        self.main_canvas.create_window(entryX, itemY, window=in_count_entry)

        itemY += stepY

        self.main_canvas.create_text(
            labelX, itemY, width=60, text=label_pattern % _.material_in_user_laebl)
        in_user_entry = ttk.Entry(
            self.main_canvas, textvariable=self.material_user_var, width=13)
        self.main_canvas.create_window(entryX, itemY, window=in_user_entry)

        itemY += stepY

        submit_button = ttk.Button(
            self.main_canvas, text=_.material_in, command=self.__material_in_handle)
        self.main_canvas.create_window(50, itemY, window=submit_button)

        cancel_button = ttk.Button(
            self.main_canvas, text=_.cancel, command=self.cancel_operate)
        self.main_canvas.create_window(entryX, itemY, window=cancel_button)

        # 绘制水平分割线
        self.main_canvas.create_line(0, 200, 300, 200)

        itemY = 230
        # 搜索类型标签
        self.main_canvas.create_text(
            labelX, itemY, width=60, text=label_pattern % _.search_type)

        # 搜索类型单选按钮
        # 按用户搜索
        user_name_search_widget = ttk.Radiobutton(
            self.main_canvas, text=_.search_by_user, command=self.__search_type_handler,
            variable=self.search_type_var,
            value=USER_SEARCH)
        # 按材料搜索: 会触发材料类型下拉框的显示
        material_name_search_widget = ttk.Radiobutton(
            self.main_canvas, text=_.search_by_material, variable=self.search_type_var,
            command=self.__search_type_handler,
            value=MATERIAL_SEARCH)

        self.main_canvas.create_window(entryX, itemY, window=user_name_search_widget)
        self.main_canvas.create_window(
            entryX + 60, itemY, window=material_name_search_widget)

        itemY += stepY
        self.main_canvas.create_text(
            labelX, itemY, text=label_pattern % _.search_key_label)

        # 主搜索关键字
        search_key_entry = ttk.Entry(
            self.main_canvas, textvariable=self.search_key_var, width=18)
        search_key_entry.bind('<FocusOut>', self.__search_key_handler)
        self.main_canvas.create_window(entryX, itemY, window=search_key_entry)

        # 搜索材料类型，入库搜索类型为材料的话则显示，否则不显示该组件
        self.search_material_type_widget = ttk.Combobox(
            self.main_canvas, textvariable=self.search_material_type_var)
        self.search_material_type_widget.config(width=16)

        itemY += stepY
        self.search_material_type_labelX = labelX
        self.search_material_type_labelY = itemY
        self.search_material_type_entryX = entryX
        self.search_material_type_entryY = itemY

        itemY += stepY
        search_button = ttk.Button(
            self.main_canvas, text=_.search, command=self.__search)
        self.main_canvas.create_window(50, itemY, window=search_button)

        search_reset_button = ttk.Button(
            self.main_canvas, text=_.reset, command=self._search_reset)
        self.main_canvas.create_window(150, itemY, window=search_reset_button)

        # 绘制垂直分割线
        self.main_canvas.create_line(300, 20, 300, 600)

    def __search_key_handler(self, event):
        '''
        根据用户选择的搜索类型来选择相关的事件处理
        1. 如果按用户搜索则不做任何处理
        2. 如果按材料搜索则重置材料型号下拉框选择值
        '''

        if not self.search_key:
            return

        if self._is_user_search():
            return

        material_type_options = MATERIAL_UTIL.getTypeNoByName(self.search_key)
        self.search_material_type_var.set(material_type_options[0])
        self.search_material_type_widget.config(values=material_type_options)

    def __search_type_handler(self):
        '''
           根据用户选择的搜索类型来控制页面搜索组件的显示效果
           1. 如果按用户搜索则在画布上去掉材料类型下拉框
           2. 如果按材料搜索则在画布上显示材料类型下拉框
        '''
        if self._is_user_search():
            self.main_canvas.delete(self.materialTypeSearchLabel)
            self.main_canvas.delete(self.searchMaterialTypeEntry)
        else:
            self.materialTypeSearchLabel = self.main_canvas.create_text(
                self.search_material_type_labelX, self.search_material_type_labelY, text=_.material_type_label)
            self.searchMaterialTypeEntry = self.main_canvas.create_window(
                self.search_material_type_entryX, self.search_material_type_entryY,
                window=self.search_material_type_widget, height=20)

    def __search(self):

        if not self.search_key:
            tkMessageBox.showinfo(
                _.search_warning_title, _.search_key_none_warning_msg)
            return

        if self._is_user_search():
            user = USER_UTIL.getObjectByName(self.searchKey)
            if not user:
                tkMessageBox.showwarning(
                    _.search_warning_title, _.user_not_exists)
                return
            self.page_obj_count = INMATERIAL_UTIL.getInListCountByUser(user)
            self.page_count = self._get_page_count()

        else:
            material = MATERIAL_UTIL.getObjectByNameAndType(
                self.search_key, self.material_type)
            if not material:
                tkMessageBox.showwarning(
                    _.search_warning_title, _.material_not_exists)
                return
            self.page_obj_count = INMATERIAL_UTIL.getInListCountByMaterial(
                material)
            self.page_count = self._get_page_count()

        self._post_operate()



    def __material_in_handle(self):
        '''
           处理材料入库数据记录
        '''

        if not self.material_name or not self.material_type or not self.material_count or not self.material_user:
            tkMessageBox.showwarning(
                _.in_material_warning_title, _.in_material_field_required_msg)
            return

        current_record_id = self._get_record_id()
        if self.last_record_id is None:
            self.last_record_id = current_record_id
        else:
            if current_record_id == self.last_record_id:
                answer = tkMessageBox.askyesno(
                    _.in_material_confirm_title, _.in_material_confirm_msg)
                if not answer:
                    return
            else:
                self.last_record_id = current_record_id

        material = self.__update_material(
            self.material_name, self.material_type, self.material_count)

        if material is None:
            return

        user = self.__update_user(self.material_user)
        if user is None:
            return

        self.__update_in_material(user.id, material.id, self.material_count)

        tkMessageBox.showinfo(_.in_material_info_title, _.in_material_succeed)

        # 入库之后更新页面的数据表格
        self._post_operate()

    def __update_material(self, name, type_no, count):

        material = MATERIAL_UTIL.getObjectByNameAndType(name, type_no)
        if material is not None:
            material.count += count
        else:
            material = Material.new_(name, type, count)
            MATERIAL_UTIL.add(material)
        MATERIAL_UTIL.commit()
        return material

    def __update_user(self, username):
        user = USER_UTIL.getObjectByName(username)
        if user is None:
            user = User.new_(username)
            USER_UTIL.add(user)
            USER_UTIL.commit()
        return user

    def __update_in_material(self, userId, materialId, count):
        in_material = InMaterial(
            user_id=userId, material_id=materialId, count=count)
        INMATERIAL_UTIL.add(in_material)
        INMATERIAL_UTIL.commit()

    def i_get_page_table_titles(self):
        return _.in_material_table_titles

    def i_get_page_obj_count(self):
        return INMATERIAL_UTIL.getCount()

    def i_get_current_page_objs(self):
        start = (self.current_page - 1) * MAX_TABLE_ROW
        end = start + MAX_TABLE_ROW
        if not self.search_key:
            return INMATERIAL_UTIL.getAllObjects()[start:end]

        if self._is_user_search():
            user = USER_UTIL.getObjectByName(self.search_key)
            return INMATERIAL_UTIL.getInListByUser(user)[start:end]
        else:

            material = MATERIAL_UTIL.getObjectByNameAndType(
                self.search_key, self.search_material_type)
            return INMATERIAL_UTIL.getInListByMaterial(material)[start:end]

    def i_fill_page_data_table(self):

        for (row, obj) in enumerate(self.page_objs):
            row_data = self.page_table_entry_values[row]
            obj_fields = obj.get_ui_list()
            user = USER_UTIL.getObjectById(obj_fields[0])
            material = MATERIAL_UTIL.getObjectById(obj_fields[1])
            obj_fields[0:3] = (user.name, material.name, material.type_no)
            for col in xrange(self.max_table_col):
                row_data[col].set(obj_fields[col])
