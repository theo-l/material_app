# encoding: utf-8
'''
材料出库控制面板类
'''
import ttk
import tkMessageBox
from gui.panels.BasePanel import ControlPanel
from gui import messages as _
from gui.constants import  MAX_TABLE_ROW, OUT_MATERIAL

from model import MATERIAL_UTIL, USER_UTIL, OUTMATERIAL_UTIL


class OutMaterialPanel(ControlPanel):
    '''
    绘制材料出库控制面板
    1. 填充材料出库的材料名称、型号、数目、用途、领料人
    2. 绘制材料出库数据信息表格
    '''

    def __init__(self, master):
        ControlPanel.__init__(self, master)
        self.control_panel_type = OUT_MATERIAL
        # self.main_canvas.grid(row=0, column=0, sticky=tk.NSEW)

    def i_paint_main_head(self):

        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, text=_.material_name_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_name_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, text=_.material_type_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_type_widget, height=20)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, text=_.material_out_count_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_count_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, text=_.material_out_usage_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_usage_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, text=_.material_out_user_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.material_user_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        submit_button = ttk.Button(self.main_canvas, text=_.material_out, command=self.__material_out_handler)
        self._create_widget(50, self.header_widget_current_y, submit_button)
        self._create_widget(150, self.header_widget_current_y, self.cancel_submit_button)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        # 绘制左边控制面板的上下分割线
        self.main_canvas.create_line(0, self.header_widget_current_y, 300, self.header_widget_current_y)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        # 绘制搜索类型标签文本
        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, text=_.search_type)

        # 绘制搜索类型的单选按钮
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.user_search_type_widget)
        self._create_widget(self.HEADER_WIDGET_X + 60, self.header_widget_current_y, self.material_search_type_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        # 绘制搜索关键字
        self._create_label(self.HEADER_LABEL_X, self.header_widget_current_y, text=_.search_key_label)
        self._create_widget(self.HEADER_WIDGET_X, self.header_widget_current_y, self.search_key_widget)

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y

        self.search_material_type_labelX = self.HEADER_LABEL_X
        self.search_material_type_labelY = self.header_widget_current_y
        self.search_material_type_entryX = self.HEADER_WIDGET_X
        self.search_material_type_entryY = self.header_widget_current_y

        self.header_widget_current_y += self.HEADER_WIDGET_STEP_Y
        self._create_widget(50, self.header_widget_current_y, self.search_button)
        self._create_widget(150, self.header_widget_current_y, self.reset_button)

        # 绘制一个垂直分割线
        self.main_canvas.create_line(300, 20, 300, 600)

    def __material_out_handler(self):
        "出库逻辑处理"
        # 根据材料名称和型号判断材料库存
        # 材料库存处理
        # 领料人处理
        # 出库记录处理

        self._search_reset()

        if self.material_count == 0:
            tkMessageBox.showwarning(_.material_count_warning_title, _.material_count_le_zero_warning_msg)
            return

        if not self.material_name or not self.material_type or not self.material_count or not self.material_usage or not self.material_user:
            tkMessageBox.showwarning(
                _.out_material_warning_title, _.out_material_field_required_msg)
            return

        if not self._repeat_record_check():
            return

        material = self._update_material(self.material_name, self.material_type, self.material_count)
        if material is None:
            return

        user = self._update_user(self.material_user)
        if user is None:
            return

        OUTMATERIAL_UTIL.updateOutMaterial(user.id, material.id, self.material_count, self.material_usage)

        tkMessageBox.showinfo(
            _.out_material_info_title, _.out_material_succeed)
        self._post_operate()

    def i_get_page_table_titles(self):
        return _.out_material_table_titles

    def i_get_page_obj_count(self):
        if not self.search_key:
            return OUTMATERIAL_UTIL.getCount()

        if self._is_user_search():
            user = USER_UTIL.getObjectByName(self.search_key)
            if not user:
                tkMessageBox.showwarning(_.search_warning_title, _.user_not_exists)
                return 0
            return OUTMATERIAL_UTIL.getOutListCountByUser(user)
        else:
            if not self.search_material_type:
                return OUTMATERIAL_UTIL.get_out_count_by_material_name(self.search_key)
            else:
                material = MATERIAL_UTIL.getObjectByNameAndType(self.search_keyk, self.search_material_type)
                return OUTMATERIAL_UTIL.getOutListCountByMaterial(material)

    def i_get_current_page_objs(self):
        start = (self.current_page - 1) * MAX_TABLE_ROW
        end = start + MAX_TABLE_ROW

        if not self.search_key:
            return OUTMATERIAL_UTIL.getAllObjects()[start:end]

        if self._is_user_search():
            user = USER_UTIL.getObjectByName(self.search_key)
            return OUTMATERIAL_UTIL.getOutListByUser(user)[start:end]
        else:
            if not self.search_material_type:
                return OUTMATERIAL_UTIL.get_out_list_by_material_name(self.search_key)[start:end]
            else:
                material = MATERIAL_UTIL.getObjectByNameAndType( self.search_key, self.search_material_type)
                return OUTMATERIAL_UTIL.getOutListByMaterial(material)[start:end]

    def i_fill_page_data_table(self):
        for (row, obj) in enumerate(self.page_objs):
            row_data = self.page_table_entry_values[row]
            obj_fields = obj.get_ui_list()
            user = USER_UTIL.getObjectById(obj_fields[0])
            material = MATERIAL_UTIL.getObjectById(obj_fields[1])
            obj_fields[0:3] = (user.name, material.name, material.type_no)
            for col in xrange(self.max_table_col):
                row_data[col].set(obj_fields[col])
