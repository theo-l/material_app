# encoding: utf-8
'''
测试用例使用的相关工具
'''

from model.model_util import DepartmentUtil, UserUtil, MaterialUtil, OutMaterialUtil, InMaterialUtil
from model.entities import Department, User, Material


__all__ = ['USER_UTIL', 'DEPARTMENT_UTIL', 'MATERIAL_UTIL', 'IN_UTIL', 'OUT_UTIL',
           'init_departments', 'init_users', 'clean_departments', 'clean_users', 'add_department_users',
           'init_materials', 'clean_materials']

USER_UTIL = UserUtil()
DEPARTMENT_UTIL = DepartmentUtil()
MATERIAL_UTIL = MaterialUtil()
IN_UTIL = InMaterialUtil()
OUT_UTIL = OutMaterialUtil()


def init_departments():
    "填充测试单位数据"
    dep1 = Department(name="Admin")
    dep2 = Department(name="HR")
    dep3 = Department(name="Fina")
    dep4 = Department(name="IT")

    DEPARTMENT_UTIL.add_all([dep1, dep2, dep3, dep4])


def clean_departments():
    "清除所有的单位数据"
    DEPARTMENT_UTIL.clean()


def init_users():
    "填充测试用户数据"
    admin = User(name="admin", password="admin", isAdmin=True)
    normal = User(name="normal", password="normal")
    simple = User(name="simple")

    USER_UTIL.add_all([admin, normal, simple])


def clean_users():
    "清除所有的用户"
    USER_UTIL.clean()


def add_department_users(department, *users):
    "将多个用户添加到一个单位中"
    for user in users:
        user.department = department
        USER_UTIL.add(user)


def init_materials():
    "填充测试材料数据"
    mat1 = Material(
        name=u"光缆", count=100, unit=u"匝", type_no=u"6芯", price=216.95)
    mat2 = Material(
        name=u"光缆", count=100, unit=u"匝", type_no=u"7芯", price=256.95)
    mat3 = Material(
        name=u"光缆", count=100, unit=u"匝", type_no=u"8芯", price=286.95)

    MATERIAL_UTIL.add_all([mat1, mat2, mat3])


def clean_materials():
    MATERIAL_UTIL.clean()
