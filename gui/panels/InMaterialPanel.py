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
from gui.constants import MAX_TABLE_ROW
from gui.constants import MATERIAL_SEARCH, USER_SEARCH

from model import USER_UTIL, MATERIAL_UTIL, INMATERIAL_UTIL, User, Material, InMaterial


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
            [ttk.Entry(self.dataTableFrame, width=self.table_entry_width, textvariable=self.pageTableEntriesValue[j][i])
             for i in xrange(self.max_table_col)] for j in xrange(MAX_TABLE_ROW)
        ]

        current_row = 0
        for (col, name) in enumerate(self.page_table_titles):
            ttk.Label(self.dataTableFrame, text=name, width=self.table_entry_width).grid(
                row=current_row, column=col)

        current_row += 1

        for row in xrange(MAX_TABLE_ROW):
            for col in xrange(self.max_table_col):
                self.page_table_entries[row][col].grid(
                    row=current_row, column=col)
            current_row += 1

        util.addHorizontalSeparator(self.dataTableFrame, 5, current_row)
        self._paintTablePagination(current_row + 2)

    def _paintTablePagination(self, row):

        util.makePreButton(self.dataTableFrame, row, 0, handler=self._prePage)
        ttk.Label(
            self.dataTableFrame, textvariable=self.page_table_info_msg).grid(row=row, column=1)
        util.makeNextButton(
            self.dataTableFrame, row, 2, handler=self._nextPage)

    def i_initMainHeadVars(self):
        self.materialNameVar = tk.StringVar()
        self.materialTypeVar = tk.StringVar()
        self.materialInCountVar = tk.IntVar()
        self.materialInUservar = tk.StringVar()
        self.searchKeyVar = tk.StringVar()
        self.searchKeyVar.set('')
        self.searchMaterialTypeVar = tk.StringVar()
        self.searchTypeVar = tk.StringVar()
        self.searchTypeVar.set(USER_SEARCH)

        # 材料搜索下拉框标签和组件的位置
        self.materialTypeLabelX = None
        self.materialTypeLabelY = None
        self.materialTypeEntryX = None
        self.materialTypeEntryY = None

        # 当前入库记录数据的标识符值
        self.lastRecordID = None

    def i_getPageTableTitles(self):
        return _.in_material_table_titles

    def i_getPageObjCount(self):
        return INMATERIAL_UTIL.getCount()

    def i_getCurrentPageObjs(self):
        start = (self.current_page - 1) * MAX_TABLE_ROW
        end = start + MAX_TABLE_ROW
        searchKey = self.searchKeyVar.get()
        if not searchKey:
            return INMATERIAL_UTIL.getAllObjects()[start:end]

        if self.searchTypeVar.get() == USER_SEARCH:
            user = USER_UTIL.getObjectByName(searchKey)
            return INMATERIAL_UTIL.getInListByUser(user)[start:end]

        if self.searchTypeVar.get() == MATERIAL_SEARCH:
            materialName, materialType = self.searchKeyVar.get(
            ), self.searchMaterialTypeVar.get()
            material = MATERIAL_UTIL.getObjectByNameAndType(
                materialName, materialType)
            return INMATERIAL_UTIL.getInListByMaterial(material)[start:end]

    def i_fillPageDataTable(self):

        for (row, obj) in enumerate(self.page_objs):
            rowData = self.pageTableEntriesValue[row]
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
            labelX, itemY, width=60,  text=labelPattern % _.material_name_label)
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
        # 按用户搜索
        userNameSearch = ttk.Radiobutton(
            self.mainCanvas, text=_.search_by_user, command=self.__searchTypeHandler, variable=self.searchTypeVar,
            value=USER_SEARCH)
        # 按材料搜索: 会触发材料类型下拉框的显示
        materialNameSearch = ttk.Radiobutton(
            self.mainCanvas, text=_.search_by_material, variable=self.searchTypeVar, command=self.__searchTypeHandler,
            value=MATERIAL_SEARCH)

        self.mainCanvas.create_window(entryX, itemY, window=userNameSearch)
        self.mainCanvas.create_window(
            entryX + 60, itemY, window=materialNameSearch)

        itemY += stepY
        self.mainCanvas.create_text(
            labelX, itemY, text=labelPattern % _.search_key_label)

        # 主搜索关键字
        searchKey = ttk.Entry(
            self.mainCanvas, textvariable=self.searchKeyVar, width=18)
        searchKey.bind('<FocusOut>', self.__searchKeyHandler)
        self.mainCanvas.create_window(entryX, itemY, window=searchKey)

        # 搜索材料类型，入库搜索类型为材料的话则显示，否则不显示该组件
        self.searchMaterialType = ttk.Combobox(
            self.mainCanvas, textvariable=self.searchMaterialTypeVar)
        self.searchMaterialType.config(width=16)

        itemY += stepY
        self.materialTypeLabelX = labelX
        self.materialTypeLabelY = itemY
        self.materialTypeEntryX = entryX
        self.materialTypeEntryY = itemY

        itemY += stepY
        searchButton = ttk.Button(
            self.mainCanvas, text=_.search, command=self.__search)
        self.mainCanvas.create_window(50, itemY, window=searchButton)

        searchResetButton = ttk.Button(
            self.mainCanvas, text=_.reset, command=self.__searchReset)
        self.mainCanvas.create_window(150, itemY, window=searchResetButton)

        # self.mainCanvas.create_text(30,)

        # 绘制垂直分割线
        self.mainCanvas.create_line(300, 20, 300, 600)

    def __searchKeyHandler(self, event):
        '''
        根据用户选择的搜索类型来选择相关的事件处理
        1. 如果按用户搜索则不做任何处理
        2. 如果按材料搜索则重置材料型号下拉框选择值
        '''
        searchKey = self.searchKeyVar.get()
        if not searchKey:
            return

        if self.__isUerSearch():
            return

        typeOptions = MATERIAL_UTIL.getTypeNoByName(searchKey)
        self.searchMaterialTypeVar.set(typeOptions[0])
        self.searchMaterialType.config(values=typeOptions)

    def __searchTypeHandler(self):
        '''
           根据用户选择的搜索类型来控制页面搜索组件的显示效果
           1. 如果按用户搜索则在画布上去掉材料类型下拉框
           2. 如果按材料搜索则在画布上显示材料类型下拉框
        '''
        if self.searchTypeVar.get() == USER_SEARCH:
            self.mainCanvas.delete(self.materialTypeSearchLabel)
            self.searchMaterialType.grid_remove()
            self.mainCanvas.delete(self.searchMaterialTypeEntry)
        if self.searchTypeVar.get() == MATERIAL_SEARCH:
            self.materialTypeSearchLabel = self.mainCanvas.create_text(
                self.materialTypeLabelX, self.materialTypeLabelY, text=_.material_type_label)
            self.searchMaterialTypeEntry = self.mainCanvas.create_window(
                self.materialTypeEntryX, self.materialTypeEntryY, window=self.searchMaterialType, height=20)

    def __search(self):
        searchKey = self.searchKeyVar.get()
        if not searchKey:
            tkMessageBox.showinfo(
                _.search_warning_title, _.search_key_none_warning_msg)
            return

        if self.__isUerSearch():
            user = USER_UTIL.getObjectByName(searchKey)
            if not user:
                tkMessageBox.showwarning(
                    _.search_warning_title, _.user_not_exists)
                return
            self.page_obj_count = INMATERIAL_UTIL.getInListCountByUser(user)
            self.page_count = self.page_obj_count / MAX_TABLE_ROW + 1
            self._freshPageData()

        else:
            (materialName, materialType) = (
                self.searchKeyVar.get(), self.searchMaterialTypeVar.get())
            material = MATERIAL_UTIL.getObjectByNameAndType(
                materialName, materialType)
            if not material:
                tkMessageBox.showwarning(
                    _.search_warning_title, _.material_not_exists)
                return
            self.page_obj_count = INMATERIAL_UTIL.getInListCountByMaterial(
                material)
            self.page_count = self.page_obj_count / MAX_TABLE_ROW + 1
            self._freshPageData()

    def __searchReset(self):
        if self.__isUerSearch():
            self.searchKeyVar.set('')
        else:
            self.searchKeyVar.set('')
            self.searchMaterialTypeVar.set('')

        self.initDynamicData()

    def __isUerSearch(self):
        return self.searchTypeVar.get() == USER_SEARCH

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
        self.materialTypeMenu.config(values=materialTypeOption)

    def __materialInHandle(self):
        try:
            (materialName, materialType, inCount, userName) = (
                self.materialNameVar.get().encode(util.ENCODING),
                self.materialTypeVar.get().encode(util.ENCODING),
                self.materialInCountVar.get(),
                self.materialInUservar.get().encode(util.ENCODING)
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
            materialName.decode(util.ENCODING), materialType.decode(util.ENCODING), inCount)

        if material is None:
            return

        user = self.__updateUser(userName)
        if user is None:
            return

        self.__updateInMaterial(user.id, material.id, inCount)

        tkMessageBox.showinfo(_.in_material_info_title, _.in_material_succeed)

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
