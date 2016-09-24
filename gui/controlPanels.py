# encoding: utf-8
'''
通用控制面板类
'''
import ttk
import Tix
import Tkinter as tk
import tkFileDialog
import tkMessageBox
from gui import util as gutil
from gui import messages as _
from model import Material, MATERIAL_UTIL, User, USER_UTIL, InMaterial, INMATERIAL_UTIL, OutMaterial, OUTMATERIAL_UTIL

USER_SEARCH = 'user'
MATERIAL_SEARCH = 'material'


class ControlPanel(tk.Frame):

    PAGE_INFO_SEP = "/"
    max_table_row = 20
    max_table_col = None,
    table_entry_width = 13
    table_start_row = 8
    page_table_titles = []
    page_table_entries_value = []
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

        self.page_table_entries_value = [
            [tk.StringVar() for i in xrange(self.max_table_col)] for j in xrange(self.max_table_row)
        ]

        self.page_table_entries = [
            [ttk.Entry(self, width=self.table_entry_width, textvariable=self.page_table_entries_value[j][i])
             for i in xrange(self.max_table_col)] for j in xrange(self.max_table_row)
        ]
        self.page_table_info_msg = tk.StringVar()

        self.i_initMainHeadVars()

    def initDynamicData(self):
        """
        初始化控制面板的动态数据
        """
        self.page_obj_count = self.i_getPageObjCount()
        self.page_count = self.page_obj_count / self.max_table_row + 1
        self.current_page = 1
        self._setPageTableInfoMsg()
        self.page_objs = self.i_getCurrentPageObjs()
        self.i_fillPageDataTable()

    def paintPanel(self):
        """
        绘制控制面板UI
        """
        gutil.addHorizontalSpace(self, 11, 0)
        self.i_paintMainHead()
        gutil.addHorizontalSeparator(self, 11, 2)
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
        for row in xrange(self.max_table_row):
            for col in xrange(self.max_table_col):
                self.page_table_entries[row][col].grid(
                    row=current_row, column=col)
            current_row += 1

        gutil.addHorizontalSeparator(self, 11, current_row)
        self._paintTablePagination(current_row + 3)

    def _paintTablePagination(self, row):
        """
        绘制数据表格的导航按钮
        """
        gutil.makePreButton(self, row, 0)
        ttk.Label(self, textvariable=self.page_table_info_msg).grid(
            row=row, column=1)
        self._setPageTableInfoMsg()
        gutil.makeNextButton(self, row, 2)

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
        for row in self.page_table_entries_value:
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
            ControlPanel.PAGE_INFO_SEP.join(map(str, [self.current_page, self.page_count])))

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


