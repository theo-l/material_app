# encoding: utf-8
'''
用户相关操作测试
'''
import unittest
from test.util import *


class DepartmentTest(unittest.TestCase):

    def setUp(self):
        init_departments()

    def tearDown(self):
        clean_departments()

    def test_add_department(self):

        self.assertIsNotNone(
            DEPARTMENT_UTIL.getObjectByName("Admin"), "object add failed")

        self.assertIsNotNone(
            DEPARTMENT_UTIL.getObjectByName("HR"), "object add failed")

        self.assertIsNotNone(
            DEPARTMENT_UTIL.getObjectByName("Fina"), "object add failed")

        self.assertIsNotNone(
            DEPARTMENT_UTIL.getObjectByName("IT"), "object add failed")

        self.assertEqual(
            DEPARTMENT_UTIL.getCount(), 4, "object delete failed")

    def test_query_department(self):

        self.assertEqual(DEPARTMENT_UTIL.getObjectByName(
            "Admin").name, "Admin", "object query failed")

        self.assertEqual(DEPARTMENT_UTIL.getObjectByName(
            "HR").name, "HR", "object query failed")

        self.assertEqual(DEPARTMENT_UTIL.getObjectByName(
            "Fina").name, "Fina", "object query failed")

        self.assertEqual(DEPARTMENT_UTIL.getObjectByName(
            "IT").name, "IT", "object query failed")

    def test_delete_department(self):

        DEPARTMENT_UTIL.deleteByName("Admin")
        self.assertIsNone(
            DEPARTMENT_UTIL.getObjectByName("Admin"), "object delete failed")

        DEPARTMENT_UTIL.deleteByName("HR")
        self.assertIsNone(
            DEPARTMENT_UTIL.getObjectByName("HR"), "object delete failed")

        DEPARTMENT_UTIL.deleteByName("Fina")
        self.assertIsNone(
            DEPARTMENT_UTIL.getObjectByName("Fina"), "object delete failed")

        DEPARTMENT_UTIL.deleteByName("IT")
        self.assertIsNone(
            DEPARTMENT_UTIL.getObjectByName("IT"), "object delete failed")

        self.assertEqual(
            DEPARTMENT_UTIL.getCount(), 0, "object delete failed")


class UserTest(unittest.TestCase):

    def setUp(self):
        init_users()

    def tearDown(self):
        clean_users()

    def test_add_user(self):
        self.assertIsNotNone(
            USER_UTIL.getObjectByName("admin"), "user add failed")
        self.assertIsNotNone(
            USER_UTIL.getObjectByName("normal"), "user add failed")
        self.assertIsNotNone(
            USER_UTIL.getObjectByName("simple"), "user add failed")
        self.assertEqual(USER_UTIL.getCount(), 3, "user add failed")

    def test_delete_user(self):
        USER_UTIL.deleteByName("admin")
        self.assertIsNone(
            USER_UTIL.getObjectByName("admin"), "user delete failed")

        USER_UTIL.deleteByName("normal")
        self.assertIsNone(
            USER_UTIL.getObjectByName("normal"), "user delete failed")

        USER_UTIL.deleteByName("simple")
        self.assertIsNone(
            USER_UTIL.getObjectByName("simple"), "user delete failed")

        self.assertEqual(USER_UTIL.getCount(), 0, "user delete failed")

    def test_query_user(self):
        self.assertEqual(
            USER_UTIL.getObjectByName("admin").name, "admin", "user query failed")

        self.assertEqual(
            USER_UTIL.getObjectByName("normal").name, "normal", "user query failed")

        self.assertEqual(
            USER_UTIL.getObjectByName("simple").name, "simple", "user query failed")

    def test_user_position(self):
        self.assertTrue(USER_UTIL.getObjectByName(
            "admin").is_admin_user(), "user position failed")

        self.assertTrue(USER_UTIL.getObjectByName(
            "normal").is_admin_user(), "user position failed")

        self.assertTrue(not USER_UTIL.getObjectByName(
            "simple").is_admin_user(), "user position failed")

    def test_login_user(self):
        self.assertIsNotNone(
            USER_UTIL.getObjectByNameAndPassword("admin", "admin"), "login failed")

        self.assertIsNotNone(
            USER_UTIL.getObjectByNameAndPassword("normal", "normal"), "login failed")

        self.assertIsNone(
            USER_UTIL.getObjectByNameAndPassword("simple", ""), "login failed")

    def test_update_user(self):
        admin = USER_UTIL.getObjectByName("admin")
        self.assertEqual(admin.password, "admin", "user query failed")
        admin.password = "updated"
        USER_UTIL.add(admin)

        self.assertEqual(USER_UTIL.getObjectByName(
            "admin").password, "updated", "user update failed")


class MateriaTest(unittest.TestCase):

    def setUp(self):
        init_materials()

    def tearDown(self):
        clean_materials()

    def test_add_material(self):
        self.assertIsNotNone(
            MATERIAL_UTIL.getObjectByNameAndType(u"光缆", u"6芯"), "material add failed")

        self.assertIsNotNone(
            MATERIAL_UTIL.getObjectByNameAndType(u"光缆", u"7芯"), "material add failed")

        self.assertIsNotNone(
            MATERIAL_UTIL.getObjectByNameAndType(u"光缆", u"8芯"), "material add failed")

        self.assertEqual(MATERIAL_UTIL.getCount(), 3, "material add failed")

    def test_query_type_no(self):
        self.assertEqual(
            MATERIAL_UTIL.getTypeNoByName(u'光缆'), [u'6芯', u'7芯', u'8芯'],  "type no query failed")

    def test_query_material(self):
        self.assertEqual(MATERIAL_UTIL.getObjectByNameAndType(
            "光缆".decode('utf-8'), "6芯".decode("utf-8")).count, 100, "material query failed")


class OutMaterialTest(unittest.TestCase):
    "测试出库相关操作"
    pass


class InMaterialTeset(unittest.TestCase):
    "测试入库相关操作"
    pass

if __name__ == '__main__':
    unittest.main()
