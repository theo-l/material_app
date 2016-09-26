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
from gui.constants import MAX_TABLE_ROW
from gui.constants import MATERIAL_SEARCH, USER_SEARCH

from model import MATERIAL_UTIL, USER_UTIL, OUTMATERIAL_UTIL, Material, User, OutMaterial


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

        # 用户搜索类型
        self.searchTypeVar = tk.StringVar()
        self.searchTypeVar.set(USER_SEARCH)

        # 用户搜索关键字
        self.searchKeyVar = tk.StringVar()
        self.searchKeyVar.set('')

        # 搜索材料型号关键字
        self.searchMaterialTypeVar = tk.StringVar()
        self.searchMaterialTypeVar.set('')

        # 搜索材料型号标签和实体放置的位置
        self.materialTypeLabelX = None
        self.materialTypeLabelY = None
        self.materialTypeEntryX = None
        self.materialTypeEntryY = None

        self.lastRecordID = None

    def i_getPageTableTitles(self):
        return _.out_material_table_titles

    def i_getPageObjCount(self):
        return OUTMATERIAL_UTIL.getCount()

    def i_getCurrentPageObjs(self):
        start = (self.current_page - 1) * MAX_TABLE_ROW
        end = start + MAX_TABLE_ROW

        searchKey = self.searchKeyVar.get()
        if not searchKey:
            return OUTMATERIAL_UTIL.getAllObjects()[start:end]

        if self.__isUserSearch():
            user = USER_UTIL.getObjectByName(searchKey)
            return OUTMATERIAL_UTIL.getOutListByUser(user)[start:end]
        else:
            materialType = self.searchMaterialTypeVar.get()
            material = MATERIAL_UTIL.getObjectByNameAndType(
                searchKey, materialType)
            return OUTMATERIAL_UTIL.getOutListByMaterial(material)

    def paintPanel(self):
        self.i_paintMainHead()
        self.paintDataTable()

    def paintDataTable(self):
        current_row = 0

        self.page_table_entries = [
            [ttk.Entry(self.dataTableFrame, width=self.table_entry_width, textvariable=self.pageTableEntriesValue[j][i])
             for i in xrange(self.max_table_col)] for j in xrange(MAX_TABLE_ROW)
        ]

        # 绘制表头
        for (col, name) in enumerate(self.page_table_titles):
            ttk.Label(self.dataTableFrame, text=name, width=self.table_entry_width).grid(
                row=current_row, column=col)

        current_row += 1

        # 绘制数据表格
        for row in xrange(MAX_TABLE_ROW):
            for col in xrange(self.max_table_col):
                self.page_table_entries[row][col].grid(
                    row=current_row, column=col)
            current_row += 1

        util.addHorizontalSeparator(self.dataTableFrame, 6, current_row)
        self._paintTablePagination(current_row + 2)

    def _paintTablePagination(self, row):
        util.makePreButton(self.dataTableFrame, row, 0, handler=self._prePage)
        ttk.Label(
            self.dataTableFrame, textvariable=self.page_table_info_msg).grid(row=row, column=1)
        util.makeNextButton(
            self.dataTableFrame, row, 2, handler=self._nextPage)

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

        itemY += stepY

        # 绘制左边控制面板的上下分割线
        self.mainCanvas.create_line(0, itemY, 300, itemY)

        itemY += stepY

        # 绘制搜索类型标签文本
        self.mainCanvas.create_text(labelX, itemY, text=_.search_type)

        # 绘制搜索类型的单选按钮
        usernameSearch = ttk.Radiobutton(
            self.mainCanvas, text=_.search_by_user, variable=self.searchTypeVar, value=USER_SEARCH,
            command=self.__searchTypeHandler)
        self.mainCanvas.create_window(entryX, itemY, window=usernameSearch)

        materialSearch = ttk.Radiobutton(
            self.mainCanvas, text=_.search_by_material, variable=self.searchTypeVar, value=MATERIAL_SEARCH,
            command=self.__searchTypeHandler)
        self.mainCanvas.create_window(
            entryX + 60, itemY, window=materialSearch)

        itemY += stepY

        # 绘制搜索关键字
        self.mainCanvas.create_text(labelX, itemY, text=_.search_key_label)
        searchKey = ttk.Entry(self.mainCanvas, textvariable=self.searchKeyVar)
        searchKey.bind('<FocusOut>', self.__searchKeyFocusOutHandler)
        self.mainCanvas.create_window(entryX, itemY, window=searchKey)

        itemY += stepY
        self.searchMaterialType = ttk.Combobox(
            self.mainCanvas, textvariable=self.searchMaterialTypeVar, width=16)

        self.materialTypeLabelX = labelX
        self.materialTypeLabelY = itemY
        self.materialTypeEntryX = entryX
        self.materialTypeEntryY = itemY

        itemY += stepY
        search = ttk.Button(
            self.mainCanvas, command=self.__search, text=_.search)
        self.mainCanvas.create_window(50, itemY, window=search)

        reset = ttk.Button(
            self.mainCanvas, command=self.__searchReset, text=_.reset)
        self.mainCanvas.create_window(150, itemY, window=reset)

        # 绘制一个垂直分割线
        self.mainCanvas.create_line(300, 20, 300, 600)

    def __search(self):
        searchKey = self.searchKeyVar.get()
        if not searchKey:
            tkMessageBox.showwarning(
                _.search_warning_title, _.search_key_none_warning_msg)

        if self.__isUserSearch():
            user = USER_UTIL.getObjectByName(searchKey)
            if not user:
                tkMessageBox.showwarning(
                    _.search_warning_title, _.user_not_exists)
                return

            self.page_obj_count = OUTMATERIAL_UTIL.getOutListCountByUser(user)
            self.page_count = self.page_obj_count / MAX_TABLE_ROW + 1
            self._freshPageData()

        else:
            materialType = self.searchMaterialTypeVar.get()
            material = MATERIAL_UTIL.getObjectByNameAndType(
                searchKey, materialType)
            if not material:
                tkMessageBox.showwarning(
                    _.search_warning_title, _.material_not_exists)
                return
            self.page_obj_count = OUTMATERIAL_UTIL.getOutListCountByMaterial(
                material)
            self.page_count = self.page_obj_count / MAX_TABLE_ROW + 1
            self._freshPageData()

    def __searchReset(self):
        "取消当前的搜索结果"
        if self.__isUserSearch():
            self.searchKeyVar.set('')
        else:
            self.searchKeyVar.set('')
            self.searchMaterialTypeVar.set('')

        self.initDynamicData()

    def __searchKeyFocusOutHandler(self, event):

        searchKey = self.searchKeyVar.get()
        if not searchKey:
            return

        if self.__isUserSearch():
            return

        typeOptions = MATERIAL_UTIL.getTypeNoByName(searchKey)
        self.searchMaterialTypeVar.set(typeOptions[0])
        self.searchMaterialType.config(values=typeOptions)

    def __searchTypeHandler(self):
        '''
        处理用户选择的搜索类型单选按钮
        1. 按用户搜索时去掉材料型号标签和下拉框的显示
        2. 按材料搜索时显示材料型号标签和下拉框的显示
        '''
        if self.__isUserSearch():
            self.mainCanvas.delete(self.materialTypeSearchLabel)
            self.mainCanvas.delete(self.materialTypeSearchEntry)
        else:
            self.materialTypeSearchLabel = self.mainCanvas.create_text(
                self.materialTypeLabelX, self.materialTypeLabelY, text=_.material_type_label)
            self.materialTypeSearchEntry = self.mainCanvas.create_window(
                self.materialTypeEntryX, self.materialTypeEntryY, window=self.searchMaterialType)

    def __isUserSearch(self):
        return self.searchTypeVar.get() == USER_SEARCH

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
                self.materialNameVar.get().encode(util.ENCODING),
                self.materialTypeVar.get().encode(util.ENCODING),
                self.materialOutCountVar.get(),
                self.materialUsageVar.get().encode(util.ENCODING),
                self.materialOutUserVar.get().encode(util.ENCODING)
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
            util.ENCODING), materialType.decode(util.ENCODING), outCount)
        if material is None:
            return

        user = self.__updateUser(username.decode(util.ENCODING))
        if user is None:
            return

        self.__updateOutMaterial(user.id, material.id, outCount, usage)

        tkMessageBox.showinfo(
            _.out_material_info_title, _.out_material_succeed)
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
