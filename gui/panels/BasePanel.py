# encoding: utf-8
'''
控制面板的基类
'''
import ttk
import tkMessageBox
import Tkinter as tk
from gui import util
from gui.constants import USER_SEARCH, MATERIAL_SEARCH
from gui.constants import MAX_TABLE_ROW, PAGE_INFO_SEPARATOR, IN_MATERIAL, OUT_MATERIAL
import  gui.messages as _

from model import MATERIAL_UTIL, USER_UTIL, User, Material



class ControlPanel(tk.Frame):
    TABLE_ENTRY_WIDTH = 13  # 表格的宽度

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.int_validator = self.register(self._intValidator)


        # control panel's header variables
        self.material_name_var = tk.StringVar()
        self.material_type_var = tk.StringVar()
        self.material_count_var = tk.IntVar()
        self.material_usage_var = tk.StringVar()
        self.material_user_var = tk.StringVar()

        # control panel's search variables
        self.search_type_var = tk.StringVar()
        self.search_type_var.set(USER_SEARCH)  # default search by user
        self.search_key_var = tk.StringVar()
        self.search_material_type_var = tk.StringVar()

        # common control panel widgets
        self.main_canvas = tk.Canvas(self, height=600, width=1000)
        self.main_canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.data_table_frame=tk.Frame(self.main_canvas, width=680, height=580)
        self.main_canvas.create_window(320,20,window=self.data_table_frame, anchor=tk.NW)

        self.material_name_widget = ttk.Entry(self.main_canvas, textvariable=self.material_name_var, width=13)
        self.material_name_widget.bind('<FocusOut>', self._material_name_handler)

        self.material_type_widget = ttk.Combobox(self.main_canvas, textvariable=self.material_type_var, width=12)

        self.material_count_widget = ttk.Entry(self.main_canvas, textvariable=self.material_count_var, width=13, validate='key', validatecommand=(self.intValidator, '%d', '%i', '%P'))

        self.material_usage_widget = ttk.Entry(self.main_canvas, textvariable = self.material_usage_var, width=13)
        self.material_user_widget = ttk.Entry(self.main_canvas, textvariable = self.material_user_var, width=13)

        self.cancel_submit_button =ttk.Button(self.main_canvas, command=self.cancel_operate, text=_.cancel)

        self.user_search_type_widget = ttk.Radiobutton(self.main_canvas, text=_.search_by_user, value=USER_SEARCH, command=self._search_type_handler, variable=self.search_type_var)
        self.material_search_type_widget = ttk.Radiobutton(self.main_canvas, text=_.search_by_material, value=MATERIAL_SEARCH, command=self._search_type_handler, variable=self.search_type_var)

        self.search_key_widget = ttk.Entry(self.main_canvas, textvariable = self.search_key_var)
        self.search_key_widget.bind('<FocusOut>', self._search_key_handler)

        self.search_material_type_widget = ttk.Combobox(self.main_canvas, textvariable=self.search_material_type_var, width=16)
        self.search_material_type_widget.config(width=12)

        self.search_button = ttk.Button(self.main_canvas, text=_.search, command=self.i_search)
        self.reset_button = ttk.Button(self.main_canvas, text=_.reset, command=self._search_reset)


        # material type search widget's label and combobox position
        self.search_material_type_labelX = None
        self.search_material_type_labelY = None
        self.search_material_type_entryX = None
        self.search_material_type_entryY = None

        # control panel's type
        self.control_panel_type=None

        # some static variable definition
        self.page_table_titles = self.i_get_page_table_titles()
        self.max_table_col = len(self.page_table_titles)
        self.page_table_entry_values = [
            [tk.StringVar() for i in xrange(self.max_table_col)] for j in xrange(MAX_TABLE_ROW)
            ]
        self.page_table_entries = [
            [ttk.Entry(self, width=self.TABLE_ENTRY_WIDTH, textvariable=self.page_table_entry_values[j][i])
             for i in xrange(self.max_table_col)] for j in xrange(MAX_TABLE_ROW)
            ]

        # control panel's data table variables
        self.last_record_id = None
        self.page_table_info_msg = tk.StringVar()
        self.page_obj_count = self.i_get_page_obj_count()
        self.page_count = self._get_page_count()
        self.current_page = 1
        self._set_page_table_info_msg()
        self.page_objs = self.i_get_current_page_objs()
        self.i_fill_page_data_table()

        # paint the control panel
        self.paint_panel()


    def _material_name_handler(self, event):
        '''
        On the control panel header exist a common association between material_name and material_type
        this event handler method will load the material_type depends on the material_name
        '''
        if not self.material_name:
            return

        material_type_options = MATERIAL_UTIL.getTypeNoByName(self.material_name)
        self.material_type_var.set(material_type_options[0])
        self.material_type_widget.config(values = material_type_options )


    def _search_type_handler(self):
        '''
        control search control's display depends on user selected search type
        '''
        if self._is_material_search():
            self.search_material_type_label_id=self.main_canvas.create_text(self.search_material_type_labelX, self.search_material_type_labelY, text=_.material_type_label)
            self.search_material_type_widget_id = self.main_canvas.create_window(self.search_material_type_entryX, self.search_material_type_entryY, window=self.search_material_type_widget)
        else:
            self.main_canvas.delete(self.search_material_type_label_id)
            self.main_canvas.delete(self.search_material_type_widget_id)


    def _search_key_handler(self, event):
        '''
        control search_material_type_widget's value initiation depends on user selected search type
        '''
        if not self.search_key:
            return

        if self._is_user_search():
            return 

        material_type_options = MATERIAL_UTIL.getTypeNoByName(self.search_key)
        self.search_material_type_var.set(material_type_options[0])
        self.material_type_widget.config(values=material_type_options)

    def i_search(self):
        'Because the search action has different behaviour in differnt control panel'
        raise NotImplemented('search action should be implemented by the concrete class')
        

    @property
    def material_name(self):
        return self.material_name_var.get()

    @material_name.setter
    def material_name(self, value):
        self.material_name_var.set(value)

    @property
    def material_type(self):
        return self.material_type_var.get()

    @material_type.setter
    def material_type(self, value):
        self.material_type_var.set(value)

    @property
    def material_count(self):
        return self.material_count_var.get()

    @material_count.setter
    def material_count(self, value):
        self.material_count_var.set(value)

    @property
    def material_usage(self):
        return self.material_usage_var.get()

    @material_usage.setter
    def material_usage(self, value):
        self.material_usage_var.set(value)

    @property
    def material_user(self):
        return self.material_user_var.get()

    @material_user.setter
    def material_user(self, value):
        self.material_user_var.set(value)

    @property
    def search_type(self):
        return self.search_type_var.get()

    @property
    def search_key(self):
        return self.search_key_var.get()

    @property
    def search_material_type(self):
        return self.search_material_type_var.get()

    def cancel_operate(self):
        self.material_name = ''
        self.material_type = ''
        self.material_count = 0
        self.material_user = ''
        self.material_usage = ''

    def _is_user_search(self):
        return self.search_type == USER_SEARCH

    def _is_material_search(self):
        return self.search_type == MATERIAL_SEARCH

    def paint_panel(self):
        """
        绘制控制面板UI
        """
        util.add_horizontal_space(self, 11, 0)
        self.i_paint_main_head()
        util.add_horizontal_separator(self, 11, 2)
        self.paint_data_table()

    def paint_data_table(self):
        """
        绘制控制面板中的数据表格
        """
        current_row = 8

        # 绘制表头
        for (col, name) in enumerate(self.page_table_titles):
            ttk.Label(self, text=name, width=self.TABLE_ENTRY_WIDTH).grid(
                row=current_row, column=col)

        current_row += 1

        # 绘制数据表格
        for row in xrange(MAX_TABLE_ROW):
            for col in xrange(self.max_table_col):
                self.page_table_entries[row][col].grid(
                    row=current_row, column=col)
            current_row += 1

        util.add_horizontal_separator(self, 11, current_row)
        self._paint_table_pagination(current_row + 3)

    def _paint_table_pagination(self, row):
        """
        绘制数据表格的导航按钮
        """
        util.makePreButton(self, row, 0)
        ttk.Label(self, textvariable=self.page_table_info_msg).grid(
            row=row, column=1)
        self._set_page_table_info_msg()
        util.makeNextButton(self, row, 2)

    def _post_operate(self):
        '''
        this method used to redraw data table after operate
        '''
        self.current_page = 1
        self._fresh_page_data()

    def _pre_page(self):
        """
        上一页导航按钮的事件处理器
        """
        if self.current_page <= 1:
            return
        self.current_page -= 1
        self._fresh_page_data()

    def _next_page(self):
        """
        下一页导航按钮的事件处理器
        """
        if self.current_page >= self.page_count:
            return
        self.current_page += 1
        self._fresh_page_data()

    def _fresh_page_data(self):
        """
        刷新当前页面的数据以及表格
        """
        self._set_page_table_info_msg()
        self.page_objs = self.i_get_current_page_objs()
        self._clean_page_data_table()
        self.i_fill_page_data_table()

    def _clean_page_data_table(self):
        """
        清除数据表格中的所有数据
        """
        for row in self.page_table_entry_values:
            for col in row:
                col.set('')

    def _add_main_head_label(self, text, row, column, width=10):
        """
        在控制面板头中绘制标签组件
        """
        return ttk.Label(self, text=text, width=width).grid(row=row, column=column)

    def _set_page_table_info_msg(self):
        '''
        设置页面导航的页面信息
        '''
        self.page_table_info_msg.set(
            PAGE_INFO_SEPARATOR.join(map(str, [self.current_page, self.page_count])))

    def _get_page_count(self):
        return (self.page_obj_count / MAX_TABLE_ROW) if self.page_obj_count % MAX_TABLE_ROW == 0 else (
            self.page_obj_count / MAX_TABLE_ROW + 1)

    def i_paint_main_head(self):
        """
        Because each control panels header has different lay out
        So this method should be implemented by each panel subclass
        """
        raise NotImplemented('method not implemented yet!')

    def i_fill_page_data_table(self):
        """
        Because the data items are depend on the data model's field
        """
        raise NotImplemented('method not implemented yet!')

    def i_get_current_page_objs(self):
        '''
        Because current page objects are depend on user's operate:
        Can be "Search"/"InMaterial"/"OutMaterial"/"Pagination"
        '''
        raise NotImplemented('method not implemented yet!')

    def i_get_page_table_titles(self):
        '''
        Each data table's header depends on the data model's fields
        '''
        raise NotImplemented('method not implemented yet!')

    def i_get_page_obj_count(self):
        '''
        Objects count are depend on the control panel and user's operate
        '''
        raise NotImplemented('method not implemented yet!')

    def _get_record_id(self):
        return "".join(
            (self.material_name, self.material_type, str(self.material_count), self.material_usage, self.material_user))


    def _search_reset(self):
        '''
        Clean search field value and refresh data table
        '''
        self.search_key_var.set('')
        if self._is_material_search():
            self.search_material_type_var.set('')
        self._fresh_page_data()

    def _update_user(self, username):
        '''
        Both "InMaterial" and "OutMaterial" operations will affect user entry, to avoid operate without user
        :param username:
        :return: user
        '''
        user = USER_UTIL.getObjectByName(username)
        if not user:
            user = User.new_(username)
            USER_UTIL.add(user)
        return user

    def _update_material(self, material_name, material_type, material_count):
        material = MATERIAL_UTIL.getObjectByNameAndType(material_name, material_type)
        if material is None:
            tkMessageBox.showwarning(_.update_material_warning_title, _.material_not_exists)
            return None

        if material is not None:
            if self.control_panel_type == IN_MATERIAL:
                material.count += material_count
            elif self.control_panel_type == OUT_MATERIAL:
                if material.count < material_count:
                    tkMessageBox.showwarning(_.update_material_warning_title, )



    # 整数Entry值验证器
    def _int_validator(self, action, index, text):
        print(action, index, text)
        if not text:
            return True

        if not text.isdigit():
            tkMessageBox.showwarning(u"整数验证信息", u'%s 不是一个整数值' % text)
            return False
        return True
