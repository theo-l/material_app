# encoding: utf-8
'''
材料出库控制面板类
'''
import ttk
import Tkinter as tk
import tkMessageBox
from gui.panels.BasePanel import ControlPanel
from gui import util
from gui import messages as _
from gui.constants import MATERIAL_SEARCH, USER_SEARCH,MAX_TABLE_ROW, OUT_MATERIAL

from model import MATERIAL_UTIL, USER_UTIL, OUTMATERIAL_UTIL, Material, User, OutMaterial


class OutMaterialPanel(ControlPanel):
    '''
    绘制材料出库控制面板
    1. 填充材料出库的材料名称、型号、数目、用途、领料人
    2. 绘制材料出库数据信息表格
    '''

    def __init__(self, master):
        ControlPanel.__init__(self, master)
        self.control_panel_type=OUT_MATERIAL

    def paint_panel(self):
        self.i_paint_main_head()
        self.paint_data_table()

    def paint_data_table(self):
        current_row = 0

        self.page_table_entries = [
            [ttk.Entry(self.data_table_frame, width=self.TABLE_ENTRY_WIDTH,
                       textvariable=self.page_table_entry_values[j][i])
             for i in xrange(self.max_table_col)] for j in xrange(MAX_TABLE_ROW)
            ]

        # 绘制表头
        for (col, name) in enumerate(self.page_table_titles):
            ttk.Label(self.data_table_frame, text=name, width=self.TABLE_ENTRY_WIDTH).grid(
                row=current_row, column=col)

        current_row += 1

        # 绘制数据表格
        for row in xrange(MAX_TABLE_ROW):
            for col in xrange(self.max_table_col):
                self.page_table_entries[row][col].grid(
                    row=current_row, column=col)
            current_row += 1

        util.add_horizontal_separator(self.data_table_frame, 6, current_row)
        self._paint_table_pagination(current_row + 2)

    def _paint_table_pagination(self, row):
        util.makePreButton(self.data_table_frame, row, 0, handler=self._pre_page)
        ttk.Label(
            self.data_table_frame, textvariable=self.page_table_info_msg).grid(row=row, column=1)
        util.makeNextButton(
            self.data_table_frame, row, 2, handler=self._next_page)

    def i_fill_page_data_table(self):
        for (row, obj) in enumerate(self.page_objs):
            row_data = self.page_table_entry_values[row]
            obj_fields = obj.get_ui_list()
            user = USER_UTIL.getObjectById(obj_fields[0])
            material = MATERIAL_UTIL.getObjectById(obj_fields[1])
            obj_fields[0:3] = (user.name, material.name, material.type_no)
            for col in xrange(self.max_table_col):
                row_data[col].set(obj_fields[col])

    def i_paint_main_head(self):

        labelX = 30
        entryX = 150
        itemY = 35
        stepY = 35


        self.main_canvas.create_text(labelX, itemY, text='%8s' % _.material_name_label)
        self.main_canvas.create_window(entryX, itemY, window=self.material_name_widget)

        itemY += stepY

        self.main_canvas.create_text(labelX, itemY, text='%8s' % _.material_type_label)
        self.main_canvas.create_window(entryX, itemY, window=self.material_type_widget, height=20)

        itemY += stepY

        self.main_canvas.create_text(labelX, itemY, text='%8s' % _.material_out_count_label)
        self.main_canvas.create_window(entryX, itemY, window=self.material_count_widget)

        itemY += stepY

        self.main_canvas.create_text(labelX, itemY, text='%8s' % _.material_out_usage_label)
        self.main_canvas.create_window(entryX, itemY, window=self.material_usage_widget)

        itemY += stepY

        self.main_canvas.create_text(labelX, itemY, text='%8s' % _.material_out_user_label)
        self.main_canvas.create_window(entryX, itemY, window=self.material_user_widget)

        itemY += stepY

        submit_button = ttk.Button(self.main_canvas, text=_.material_out, command=self.__material_out_handler)
        self.main_canvas.create_window(50, itemY, window=submit_button)
        self.main_canvas.create_window(150, itemY, window=self.cancel_submit_button)

        itemY += stepY

        # 绘制左边控制面板的上下分割线
        self.main_canvas.create_line(0, itemY, 300, itemY)

        itemY += stepY

        # 绘制搜索类型标签文本
        self.main_canvas.create_text(labelX, itemY, text=_.search_type)

        # 绘制搜索类型的单选按钮
        username_search_widget = ttk.Radiobutton(
        self.main_canvas.create_window(entryX, itemY, window=self.user_search_type_widget)
        self.main_canvas.create_window(entryX + 60, itemY, window=self.material_search_type_widget)

        itemY += stepY

        # 绘制搜索关键字
        self.main_canvas.create_text(labelX, itemY, text=_.search_key_label)
        self.main_canvas.create_window(entryX, itemY, window=self.search_key_widget)

        itemY += stepY

        self.search_material_type_labelX = labelX
        self.search_material_type_labelY = itemY
        self.search_material_type_entryX = entryX
        self.search_material_type_entryY = itemY

        itemY += stepY
        self.main_canvas.create_window(50, itemY, window=self.search_button)
        self.main_canvas.create_window(150, itemY, window=self.reset_button)

        # 绘制一个垂直分割线
        self.main_canvas.create_line(300, 20, 300, 600)

    def i_search(self):
        if not self.search_key:
            tkMessageBox.showwarning(
                _.search_warning_title, _.search_key_none_warning_msg)

        if self._is_user_search():
            user = USER_UTIL.getObjectByName(self.search_key)
            if not user:
                tkMessageBox.showwarning(
                    _.search_warning_title, _.user_not_exists)
                return

            self.page_obj_count = OUTMATERIAL_UTIL.getOutListCountByUser(user)

        else:
            material = MATERIAL_UTIL.getObjectByNameAndType(
                self.search_key, self.search_material_type)
            if not material:
                tkMessageBox.showwarning(
                    _.search_warning_title, _.material_not_exists)
                return
            self.page_obj_count = OUTMATERIAL_UTIL.getOutListCountByMaterial(
                material)

        self.page_count = self._get_page_count()
        self._post_operate()


    def __search_key_focus_out_handler(self, event):

        if not self.search_key:
            return

        if self._is_user_search():
            return

        material_type_options = MATERIAL_UTIL.getTypeNoByName(self.search_keyk)
        self.search_material_type_var.set(material_type_options[0])
        self.search_material_type_widget.config(values=material_type_options)

    def __search_type_handler(self):
        '''
        处理用户选择的搜索类型单选按钮
        1. 按用户搜索时去掉材料型号标签和下拉框的显示
        2. 按材料搜索时显示材料型号标签和下拉框的显示
        '''
        if self._is_user_search():
            self.main_canvas.delete(self.material_type_search_label)
            self.main_canvas.delete(self.material_type_search_entry)
        else:
            self.material_type_search_label = self.main_canvas.create_text(
                self.search_material_type_labelX, self.search_material_type_labelY, text=_.material_type_label)
            self.material_type_search_entry = self.main_canvas.create_window(
                self.search_material_type_entryX, self.search_material_type_entryY,
                window=self.search_material_type_widget)


    def __material_out_handler(self):
        "出库逻辑处理"
        # 根据材料名称和型号判断材料库存
        # 材料库存处理
        # 领料人处理
        # 出库记录处理

        if not self.material_name or not self.material_type or not self.material_count or not self.material_usage or not self.material_user:
            tkMessageBox.showwarning(
                _.out_material_warning_title, _.out_material_field_required_msg)
            return

        current_record_id = self._get_record_id()
        if self.last_record_id is None:
            self.last_record_id = current_record_id
        else:
            if current_record_id == self.last_record_id:
                answer = tkMessageBox.askyesno(
                    _.out_material_confirm_title, _.out_material_confirm_msg)
                if not answer:
                    return
            else:
                self.last_record_id = current_record_id

        material = self.__update_material(self.material_name, self.material_type, self.material_count)
        if material is None:
            return

        user = self.__update_user(self.material_user)
        if user is None:
            return

        self.__update_out_material(user.id, material.id, self.material_count, self.material_usage)

        tkMessageBox.showinfo(
            _.out_material_info_title, _.out_material_succeed)
        self._post_operate()

    def __update_material(self, name, type_no, count):
        "检查材料库存，更新材料库存"
        material = MATERIAL_UTIL.getObjectByNameAndType(name, type_no)
        if material is None:
            tkMessageBox.showwarning(
                _.out_material_warning_title, _.material_not_exists)
            return None
        if material.count < count:
            tkMessageBox.showwarning(
                _.out_material_warning_title, _.out_material_count_over_msg % (material.count, count))
            return None
        material.count -= count
        MATERIAL_UTIL.commit()
        return material

    def __update_user(self, username):
        user = USER_UTIL.getObjectByName(username)
        if user is None:
            user = User.new_(username)
            USER_UTIL.add(user)
            USER_UTIL.commit()
        return user

    def __update_out_material(self, userId, materialId, count, usage):
        out_material = OutMaterial(
            user_id=userId, material_id=materialId, count=count, usage=usage)
        OUTMATERIAL_UTIL.add(out_material)
        OUTMATERIAL_UTIL.commit()

    def i_get_page_table_titles(self):
        return _.out_material_table_titles

    def i_get_page_obj_count(self):
        return OUTMATERIAL_UTIL.getCount()

    def i_get_current_page_objs(self):
        start = (self.current_page - 1) * MAX_TABLE_ROW
        end = start + MAX_TABLE_ROW

        if not self.search_key:
            return OUTMATERIAL_UTIL.getAllObjects()[start:end]

        if self._is_user_search():
            user = USER_UTIL.getObjectByName(self.search_key)
            return OUTMATERIAL_UTIL.getOutListByUser(user)[start:end]
        else:
            material = MATERIAL_UTIL.getObjectByNameAndType(
                self.search_key, self.search_material_type)
            return OUTMATERIAL_UTIL.getOutListByMaterial(material)
