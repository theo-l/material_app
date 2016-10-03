# encoding: utf-8
'''
材料入库控制面板类
'''
import ttk
import tkMessageBox
from gui.panels.BasePanel import ControlPanel
from gui import messages as _
from gui.constants import MAX_TABLE_ROW, IN_MATERIAL

from model import USER_UTIL, MATERIAL_UTIL, INMATERIAL_UTIL


class InMaterialPanel(ControlPanel):
    '''
    材料入库控制面板
    1.  填充材料入库的材料名、型号、数目、入库人信息
    2.  绘制入库数据记录信息表格
    '''

    def __init__(self, master):
        ControlPanel.__init__(self, master)
        self.control_panel_type = IN_MATERIAL
        # self.main_canvas.grid(row=0, column=0, sticky=tk.NSEW)

    def i_paint_main_head(self):

        self._create_label(
            self.HEADER_LABEL_X, self.header_widget_current_y, _.material_name_label)
        self._create_widget(
            self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_name_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        self._create_label(
            self.HEADER_LABEL_X, self.header_widget_current_y, _.material_type_label)
        self._create_widget(
            self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_type_widget, height=20)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        self._create_label(
            self.HEADER_LABEL_X, self.header_widget_current_y, _.material_in_count_label, width=60)
        self._create_widget(
            self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_count_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        self._create_label(
            self.HEADER_LABEL_X, self.header_widget_current_y, _.material_in_user_laebl, width=60)
        self._create_widget(
            self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_user_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        submit_button = ttk.Button(
            self.main_canvas, text=_.material_in, command=self.__material_in_handle)
        self._create_widget(50, self.header_widget_current_y, submit_button)
        self._create_widget(
            self.HEADER_WIDGET_X, self.header_widget_current_y, self.cancel_submit_button)

        # 绘制水平分割线
        self.main_canvas.create_line(0, 200, 300, 200)

        self.header_widget_current_y = 230
        # 搜索类型标签
        self._create_label(
            self.HEADER_LABEL_X, self.header_widget_current_y, _.search_type, width=60)

        # 搜索类型单选按钮
        self._create_widget(
            self.HEADER_WIDGET_X, self.header_widget_current_y, self.user_search_type_widget)
        self._create_widget(
            self.HEADER_WIDGET_X + 60, self.header_widget_current_y, self.material_search_type_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y
        self._create_label(
            self.HEADER_LABEL_X, self.header_widget_current_y, _.search_key_label)

        # 主搜索关键字
        self._create_widget(
            self.HEADER_WIDGET_X, self.header_widget_current_y, self.search_key_widget)

        # 搜索材料类型，入库搜索类型为材料的话则显示，否则不显示该组件

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y
        self.search_material_type_labelX = self.HEADER_LABEL_X
        self.search_material_type_labelY = self.header_widget_current_y
        self.search_material_type_entryX = self.HEADER_WIDGET_X
        self.search_material_type_entryY = self.header_widget_current_y

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y
        self._create_widget(
            50, self.header_widget_current_y, self.search_button)
        self._create_widget(
            150, self.header_widget_current_y, self.reset_button)

        # 绘制垂直分割线
        self.main_canvas.create_line(300, 20, 300, 600)

    def __material_in_handle(self):
        '''
           处理材料入库数据记录
        '''

        self._search_reset()

        if self.material_count == 0:
            tkMessageBox.showwarning(
                _.material_count_warning_title, _.material_count_le_zero_warning_msg)
            return

        if not self.material_name or not self.material_type or not self.material_count or not self.material_user:
            tkMessageBox.showwarning(
                _.in_material_warning_title, _.in_material_field_required_msg)
            return

        if not self._repeat_record_check():
            return

        material = self._update_material(
            self.material_name, self.material_type, self.material_count)

        if material is None:
            return

        user = self._update_user(self.material_user)
        if user is None:
            return

        INMATERIAL_UTIL.update_in_material(
            user.id, material.id, self.material_count)
        tkMessageBox.showinfo(_.in_material_info_title, _.in_material_succeed)

        # 入库之后更新页面的数据表格
        self._post_operate()

    def i_get_page_table_titles(self):
        return _.in_material_table_titles

    def i_get_page_obj_count(self):
        if not self.search_key:
            return INMATERIAL_UTIL.get_count()

        if self._is_user_search():
            user = USER_UTIL.get_object_by_name(self.search_key)
            if not user:
                tkMessageBox.showwarning(
                    _.search_warning_title, _.user_not_exists)
                return 0
            else:
                return INMATERIAL_UTIL.get_in_list_count_by_user(user)
        else:
            if not self.search_material_type:
                return INMATERIAL_UTIL.get_in_count_by_material_name(self.search_key)
            else:
                material = MATERIAL_UTIL.get_object_by_name_and_type(
                    self.search_key, self.search_material_type)
                return INMATERIAL_UTIL.get_in_list_count_by_material(material)

    def i_get_current_page_objs(self):
        start = (self.current_page - 1) * MAX_TABLE_ROW
        end = start + MAX_TABLE_ROW
        if not self.search_key:
            return INMATERIAL_UTIL.get_all_objects()[start:end]

        if self._is_user_search():
            user = USER_UTIL.get_object_by_name(self.search_key)
            return INMATERIAL_UTIL.get_in_list_by_user(user)[start:end]
        else:
            if not self.search_material_type:
                return INMATERIAL_UTIL.get_in_list_by_material_name(self.search_key)[start:end]
            else:
                material = MATERIAL_UTIL.get_object_by_name_and_type(
                    self.search_key, self.search_material_type)
                return INMATERIAL_UTIL.get_in_list_by_material(material)[start:end]

    def i_fill_page_data_table(self):

        for (row, obj) in enumerate(self.page_objs):
            row_data = self.page_table_entry_values[row]
            obj_fields = obj.get_ui_list()
            user = USER_UTIL.get_object_by_id(obj_fields[0])
            material = MATERIAL_UTIL.get_object_by_id(obj_fields[1])
            obj_fields[0:3] = (user.name, material.name, material.type_no)
            for col in xrange(self.max_table_col):
                row_data[col].set(obj_fields[col])
