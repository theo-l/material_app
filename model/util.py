# encoding: utf-8

from model.models import Base, User, Department, Material, OutMaterial, InMaterial
from model import config


def install_database():
    "安装数据库"
    Base.metadata.create_all(config.ENGINE)


class ModelUtil(object):
    "数据库基本操作工具"
    session = config.SESSION

    def __init__(self):
        pass

    def is_object_exists(self, obj):
        return False

    def add(self, obj):
        if not self.is_object_exists(obj):
            self.session.add(obj)
            self.commit()

    def add_all(self, *objs):
        self.session.add_all(*objs)
        self.flush()

    def delete(self, obj):
        self.session.delete(obj)
        self.flush()

    def get_new(self):
        return self.session.new

    def get_dirty(self):
        return self.session.dirty

    def query(self, *args, **kwargs):
        return self.session.query(*args, **kwargs)

    def flush(self):
        return self.session.flush()

    def commit(self):
        return self.session.commit()

    def rollback(self):
        return self.session.rollback()


class DepartmentUtil(ModelUtil):
    "单位数据库操作工具"

    def get_object_by_name(self, name):
        return self.query(Department).filter_by(name=name).first()

    def delete_by_name(self, name):
        obj = self.get_object_by_name(name)
        if obj is not None:
            self.delete(obj)

    def is_object_exists(self, obj):
        return self.get_object_by_name(obj.name) is None

    def get_all_objects(self):
        return self.query(Department).all()

    def get_count(self):
        return self.query(Department).count()

    def clean(self):
        "清理所有的单位对象"
        
        departments = self.get_all_objects()
        for dep in departments:
            self.delete(dep)


class UserUtil(ModelUtil):
    "用户数据库操作工具"

    def login(self, username, password):
        if self.get_object_by_name_and_password(username, password) is None:
            return False
        return True

    def is_admin(self, obj):
        "判断用户是否是管理员"
        return obj.is_admin_user()

    def get_all_objects(self):
        return self.query(User).all()

    def get_count(self):
        return self.query(User).count()

    def get_object_by_name(self, name):
        return self.query(User).filter_by(name=name).first()

    def get_object_by_id(self, user_id):
        return self.query(User).filter_by(id=user_id).first()

    def delete_by_name(self, name):
        obj = self.get_object_by_name(name)
        if obj is not None:
            self.delete(obj)

    def is_object_exists(self, obj):
        return self.get_object_by_name(obj.name) is not None

    def get_object_by_name_and_password(self, name, password):
        return self.query(User).filter_by(name=name).filter_by(password=password).first()

    def clean(self):
        "清除所有的用户对象,谨慎使用"
        for user in self.get_all_objects():
            self.delete(user)


class MaterialUtil(ModelUtil):
    "材料数据库操作工具"

    def get_type_no_by_name(self, name):
        "根据材料名称来获取其对应的相关型号来提供自动补充"
        return [i[0] for i in self.query(Material.type_no).filter_by(name=name).all()]

    def get_all_objects(self):
        return self.query(Material).order_by(Material.name.asc(), Material.type_no.asc()).order_by(Material.id.asc()).all()

    def get_count(self):
        return self.query(Material).count()

    def get_count_by_name(self, name):
        return self.query(Material).filter_by(name=name).count()

    def get_count_by_name_and_type(self, name, type_no):
        return self.query(Material).filter_by(name=name, type_no=type_no).count()

    def clean(self):
        for material in self.get_all_objects():
            self.delete(material)

    def get_object_by_name(self, name):
        return self.query(Material).filter_by(name=name).all()

    def get_list_by_name(self, material_name):
        'return a list of material which have the same name'
        return self.query(Material).filter_by(name=material_name).all()

    def get_object_by_name_and_type(self, name, typeNo):
        return self.query(Material).filter_by(name=name, type_no=typeNo).first()

    def get_object_by_id(self, material_id):
        return self.query(Material).filter_by(id=material_id).first()

    def is_object_exists(self, obj):
        "判断材料是否已经在数据库中存在"
        return self.get_object_by_name_and_type(obj.name, obj.type_no) is not None


class OutMaterialUtil(ModelUtil):
    "材料出库数据库表操作工具"

    def get_out_list_by_user(self, user):
        "根据用户来获取用户的材料出库列表"
        return self.query(OutMaterial).filter_by(user_id=user.id).all()

    def get_out_list_count_by_user(self, user):
        return self.query(OutMaterial).filter_by(user_id=user.id).count()

    def get_out_list_by_material(self, material):
        "根据材料来获取材料的出库列表"
        return self.query(OutMaterial).filter_by(material_id=material.id).all()

    def get_out_list_count_by_material(self, material):
        return self.query(OutMaterial).filter_by(material_id=material.id).count()

    def get_out_count_by_material_name(self, material_name):
        materials = self.query(Material).filter_by(name=material_name).all()
        count = 0
        for material in materials:
            count += self.get_out_list_count_by_material(material)
        return count

    def get_out_list_by_material_name(self, material_name):
        materials = self.query(Material).filter_by(name=material_name).all()
        objects = []
        for material in materials:
            objects.extend(self.get_out_list_count_by_material(material))
        return objects

    def update_out_material(self, user_id, material_id, material_count, material_usage):
        obj = OutMaterial(
            user_id=user_id, material_id=material_id, count=material_count, usage=material_usage)
        self.add(obj)

    def is_object_exists(self, obj):
        return ModelUtil.is_object_exists(self, obj)

    def get_count(self):
        return self.query(OutMaterial).count()

    def get_all_objects(self):
        '''
        出库数据记录按照其出库时间逆序排列
        '''
        return self.query(OutMaterial).order_by(OutMaterial.id.desc()).all()


class InMaterialUtil(ModelUtil):
    "材料入库数据库表操作工具"

    def get_in_list_by_user(self, user):
        "根据用户来获取用户的材料入库列表"
        return self.query(InMaterial).filter_by(user_id=user.id).all()

    def get_in_list_count_by_user(self, user):
        return self.query(InMaterial).filter_by(user_id=user.id).count()

    def get_in_list_by_material(self, material):
        "根据材料来获取材料的入库列表"
        return self.query(InMaterial).filter_by(material_id=material.id).all()

    def get_in_list_count_by_material(self, material):
        return self.query(InMaterial).filter_by(material_id=material.id).count()

    def get_in_count_by_material_name(self, material_name):
        'query in material count only by material name'
        materials = self.query(Material).filter_by(name=material_name)
        count = 0
        for material in materials:
            count += self.get_in_list_count_by_material(material)
        return count

    def get_in_list_by_material_name(self, material_name):
        'query in material object list only by material name'
        materials = self.query(Material).filter_by(name=material_name)
        objects = []
        for material in materials:
            objects.extend(self.get_in_list_by_material(material))
        return objects

    def update_in_material(self, user_id, material_id, material_count):
        obj = InMaterial(
            user_id=user_id, material_id=material_id, count=material_count)
        self.add(obj)

    def get_count(self):
        "获取数据记录个数"
        return self.query(InMaterial).count()

    def get_all_objects(self):
        "获取所有的数据，按照入库时间逆序排列"
        return self.query(InMaterial).order_by(InMaterial.id.desc()).all()

    def is_object_exists(self, obj):
        return ModelUtil.is_object_exists(self, obj)