class MaterialPanel(ControlPanel):
    '''
    材料控制面板
    1. 从文件导入材料信息
    2. 显示材料信息表格

    '''

    def __init__(self, master):
        ControlPanel.__init__(self, master)
        self.bind('<Enter>', self.enterHandler)

    def enterHandler(self, event):
        self._freshPageData()

    def i_initMainHeadVars(self):
        pass

    def i_getPageTableTitles(self):
        return _.material_table_titles

    def i_getPageObjCount(self):
        return MATERIAL_UTIL.getCount()

    def i_getCurrentPageObjs(self):
        start = (self.current_page - 1) * self.max_table_row
        end = start + self.max_table_row
        return MATERIAL_UTIL.getAllObjects()[start:end]

    def i_fillPageDataTable(self):
        for (row, obj) in enumerate(self.page_objs):
            rowData = self.page_table_entries_value[row]
            objFields = obj.get_ui_list()
            for col in xrange(self.max_table_col):
                rowData[col].set(objFields[col])

    def i_paintMainHead(self):
        mainHeadRow = 1
        ttk.Button(
            self, text=_.material_file_upload, command=self.__importMaterialFromFile).grid(row=mainHeadRow, column=0)

        ttk.Button(self, text=_.refresh, command=self._freshPageData).grid(
            row=mainHeadRow, column=2)

    def __importMaterialFromFile(self):
        materialFile = tkFileDialog.askopenfile(mode="r")

        if materialFile is None:
            return

        emptyLinePassed = False
        titleLineFound = False
        materialNameIndex = None
        materialTypeIndex = None
        import re
        for line in materialFile.readlines():
            fields = [item.strip(" \n").decode(gutil.ENCODING)
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
        self.initDynamicData()

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


class InMaterialPanel(ControlPanel):
    '''
    材料入库控制面板
    1.  填充材料入库的材料名、型号、数目、入库人信息
    2.  绘制入库数据记录信息表格
    '''

    def __init__(self, master):
        ControlPanel.__init__(self, master)

    def paintPanel(self):

        self.i_paintMainHead()
        self.paintDataTable()

    def paintDataTable(self):

        self.dataTableFrame = tk.Frame(
            self, width=680, height=580)
        self.mainCanvas.create_window(
            320, 20, window=self.dataTableFrame, anchor=tk.NW)

        self.page_table_entries = [
            [ttk.Entry(self.dataTableFrame, width=self.table_entry_width, textvariable=self.page_table_entries_value[j][i])
             for i in xrange(self.max_table_col)] for j in xrange(self.max_table_row)
        ]

        current_row = 0
        for (col, name) in enumerate(self.page_table_titles):
            ttk.Label(self.dataTableFrame, text=name, width=self.table_entry_width).grid(
                row=current_row, column=col)

        current_row += 1

        for row in xrange(self.max_table_row):
            for col in xrange(self.max_table_col):
                self.page_table_entries[row][col].grid(
                    row=current_row, column=col)
            current_row += 1

        gutil.addHorizontalSeparator(self.dataTableFrame, 5, current_row)
        self._paintTablePagination(current_row + 2)

    def _paintTablePagination(self, row):

        gutil.makePreButton(self.dataTableFrame, row, 0, handler=self._prePage)
        ttk.Label(
            self.dataTableFrame, textvariable=self.page_table_info_msg).grid(row=row, column=1)
        gutil.makeNextButton(
            self.dataTableFrame, row, 2, handler=self._nextPage)

    def i_initMainHeadVars(self):
        self.materialNameVar = tk.StringVar()
        self.materialTypeVar = tk.StringVar()
        self.materialInCountVar = tk.IntVar()
        self.materialInUservar = tk.StringVar()
        self.searchKeyVar = tk.StringVar()
        self.searchKeyVar.set(_.search_key_place_hold)
        self.searchType = tk.StringVar()
        self.searchType.set(USER_SEARCH)
        # 当前入库记录数据的标识符值
        self.lastRecordID = None

    def i_getPageTableTitles(self):
        return _.in_material_table_titles

    def i_getPageObjCount(self):
        return INMATERIAL_UTIL.getCount()

    def i_getCurrentPageObjs(self):
        start = (self.current_page - 1) * self.max_table_row
        end = start + self.max_table_row
        searchKey = self.searchKeyVar.get()
        if not searchKey:
            return INMATERIAL_UTIL.getAllObjects()[start:end]

        if self.searchType.get() == USER_SEARCH:
            user = USER_UTIL.getObjectByName(searchKey)
            return INMATERIAL_UTIL.getInListByUser(user)[start:end]

        if self.searchType.get() == MATERIAL_SEARCH:
            material = MATERIAL_UTIL.getObjectByName(searchKey)
            return INMATERIAL_UTIL.getInListByMaterial(material)[start:end]

    def i_fillPageDataTable(self):

        for (row, obj) in enumerate(self.page_objs):
            rowData = self.page_table_entries_value[row]
            objFields = obj.get_ui_list()
            user = USER_UTIL.getObjectById(objFields[0])
            material = MATERIAL_UTIL.getObjectById(objFields[1])
            objFields[0:3] = (user.name, material.name, material.type_no)
            for col in xrange(self.max_table_col):
                rowData[col].set(objFields[col])

    def i_paintMainHead(self):

        self.mainCanvas = tk.Canvas(
            self, height=600, width=1000)

        self.mainCanvas.grid(row=0, column=0, sticky=tk.NSEW)

        labelX = 30
        entryX = 150
        itemY = 35
        stepY = 30
        labelPattern = '%6s'

        self.mainCanvas.create_text(
            labelX, itemY, width=50,  text=labelPattern % _.material_name_label)
        materialNameEntry = ttk.Entry(
            self.mainCanvas, textvariable=self.materialNameVar, width=13)
        materialNameEntry.bind('<FocusOut>', self.__reloadMaterialType)
        self.mainCanvas.create_window(entryX, itemY, window=materialNameEntry)

        itemY += stepY

        self.mainCanvas.create_text(
            labelX, itemY, width=50, text=labelPattern % _.material_type_label)
        self.materialTypeMenu = ttk.Combobox(
            self.mainCanvas, textvariable=self.materialTypeVar)
        self.materialTypeMenu.config(width=12)
        self.mainCanvas.create_window(
            entryX, itemY, window=self.materialTypeMenu, height=20)

        itemY += stepY

        self.mainCanvas.create_text(
            labelX, itemY, width=60, text=labelPattern % _.material_in_count_label)
        inCountEntry = ttk.Entry(
            self.mainCanvas, textvariable=self.materialInCountVar, width=13)
        self.mainCanvas.create_window(entryX, itemY, window=inCountEntry)

        itemY += stepY

        self.mainCanvas.create_text(
            labelX, itemY, width=60, text=labelPattern % _.material_in_user_laebl)
        inUserEntry = ttk.Entry(
            self.mainCanvas, textvariable=self.materialInUservar, width=13)
        self.mainCanvas.create_window(entryX, itemY, window=inUserEntry)

        itemY += stepY

        subBtn = ttk.Button(
            self.mainCanvas, text=_.material_in, command=self.__materialInHandle)
        self.mainCanvas.create_window(50, itemY, window=subBtn)

        cancelBtn = ttk.Button(
            self.mainCanvas, text=_.cancel, command=self.__cancelMaterialIn)
        self.mainCanvas.create_window(entryX, itemY, window=cancelBtn)

        self.mainCanvas.create_line(0, 200, 300, 200)

        itemY = 230
        # 搜索类型标签
        self.mainCanvas.create_text(
            labelX, itemY, width=60, text=labelPattern % _.search_type)

        # 搜索类型单选按钮
        userNameSearch = ttk.Radiobutton(
            self.mainCanvas, text=_.search_by_user, variable=self.searchType, value=USER_SEARCH)
        materialNameSearch = ttk.Radiobutton(
            self.mainCanvas, text=_.search_by_material, variable=self.searchType, value=MATERIAL_SEARCH)

        self.mainCanvas.create_window(entryX, itemY, window=userNameSearch)
        self.mainCanvas.create_window(
            entryX + 60, itemY, window=materialNameSearch)

        itemY += stepY
        self.mainCanvas.create_text(
            labelX, itemY, text=labelPattern % _.search_key_label)

        searchKey = ttk.Entry(self.mainCanvas, textvariable=self.searchKeyVar)
        self.mainCanvas.create_window(entryX, itemY, window=searchKey)

        searchButton = ttk.Button(
            self.mainCanvas, text=_.search, command=self.__search)
        self.mainCanvas.create_window(50, itemY, window=searchButton)

        searchResetButton = ttk.Button(
            self.mainCanvas, text=_.reset, command=self.__searchReset)
        self.mainCanvas.create_window(150, itemY, window=searchResetButton)

        self.mainCanvas.create_text(30,)

        # 绘制垂直分割线
        self.mainCanvas.create_line(300, 20, 300, 600)

    def __search(self):
        searchKey = self.searchKeyVar.get()
        if not searchKey:
            tkMessageBox.showinfo(
                _.search_warning_title, _.search_key_none_warning_msg)
            return

        if self.searchType.get() == USER_SEARCH:
            user = USER_UTIL.getObjectByName(searchKey)
            if not user:
                tkMessageBox.showwarning(
                    _.search_warning_title, _.user_not_exists)
                return
            self.page_obj_count = INMATERIAL_UTIL.getInListCountByUser(user)
            self.page_count = self.page_obj_count / self.max_table_row + 1
            self._freshPageData()

        if self.searchType.get() == MATERIAL_SEARCH:
            material = MATERIAL_UTIL.getObjectByName(searchKey)
            if not material:
                tkMessageBox.showwarning(
                    _.search_warning_title, _.material_not_exists)
                return
            self.page_obj_count = INMATERIAL_UTIL.getInListCountByMaterial(
                material)
            self.page_count = self.page_obj_count / self.max_table_row + 1
            self._freshPageData()

    def __searchReset(self):
        pass

    def __cancelMaterialIn(self):
        '''
        取消当前入库操作，清除用户输入的所有数据字段值
        '''
        self.materialNameVar.set('')
        self.materialTypeVar.set('')
        self.materialInCountVar.set(0)
        self.materialInUservar.set('')

    def __reloadMaterialType(self, event):
        materialName = self.materialNameVar.get()
        if not materialName:
            return

        materialTypeOption = MATERIAL_UTIL.getTypeNoByName(materialName)
        self.materialTypeVar.set(materialTypeOption[0])

    def __materialInHandle(self):
        try:
            (materialName, materialType, inCount, userName) = (
                self.materialNameVar.get().encode(gutil.ENCODING),
                self.materialTypeVar.get().encode(gutil.ENCODING),
                self.materialInCountVar.get(),
                self.materialInUservar.get().encode(gutil.ENCODING)
            )

            if inCount <= 0:
                tkMessageBox.showwarning(
                    _.in_material_warning_title, _.in_material_count_le_zero_msg)
                return
        except ValueError:
            tkMessageBox.showwarning(
                _.in_material_warning_title, _.in_material_count_non_num_msg)
            return

        if not materialName or not materialType or not inCount or not userName:
            tkMessageBox.showwarning(
                _.in_material_warning_title, _.in_material_field_required_msg)
            return

        if self.lastRecordID is None:
            self.lastRecordID = "".join(
                (materialName, materialType, str(inCount), userName))
        else:
            currentRecordID = "".join(
                (materialName, materialType, str(inCount), userName))
            if currentRecordID == self.lastRecordID:
                answer = tkMessageBox.askyesno(
                    _.in_material_confirm_title, _.in_material_confirm_msg)
                if not answer:
                    return
            else:
                self.lastRecordID = currentRecordID

        material = self.__updateMaterial(
            materialName.decode(gutil.ENCODING), materialType.decode(gutil.ENCODING), inCount)

        if material is None:
            return

        user = self.__updateUser(userName)
        if user is None:
            return

        self.__updateInMaterial(user.id, material.id, inCount)

        # 入库之后更新页面的数据表格
        self.initDynamicData()

    def __updateMaterial(self, name, type_no, count):

        material = MATERIAL_UTIL.getObjectByNameAndType(name, type_no)
        if material is not None:
            material.count += count
        else:
            material = Material.new_(name, type, count)
            MATERIAL_UTIL.add(material)
        MATERIAL_UTIL.commit()
        return material

    def __updateUser(self, username):
        user = USER_UTIL.getObjectByName(username)
        if user is None:
            user = User.new_(username)
            USER_UTIL.add(user)
            USER_UTIL.commit()
        return user

    def __updateInMaterial(self, userId, materialId, count):
        inMaterial = InMaterial(
            user_id=userId, material_id=materialId, count=count)
        INMATERIAL_UTIL.add(inMaterial)
        INMATERIAL_UTIL.commit()


class OutMaterialPanel(ControlPanel):
    '''
    绘制材料出库控制面板
    1. 填充材料出库的材料名称、型号、数目、用途、领料人
    2. 绘制材料出库数据信息表格
    '''

    def __init__(self, master):
        ControlPanel.__init__(self, master)

    def i_initMainHeadVars(self):
        self.materialNameVar = tk.StringVar()
        self.materialTypeVar = tk.StringVar()
        self.materialOutCountVar = tk.IntVar()
        self.materialUsageVar = tk.StringVar()
        self.materialOutUserVar = tk.StringVar()

        self.lastRecordID = None

    def i_getPageTableTitles(self):
        return _.out_material_table_titles

    def i_getPageObjCount(self):
        return OUTMATERIAL_UTIL.getCount()

    def i_getCurrentPageObjs(self):
        start = (self.current_page - 1) * self.max_table_row
        end = start + self.max_table_row
        return OUTMATERIAL_UTIL.getAllObjects()[start:end]

    def paintPanel(self):
        self.i_paintMainHead()
        self.paintDataTable()

    def paintDataTable(self):
        current_row = 0

        self.page_table_entries = [
            [ttk.Entry(self.dataTableFrame, width=self.table_entry_width, textvariable=self.page_table_entries_value[j][i])
             for i in xrange(self.max_table_col)] for j in xrange(self.max_table_row)
        ]

        # 绘制表头
        for (col, name) in enumerate(self.page_table_titles):
            ttk.Label(self.dataTableFrame, text=name, width=self.table_entry_width).grid(
                row=current_row, column=col)

        current_row += 1

        # 绘制数据表格
        for row in xrange(self.max_table_row):
            for col in xrange(self.max_table_col):
                self.page_table_entries[row][col].grid(
                    row=current_row, column=col)
            current_row += 1

        gutil.addHorizontalSeparator(self.dataTableFrame, 6, current_row)
        self._paintTablePagination(current_row + 2)

    def _paintTablePagination(self, row):
        gutil.makePreButton(self.dataTableFrame, row, 0, handler=self._prePage)
        ttk.Label(
            self.dataTableFrame, textvariable=self.page_table_info_msg).grid(row=row, column=1)
        gutil.makeNextButton(
            self.dataTableFrame, row, 2, handler=self._nextPage)

    def i_fillPageDataTable(self):
        for (row, obj) in enumerate(self.page_objs):
            rowData = self.page_table_entries_value[row]
            objFields = obj.get_ui_list()
            user = USER_UTIL.getObjectById(objFields[0])
            material = MATERIAL_UTIL.getObjectById(objFields[1])
            objFields[0:3] = (user.name, material.name, material.type_no)
            for col in xrange(self.max_table_col):
                rowData[col].set(objFields[col])

    def i_paintMainHead(self):

        labelX = 30
        entryX = 150
        itemY = 35
        stepY = 35
        self.mainCanvas = tk.Canvas(
            self, width=1000, height=600)
        self.mainCanvas.grid(row=0, column=0, sticky=tk.NSEW)

        self.dataTableFrame = tk.Frame(
            self.mainCanvas, width=680, height=580)
        self.mainCanvas.create_window(
            320, 20, window=self.dataTableFrame, anchor=tk.NW)

        self.mainCanvas.create_text(
            labelX, itemY, text='%8s' % _.material_name_label)
        materialNameEntry = ttk.Entry(
            self.mainCanvas, textvariable=self.materialNameVar, width=13)
        materialNameEntry.bind('<FocusOut>', self.__reloadMaterialType)
        self.mainCanvas.create_window(entryX, itemY, window=materialNameEntry)

        itemY += stepY

        self.mainCanvas.create_text(
            labelX, itemY, text='%8s' % _.material_type_label)
        self.materialTypeMenu = ttk.Combobox(
            self.mainCanvas, textvariable=self.materialTypeVar)
        self.materialTypeMenu.config(width=12)
        self.mainCanvas.create_window(
            entryX, itemY, window=self.materialTypeMenu, height=20)

        itemY += stepY

        self.mainCanvas.create_text(
            labelX, itemY, text='%8s' % _.material_out_count_label)
        outCountEntry = ttk.Entry(
            self.mainCanvas, textvariable=self.materialOutCountVar, width=13)
        self.mainCanvas.create_window(entryX, itemY, window=outCountEntry)

        itemY += stepY

        self.mainCanvas.create_text(
            labelX, itemY, text='%8s' % _.material_out_usage_label)
        outUsageEntry = ttk.Entry(
            self.mainCanvas, textvariable=self.materialUsageVar, width=13)
        self.mainCanvas.create_window(entryX, itemY, window=outUsageEntry)

        itemY += stepY

        self.mainCanvas.create_text(
            labelX, itemY, text='%8s' % _.material_out_user_label)
        outUserEntry = ttk.Entry(
            self.mainCanvas, textvariable=self.materialOutUserVar, width=13)
        self.mainCanvas.create_window(entryX, itemY, window=outUserEntry)

        itemY += stepY

        subBtn = ttk.Button(
            self.mainCanvas, text=_.material_out, command=self.__materialOutHandler)
        self.mainCanvas.create_window(50, itemY, window=subBtn)
        cancelBtn = ttk.Button(
            self.mainCanvas, text=_.cancel, command=self.__cancelMaterialOutHandler)
        self.mainCanvas.create_window(150, itemY, window=cancelBtn)

        self.mainCanvas.create_line(300, 20, 300, 600)

    def __reloadMaterialType(self, event):
        materialName = self.materialNameVar.get()
        if not materialName:
            return
        materialTypeOption = MATERIAL_UTIL.getTypeNoByName(materialName)

        self.materialTypeVar.set(materialTypeOption[0])
        self.materialTypeMenu.config(values=materialTypeOption)

    def __cancelMaterialOutHandler(self):
        '重置所有填充的入库信息'
        self.materialNameVar.set('')
        self.materialTypeVar.set('')
        self.materialOutCountVar.set(0)
        self.materialUsageVar.set('')
        self.materialOutUserVar.set('')

    def __materialOutHandler(self):
        "出库逻辑处理"
        # 根据材料名称和型号判断材料库存
        # 材料库存处理
        # 领料人处理
        # 出库记录处理
        try:
            (materialName, materialType, outCount, usage, username) = (
                self.materialNameVar.get().encode(gutil.ENCODING),
                self.materialTypeVar.get().encode(gutil.ENCODING),
                self.materialOutCountVar.get(),
                self.materialUsageVar.get().encode(gutil.ENCODING),
                self.materialOutUserVar.get().encode(gutil.ENCODING)
            )
            if outCount <= 0:
                tkMessageBox.showwarning(
                    _.out_material_warning_title, _.out_material_count_le_zero_msg)
                return
        except ValueError:
            tkMessageBox.showwarning(
                _.out_material_warning_title, _.out_material_count_non_num_msg)
            return

        if not materialName or not materialType or not outCount or not usage or not username:
            tkMessageBox.showwarning(
                _.out_material_warning_title, _.out_material_field_required_msg)
            return

        if self.lastRecordID is None:
            self.lastRecordID = "".join(
                (materialName, materialType, str(outCount), usage, username))
        else:
            currentRecordID = "".join(
                (materialName, materialType, str(outCount), usage, username))
            if currentRecordID == self.lastRecordID:
                answer = tkMessageBox.askyesno(
                    _.out_material_confirm_title, _.out_material_confirm_msg)
                if not answer:
                    return
            else:
                self.lastRecordID = currentRecordID

        material = self.__updateMaterial(materialName.decode(
            gutil.ENCODING), materialType.decode(gutil.ENCODING), outCount)
        if material is None:
            return

        user = self.__updateUser(username.decode(gutil.ENCODING))
        if user is None:
            return

        self.__updateOutMaterial(user.id, material.id, outCount, usage)
        self.initDynamicData()

    def __updateMaterial(self, name, type_no, count):
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

    def __updateUser(self, username):
        user = USER_UTIL.getObjectByName(username)
        if user is None:
            user = User.new_(username)
            USER_UTIL.add(user)
            USER_UTIL.commit()
        return user

    def __updateOutMaterial(self, userId, materialId, count, usage):
        outMaterial = OutMaterial(
            user_id=userId, material_id=materialId, count=count, usage=usage)
        OUTMATERIAL_UTIL.add(outMaterial)
        OUTMATERIAL_UTIL.commit()
