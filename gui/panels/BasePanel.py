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
import gui.messages as _

from model import MATERIAL_UTIL, USER_UTIL, User


class ControlPanel(tk.Frame):
    TABLE_ENTRY_WIDTH = 13  # 表格的宽度

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.int_validator = self.register(util.int_validator)

        # control panel's common header variables
        self.material_name_var = tk.StringVar()
        self.material_type_var = tk.StringVar()
        self.material_new_type_var = tk.StringVar()
        self.material_unit_var = tk.StringVar()
        self.material_count_var = tk.IntVar()
        self.material_price_var = tk.DoubleVar()
        self.material_note_var = tk.StringVar()
        self.material_usage_var = tk.StringVar()
        self.material_user_var = tk.StringVar()

        # control panel's common search variables
        self.search_type_var = tk.StringVar()
        self.search_type_var.set(USER_SEARCH)  # default search by user
        self.search_key_var = tk.StringVar()
        self.search_material_type_var = tk.StringVar()

        # control panel main canvas for layout
        self.main_canvas = tk.Canvas(self, height=600, width=1200, bg='light green')
        self.main_canvas.grid(row=0, column=0, sticky=tk.NSEW)

        # control panel's data table frame widget
        self.data_table_frame = tk.Frame(self.main_canvas, width=780, height=580, bg='light blue')
        self.main_canvas.create_window(320, 20, window=self.data_table_frame, anchor=tk.NW)

        # control panel's common header widgets
        self.material_name_widget = ttk.Entry(self.main_canvas, textvariable=self.material_name_var, width=13)
        self.material_name_widget.bind('<FocusOut>', self._material_name_handler)

        self.material_type_widget = ttk.Combobox(self.main_canvas, textvariable=self.material_type_var, width=12)
        self.material_new_type_widget = ttk.Entry(self.main_canvas, textvariable=self.material_new_type_var, width=13)

        self.material_unit_widget = ttk.Entry(self.main_canvas, textvariable=self.material_unit_var, width=13)

        self.material_count_widget = ttk.Entry(self.main_canvas, textvariable=self.material_count_var, width=13,
                                               validate='key', validatecommand=(self.int_validator, '%d', '%i', '%P'))
        self.material_price_widget = ttk.Entry(self.main_canvas, textvariable=self.material_price_var, width=13)
        self.material_note_widget = ttk.Entry(self.main_canvas, textvariable=self.material_note_var, width=13)

        self.material_usage_widget = ttk.Entry(self.main_canvas, textvariable=self.material_usage_var, width=13)
        self.material_user_widget = ttk.Entry(self.main_canvas, textvariable=self.material_user_var, width=13)

        self.cancel_submit_button = ttk.Button(self.main_canvas, command=self._cancel_operate, text=_.cancel)

        self.user_search_type_widget = ttk.Radiobutton(self.main_canvas, text=_.search_by_user, value=USER_SEARCH,
                                                       command=self._search_type_handler, variable=self.search_type_var)
        self.material_search_type_widget = ttk.Radiobutton(self.main_canvas, text=_.search_by_material,
                                                           value=MATERIAL_SEARCH, command=self._search_type_handler,
                                                           variable=self.search_type_var)

        # control panel's common search widget
        self.search_key_widget = ttk.Entry(self.main_canvas, textvariable=self.search_key_var)
        self.search_key_widget.bind('<FocusOut>', self._search_key_handler)

        self.search_material_type_widget = ttk.Combobox(self.main_canvas, textvariable=self.search_material_type_var)
        self.search_material_type_widget.config(width=12)

        self.search_button = ttk.Button(self.main_canvas, text=_.search, command=self._search)
        self.reset_button = ttk.Button(self.main_canvas, text=_.reset, command=self._search_reset)
        self.export_button = ttk.Button(self.data_table_frame, text=_.export, command=self.i_export)

        # material type search widget's label and combobox position
        self.search_material_type_labelX = None
        self.search_material_type_labelY = None
        self.search_material_type_entryX = None
        self.search_material_type_entryY = None

        # variables used to control the control panel's main header layout
        self.HEADER_LABEL_X = 30
        self.HEADER_WIDGET_X = 150
        self.header_widget_current_y = 35
        self.HEADER_WIDGET_STEP_Y = 30

        # control panel's type, used to control update material's count behavior
        self.control_panel_type = None

        # some static variable definition
        self.page_table_titles = self.i_get_page_table_titles()
        self.max_table_col = len(self.page_table_titles)
        self.page_table_entry_values = [
            [tk.StringVar() for i in xrange(self.max_table_col)] for j in xrange(MAX_TABLE_ROW)
            ]
        self.page_table_entries = [
            [ttk.Entry(self.data_table_frame, width=self.TABLE_ENTRY_WIDTH,
                       textvariable=self.page_table_entry_values[j][i])
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

    def paint_panel(self):
        """
        绘制控制面板UI
        """
        # util.add_horizontal_space(self, 11, 0)
        self.i_paint_main_head()
        # util.add_horizontal_separator(self, 11, 2)
        self.paint_data_table()

    def paint_data_table(self):
        """
        绘制控制面板中的数据表格
        """
        # self.page_table_entries = [
        #     [ttk.Entry(self.data_table_frame, width=self.TABLE_ENTRY_WIDTH,
        #                textvariable=self.page_table_entry_values[j][i]) for i in xrange(self.max_table_col)]
        #     for j in xrange(MAX_TABLE_ROW)
        #     ]

        current_row = 0
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

        util.add_horizontal_separator(self.data_table_frame, self.max_table_col, current_row)
        self._paint_table_pagination(current_row + 3)

    def _paint_table_pagination(self, row):

        """
        绘制数据表格的导航按钮
        """
        util.make_pre_button(self.data_table_frame, row, 0, self._pre_page)
        ttk.Label(self.data_table_frame, textvariable=self.page_table_info_msg).grid(
            row=row, column=1)
        self._set_page_table_info_msg()
        util.make_next_button(self.data_table_frame, row, 2, self._next_page)
#        self.export_button.config(row=row, column=3, command=self.i_export)

    def _material_name_handler(self, event):
        '''
        On the control panel header exist a common association between material_name and material_type
        this event handler method will load the material_type depends on the material_name
        '''
        if not self.material_name:
            return

        material_type_options = MATERIAL_UTIL.get_type_no_by_name(self.material_name)
        self.material_type_var.set(material_type_options[0])
        self.material_type_widget.config(values=material_type_options)

    def _search_type_handler(self):
        '''
        control search control's display depends on user selected search type
        '''
        if self._is_material_search():
            self.search_material_type_label_id = self.main_canvas.create_text(self.search_material_type_labelX,
                                                                              self.search_material_type_labelY,
                                                                              text=_.material_type_label)
            self.search_material_type_widget_id = self.main_canvas.create_window(self.search_material_type_entryX,
                                                                                 self.search_material_type_entryY,
                                                                                 window=self.search_material_type_widget)
        else:
            self.main_canvas.delete(self.search_material_type_label_id)
            self.main_canvas.delete(self.search_material_type_widget_id)

    def _search_key_handler(self, event):
        '''
        control search_material_type_widget's value initiation depends on user selected search type
        '''
        if not self.search_key:
            print 'key word is null'
            return

        if self._is_user_search():
            print 'is user search'
            return

        material_type_options = MATERIAL_UTIL.get_type_no_by_name(self.search_key)
        self.search_material_type_var.set(material_type_options[0])
        self.search_material_type_widget.config(values=material_type_options)

    # properties methods
    @property
    def material_name(self):
        return self.material_name_var.get()

    @property
    def material_type(self):
        return self.material_type_var.get()

    @property
    def material_new_type(self):
        return self.material_new_type_var.get()

    @property
    def material_unit(self):
        return self.material_unit_var.get()

    @property
    def material_price(self):
        return self.material_price_var.get()

    @property
    def material_note(self):
        return self.material_note_var.get()

    @property
    def material_count(self):
        return self.material_count_var.get()

    @property
    def material_usage(self):
        return self.material_usage_var.get()

    @property
    def material_user(self):
        return self.material_user_var.get()

    @property
    def search_type(self):
        return self.search_type_var.get()

    @property
    def search_key(self):
        return self.search_key_var.get()

    @property
    def search_material_type(self):
        return self.search_material_type_var.get()

    def _cancel_operate(self):
        '''
        let control panel's main header's operation data filed be the default value
        :return:
        '''
        self.material_name_var.set('')
        self.material_type_var.set('')
        self.material_new_type_var.set('')
        self.material_unit_var.set('')
        self.material_count_var.set(0)
        self.material_price_var.set(0.0)
        self.material_note_var.set('')
        self.material_user_var.set('')
        self.material_usage_var.set('')

    def _post_operate(self):
        '''
        this method used to redraw data table after operate
        '''
        self.current_page = 1
        self.page_obj_count = self.i_get_page_obj_count()
        self.page_count = self._get_page_count()
        self._fresh_page_data()

    def _search(self):
        '''
        this is a generalized search handler for search action
        :return:
        '''
        if not self.search_key:
            tkMessageBox.showwarning(_.search_warning_title, _.search_key_none_warning_msg)
            return

        self._post_search()

    def _search_reset(self):
        '''
        Clean search field value and refresh data table
        '''
        self.search_key_var.set('')
        if self._is_material_search():
            self.search_material_type_var.set('')
        self._post_operate()

    def _post_search(self):
        '''
        this method will be called after search operation
        :return:
        '''
        self.current_page = 1
        self.page_obj_count = self.i_get_page_obj_count()
        self.page_count = self._get_page_count()
        self._fresh_page_data()
    
    def i_export(self):
        '''Export current page objects of normal or search results'''
        #TODO
        raise NotImplementedError('export method should be implemented by subclass')

    def _is_user_search(self):
        return self.search_type == USER_SEARCH

    def _is_material_search(self):
        return self.search_type == MATERIAL_SEARCH

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

    def i_fill_page_data_table(self):
        """
        using self.page_objs to fill self.page_table_entry_values,
        self.page_objs depends on user selected operations: search/create
        """
        raise NotImplemented('method not implemented yet!')

    def _create_label(self, x, y, text, width=50, **config):
        """
        draw label text on control panel's header
        """

        self.main_canvas.create_text(x, y, text='%6s' % text, width=width, **config)

    def _create_widget(self, x, y, widget, **config):
        '''
        draw tkinter widget on control panel's header
        '''
        self.main_canvas.create_window(x, y, window=widget, **config)

    def _set_page_table_info_msg(self):
        '''
        setting data table's page navigation infomation
        '''
        self.page_table_info_msg.set(
            PAGE_INFO_SEPARATOR.join(map(str, [self.current_page, self.page_count])))

    def _get_page_count(self):
        return (self.page_obj_count / MAX_TABLE_ROW) if self.page_obj_count % MAX_TABLE_ROW == 0 else (
            self.page_obj_count / MAX_TABLE_ROW + 1)

    def i_paint_main_head(self):
        """
        draw the control panel's main header
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
        get current data table's header string list
        '''
        raise NotImplemented('method not implemented yet!')

    def i_get_page_obj_count(self):
        '''
        get current control panel's related object's all count
        '''
        raise NotImplemented('method not implemented yet!')

    def _repeat_record_check(self):
        '''
        check if current operate record is the same as before
        :return: bool
        '''
        current_record_id = self._get_record_id()
        if self.last_record_id is None:
            self.last_record_id = current_record_id
            return True
        else:
            if current_record_id == self.last_record_id:
                if self.control_panel_type == IN_MATERIAL:
                    answer = tkMessageBox.askyesno(_.in_material_confirm_title, _.in_material_confirm_msg)
                    if not answer:
                        return False
                elif self.control_panel_type == OUT_MATERIAL:
                    answer = tkMessageBox.askyesno(_.out_material_confirm_title, _.out_material_confirm_msg)
                    if not answer:
                        return False
                return True
            else:
                self.last_record_id = current_record_id
                return True

    def _get_record_id(self):
        """
        generate a identity string for current operating data
        used to compare user's last 2 operation data
        :rtype: str
        """
        return "".join(
            (self.material_name, self.material_type, str(self.material_count), self.material_usage, self.material_user))

    def _update_user(self, username):
        '''
        Both "InMaterial" and "OutMaterial" operations will affect user entry, to avoid operate without user
        :param username:
        :return: user
        '''
        user = USER_UTIL.get_object_by_name(username)
        if not user:
            user = User.new_(username)
            USER_UTIL.add(user)
        return user

    def _update_material(self, material_name, material_type, material_count):
        '''
        this method mainly used to update material's count number depens on the control panel's type
        :param material_name:
        :param material_type:
        :param material_count:
        :return: Material
        '''
        material = MATERIAL_UTIL.get_object_by_name_and_type(material_name, material_type)
        if material is None:
            tkMessageBox.showwarning(_.update_material_warning_title, _.material_not_exists)
            return None

        if self.control_panel_type == IN_MATERIAL:
            material.count += material_count
        elif self.control_panel_type == OUT_MATERIAL:
            if material.count < material_count:
                tkMessageBox.showwarning(_.update_material_warning_title, _.out_material_count_over_msg)
                return
            else:
                material.count -= material_count
        MATERIAL_UTIL.add(material)
        return material
