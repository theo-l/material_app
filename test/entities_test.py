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
            DEPARTMENT_UTIL.get_object_by_name("Admin"), "object add failed")

        self.assertIsNotNone(
            DEPARTMENT_UTIL.get_object_by_name("HR"), "object add failed")

        self.assertIsNotNone(
            DEPARTMENT_UTIL.get_object_by_name("Fina"), "object add failed")

        self.assertIsNotNone(
            DEPARTMENT_UTIL.get_object_by_name("IT"), "object add failed")

        self.assertEqual(
            DEPARTMENT_UTIL.get_count(), 4, "object delete failed")

    def test_query_department(self):

        self.assertEqual(DEPARTMENT_UTIL.get_object_by_name(
            "Admin").name, "Admin", "object query failed")

        self.assertEqual(DEPARTMENT_UTIL.get_object_by_name(
            "HR").name, "HR", "object query failed")

        self.assertEqual(DEPARTMENT_UTIL.get_object_by_name(
            "Fina").name, "Fina", "object query failed")

        self.assertEqual(DEPARTMENT_UTIL.get_object_by_name(
            "IT").name, "IT", "object query failed")

    def test_delete_department(self):

        DEPARTMENT_UTIL.delete_by_name("Admin")
        self.assertIsNone(
            DEPARTMENT_UTIL.get_object_by_name("Admin"), "object delete failed")

        DEPARTMENT_UTIL.delete_by_name("HR")
        self.assertIsNone(
            DEPARTMENT_UTIL.get_object_by_name("HR"), "object delete failed")

        DEPARTMENT_UTIL.delete_by_name("Fina")
        self.assertIsNone(
            DEPARTMENT_UTIL.get_object_by_name("Fina"), "object delete failed")

        DEPARTMENT_UTIL.delete_by_name("IT")
        self.assertIsNone(
            DEPARTMENT_UTIL.get_object_by_name("IT"), "object delete failed")

        self.assertEqual(
            DEPARTMENT_UTIL.get_count(), 0, "object delete failed")


class UserTest(unittest.TestCase):

    def setUp(self):
        init_users()

    def tearDown(self):
        clean_users()

    def test_add_user(self):
        self.assertIsNotNone(
            USER_UTIL.get_object_by_name("admin"), "user add failed")
        self.assertIsNotNone(
            USER_UTIL.get_object_by_name("normal"), "user add failed")
        self.assertIsNotNone(
            USER_UTIL.get_object_by_name("simple"), "user add failed")
        self.assertEqual(USER_UTIL.get_count(), 3, "user add failed")

    def test_delete_user(self):
        USER_UTIL.delete_by_name("admin")
        self.assertIsNone(
            USER_UTIL.get_object_by_name("admin"), "user delete failed")

        USER_UTIL.delete_by_name("normal")
        self.assertIsNone(
            USER_UTIL.get_object_by_name("normal"), "user delete failed")

        USER_UTIL.delete_by_name("simple")
        self.assertIsNone(
            USER_UTIL.get_object_by_name("simple"), "user delete failed")

        self.assertEqual(USER_UTIL.get_count(), 0, "user delete failed")

    def test_query_user(self):
        self.assertEqual(
            USER_UTIL.get_object_by_name("admin").name, "admin", "user query failed")

        self.assertEqual(
            USER_UTIL.get_object_by_name("normal").name, "normal", "user query failed")

        self.assertEqual(
            USER_UTIL.get_object_by_name("simple").name, "simple", "user query failed")

    def test_user_position(self):
        self.assertTrue(USER_UTIL.get_object_by_name(
            "admin").is_admin_user(), "user position failed")

        self.assertTrue(USER_UTIL.get_object_by_name(
            "normal").is_admin_user(), "user position failed")

        self.assertTrue(not USER_UTIL.get_object_by_name(
            "simple").is_admin_user(), "user position failed")

    def test_login_user(self):
        self.assertIsNotNone(
            USER_UTIL.get_object_by_name_and_password("admin", "admin"), "login failed")

        self.assertIsNotNone(
            USER_UTIL.get_object_by_name_and_password("normal", "normal"), "login failed")

        self.assertIsNone(
            USER_UTIL.get_object_by_name_and_password("simple", ""), "login failed")

    def test_update_user(self):
        admin = USER_UTIL.get_object_by_name("admin")
        self.assertEqual(admin.password, "admin", "user query failed")
        admin.password = "updated"
        USER_UTIL.add(admin)

        self.assertEqual(USER_UTIL.get_object_by_name(
            "admin").password, "updated", "user update failed")


class MateriaTest(unittest.TestCase):

    def setUp(self):
        init_materials()

    def tearDown(self):
        clean_materials()

    def test_add_material(self):
        self.assertIsNotNone(
            MATERIAL_UTIL.get_object_by_name_and_type(u"光缆", u"6芯"), "material add failed")

        self.assertIsNotNone(
            MATERIAL_UTIL.get_object_by_name_and_type(u"光缆", u"7芯"), "material add failed")

        self.assertIsNotNone(
            MATERIAL_UTIL.get_object_by_name_and_type(u"光缆", u"8芯"), "material add failed")

        self.assertEqual(MATERIAL_UTIL.get_count(), 3, "material add failed")

    def test_query_type_no(self):
        self.assertEqual(
            MATERIAL_UTIL.get_type_no_by_name(u'光缆'), [u'6芯', u'7芯', u'8芯'],  "type no query failed")

    def test_query_material(self):
        self.assertEqual(MATERIAL_UTIL.get_object_by_name_and_type(
            "光缆".decode('utf-8'), "6芯".decode("utf-8")).count, 100, "material query failed")


class OutMaterialTest(unittest.TestCase):
    "测试出库相关操作"
    pass


class InMaterialTeset(unittest.TestCase):
    "测试入库相关操作"
    pass

if __name__ == '__main__':
    unittest.main()
