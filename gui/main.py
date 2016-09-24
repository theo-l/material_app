# encoding: utf-8
'''
主要用户界面
'''
import ttk
import Tkinter as tk
import tkMessageBox

from model import USER_UTIL, install_database

from gui.controlPanels import InMaterialPanel, MaterialPanel, OutMaterialPanel


class Application(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.LOGGED_IN = False
        self.USER = None
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.resizable(False, False)
        self.title(u'材料管理系统')
        install_database()
        self.initComponents()

    def initComponents(self):
        self.createMainPanel()
        self.createLoginPanel()
        self.createMaterialPanel()
        self.createInMaterialPanel()
        self.createOutMaterialPanel()
        self.createQueryPanel()
        self.createLogoutPanel()

        self.main.add(self.loginPanel, text="登录")
        self.main.pack(fill=tk.BOTH, expand=tk.YES)

    def createMainPanel(self):
        "创建主要的控制面板容器"
        self.main = ttk.Notebook(self, width=self.WIDTH, height=self.HEIGHT)

    def createLoginPanel(self):
        "创建登录控制面板"
        self.loginPanel = ttk.Frame(self.main)
        self.loginMsgVar = tk.StringVar()
        self.paintLoginPanel()

    def createMaterialPanel(self):
        "创建材料管理面板"
        self.materialPanel = MaterialPanel(self)

    def createInMaterialPanel(self):
        "创建入库控制面板"
        self.inMaterialPanel = InMaterialPanel(self.main)

    def createOutMaterialPanel(self):
        "创建出库控制面板"
        self.outMaterialPanel = OutMaterialPanel(self.main)

    def createQueryPanel(self):
        "创建查询控制面板"
        self.queryPanel = ttk.Frame(self.main)

    def createLogoutPanel(self):
        "创建注销控制面板"
        self.logoutPanel = ttk.Frame(self.main)
        self.paintLogoutPanel()

    def paintLoginPanel(self):
        '绘制登录控制面板'

        self.loginMsg = tk.Label(self.loginPanel, textvariable=self.loginMsgVar,
                                 foreground="red", font=('times', 12, 'bold'))
        ttk.Label(self.loginPanel, text=u"用户名").grid(
            column=0, row=1)
        tk.Entry(self.loginPanel, textvariable=self.username).grid(
            column=1, row=1)

        ttk.Label(self.loginPanel, text=u"密码").grid(
            column=0, row=2)
        tk.Entry(self.loginPanel, textvariable=self.password,
                 show="*").grid(column=1, row=2)

        self.username.set('test')
        self.password.set('test')

        ttk.Button(
            self.loginPanel, text=u"登录", command=self.login).grid(row=3)

    def paintLogoutPanel(self):
        "绘制注销控制面板"
        ttk.Button(self.logoutPanel, text=u"注销", command=self.logout).pack(
            anchor=tk.CENTER)

    def login(self):
        "登录相关操作实现"

        self.USER = USER_UTIL.getObjectByNameAndPassword(
            self.username.get(), self.password.get())

        self.LOGGED_IN = self.USER is not None

        if self.LOGGED_IN:
            self.loginMsgVar.set('')  # 重置登录消息标签
            self.main.forget(self.loginPanel)
            self.main.add(self.materialPanel, text=u"材料管理")
            self.main.add(self.inMaterialPanel, text=u"入库")
            self.main.add(self.outMaterialPanel, text=u"出库")
            self.main.add(self.queryPanel, text=u"查询")
            self.main.add(self.logoutPanel, text=u"注销")
        else:
            self.loginMsg.grid(row=0, columnspan=2)
            self.loginMsgVar.set(text=u"用户名或密码错误！")

    def logout(self):

        if tkMessageBox.askyesno("注销？", u"你确定要退出当前登录用户吗？"):
            self.LOGGED_IN = False
            self.main.add(self.loginPanel, text=u"登录")
            self.main.forget(self.materialPanel)
            self.main.forget(self.inMaterialPanel)
            self.main.forget(self.outMaterialPanel)
            self.main.forget(self.queryPanel)
            self.main.forget(self.logoutPanel)


def main():
    app = Application()
    app.title(u"材料管理")
    app.mainloop()

if __name__ == '__main__':
    main()
