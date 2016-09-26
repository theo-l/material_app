# encoding: utf-8
'''
控制面板的基类
'''
import ttk
import Tkinter as tk
from gui import util
from gui.constants import MAX_TABLE_ROW, PAGE_INFO_SEPARATOR


class ControlPanel(tk.Frame):

    #     PAGE_INFO_SEP = "/"
    #     max_table_row = 20
    max_table_col = None,
    table_entry_width = 13
    table_start_row = 8
    page_table_titles = []
    pageTableEntriesValue = []
    page_table_entries = []
    page_table_info_msg = None
    page_obj_count = 0
    page_count = 1
    current_page = 1
    page_objs = None

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.initStaticData()
        self.initDynamicData()
        self.paintPanel()

    def initStaticData(self):
        """
        初始化控制面板的静态数据
        """

        self.page_table_titles = self.i_getPageTableTitles()
        self.max_table_col = len(self.page_table_titles)

        self.pageTableEntriesValue = [
            [tk.StringVar() for i in xrange(self.max_table_col)] for j in xrange(MAX_TABLE_ROW)
        ]

        self.page_table_entries = [
            [ttk.Entry(self, width=self.table_entry_width, textvariable=self.pageTableEntriesValue[j][i])
             for i in xrange(self.max_table_col)] for j in xrange(MAX_TABLE_ROW)
        ]
        self.page_table_info_msg = tk.StringVar()

        self.i_initMainHeadVars()

    def initDynamicData(self):
        """
        初始化控制面板的动态数据
        """
        self.page_obj_count = self.i_getPageObjCount()
        self.page_count = self.page_obj_count / MAX_TABLE_ROW + 1
        self.current_page = 1
        self._setPageTableInfoMsg()
        self.page_objs = self.i_getCurrentPageObjs()
        self.i_fillPageDataTable()

    def paintPanel(self):
        """
        绘制控制面板UI
        """
        util.addHorizontalSpace(self, 11, 0)
        self.i_paintMainHead()
        util.addHorizontalSeparator(self, 11, 2)
        self.paintDataTable()

    def paintDataTable(self):
        """
        绘制控制面板中的数据表格
        """
        current_row = self.table_start_row

        # 绘制表头
        for (col, name) in enumerate(self.page_table_titles):
            ttk.Label(self, text=name, width=self.table_entry_width).grid(
                row=current_row, column=col)

        current_row += 1

        # 绘制数据表格
        for row in xrange(MAX_TABLE_ROW):
            for col in xrange(self.max_table_col):
                self.page_table_entries[row][col].grid(
                    row=current_row, column=col)
            current_row += 1

        util.addHorizontalSeparator(self, 11, current_row)
        self._paintTablePagination(current_row + 3)

    def _paintTablePagination(self, row):
        """
        绘制数据表格的导航按钮
        """
        util.makePreButton(self, row, 0)
        ttk.Label(self, textvariable=self.page_table_info_msg).grid(
            row=row, column=1)
        self._setPageTableInfoMsg()
        util.makeNextButton(self, row, 2)

    def _prePage(self):
        """
        上一页导航按钮的事件处理器
        """
        if self.current_page <= 1:
            return
        self.current_page -= 1
        self._freshPageData()

    def _nextPage(self):
        """
        下一页导航按钮的事件处理器
        """
        if self.current_page >= self.page_count:
            return
        self.current_page += 1
        self._freshPageData()

    def _freshPageData(self):
        """
        刷新当前页面的数据以及表格
        """
        self._setPageTableInfoMsg()
        self.page_objs = self.i_getCurrentPageObjs()
        self._cleanPageDataTable()
        self.i_fillPageDataTable()

    def _cleanPageDataTable(self):
        """
        清除数据表格中的所有数据
        """
        for row in self.pageTableEntriesValue:
            for col in row:
                col.set('')

    def _addMainHeadLabel(self, text, row, column, width=10):
        """
        在控制面板头中绘制标签组件
        """
        return ttk.Label(self, text=text, width=width).grid(row=row, column=column)

    def _setPageTableInfoMsg(self):
        '''
        设置页面导航的页面信息
        '''
        self.page_table_info_msg.set(
            PAGE_INFO_SEPARATOR.join(map(str, [self.current_page, self.page_count])))

    def i_initMainHeadVars(self):
        """
           初始化控制面板头中的一些变量
        """
        raise NotImplemented('method not implemented yet!')

    def i_paintMainHead(self):
        """
        绘制控制面板中的主要头
        """
        raise NotImplemented('method not implemented yet!')

    def i_fillPageDataTable(self):
        """
        使用当前页面中的数据对象来填充数据表格
        """
        raise NotImplemented('method not implemented yet!')

    def i_getCurrentPageObjs(self):
        '''
        根据当前的页面信息来获取当前页面的数据对象集合
        '''
        raise NotImplemented('method not implemented yet!')

    def i_getPageTableTitles(self):
        '''
        用来设置页面数据表格的标题信息
        '''
        raise NotImplemented('method not implemented yet!')

    def i_getPageObjCount(self):
        '''
        获取页面数据对象的总数
        '''
        raise NotImplemented('method not implemented yet!')
