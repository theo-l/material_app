# encoding: utf-8
'''
主要用户界面
'''
import ttk
import Tkinter as tk
import tkMessageBox

from model import USER_UTIL, install_database
from gui.constants import WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_TITLE, LOGIN_PANEL_NAME, \
    LOGOUT_PANEL_NAME, MATERIAL_PANEL_NAME, IN_MATERIAL_PANEL_NAME, OUT_MATERIAL_PANEL_NAME, QUERY_PANEL_NAME
from gui.panels import MaterialPanel, InMaterialPanel, OutMaterialPanel
from gui import messages as _
from gui.config import DEBUG


class Application(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.LOGGED_IN = False
        self.USER = None
        self.WIDTH = WINDOW_WIDTH
        self.HEIGHT = WINDOW_HEIGHT
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.resizable(False, False)
        self.title(WINDOW_TITLE)
        install_database()
        self.init_components()

    def init_components(self):
        self.create_main_panel()
        self.create_login_panel()
        self.create_material_panel()
        self.create_in_material_panel()
        self.create_out_material_panel()
        self.create_query_panel()
        self.create_logout_panel()

        self.main.add(self.login_panel, text=LOGIN_PANEL_NAME)
        self.main.pack(fill=tk.BOTH, expand=tk.YES)

    def create_main_panel(self):
        "创建主要的控制面板容器"
        self.main = ttk.Notebook(self, width=self.WIDTH, height=self.HEIGHT)

    def create_login_panel(self):
        "创建登录控制面板"
        self.login_panel = ttk.Frame(self.main)
        self.login_msg_var = tk.StringVar()
        self.paint_login_panel()

    def create_material_panel(self):
        "创建材料管理面板"
        self.material_panel = MaterialPanel(self)

    def create_in_material_panel(self):
        "创建入库控制面板"
        self.in_material_panel = InMaterialPanel(self.main)

    def create_out_material_panel(self):
        "创建出库控制面板"
        self.out_material_panel = OutMaterialPanel(self.main)

    def create_query_panel(self):
        "创建查询控制面板"
        self.query_panel = ttk.Frame(self.main)

    def create_logout_panel(self):
        "创建注销控制面板"
        self.logout_panel = ttk.Frame(self.main)
        self.paint_logout_panel()

    def paint_login_panel(self):
        '绘制登录控制面板'

        self.login_msg = tk.Label(self.login_panel, textvariable=self.login_msg_var,
                                  foreground="red", font=('times', 12, 'bold'))
        ttk.Label(self.login_panel, text=_.login_username).grid(
            column=0, row=1)
        tk.Entry(self.login_panel, textvariable=self.username).grid(
            column=1, row=1)

        ttk.Label(self.login_panel, text=_.login_password).grid(
            column=0, row=2)
        tk.Entry(self.login_panel, textvariable=self.password,
                 show="*").grid(column=1, row=2)

        if DEBUG:
            self.username.set('test')
            self.password.set('test')

        ttk.Button(
            self.login_panel, text=_.login, command=self.login).grid(row=3)

    def paint_logout_panel(self):
        "绘制注销控制面板"
        ttk.Button(self.logout_panel, text=_.logout, command=self.logout).pack(
            anchor=tk.CENTER)

    def login(self):
        "登录相关操作实现"

        self.USER = USER_UTIL.getObjectByNameAndPassword(
            self.username.get(), self.password.get())

        self.LOGGED_IN = self.USER is not None

        if self.LOGGED_IN:
            self.login_msg_var.set('')  # 重置登录消息标签
            self.main.forget(self.login_panel)
            self.main.add(self.material_panel, text=MATERIAL_PANEL_NAME)
            self.main.add(self.in_material_panel, text=IN_MATERIAL_PANEL_NAME)
            self.main.add(self.out_material_panel, text=OUT_MATERIAL_PANEL_NAME)
            self.main.add(self.query_panel, text=QUERY_PANEL_NAME)
            self.main.add(self.logout_panel, text=LOGOUT_PANEL_NAME)
        else:
            self.login_msg.grid(row=0, columnspan=2)
            self.login_msg_var.set(_.login_error_msg)

    def logout(self):

        if tkMessageBox.askyesno(_.logout_query_title, _.logout_query_msg):
            self.LOGGED_IN = False
            self.main.add(self.login_panel, text=LOGIN_PANEL_NAME)
            self.main.forget(self.material_panel)
            self.main.forget(self.in_material_panel)
            self.main.forget(self.out_material_panel)
            self.main.forget(self.query_panel)
            self.main.forget(self.logout_panel)


def main():
    app = Application()
    app.mainloop()

if __name__ == '__main__':
    main()
