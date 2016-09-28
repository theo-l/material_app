# encoding: utf-8

'''
材料管理系统中实体对应的数据库表模型
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, Date, Boolean, ForeignKey, event
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()


class Department(Base):
    "单位机构表"

    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)

    users = relationship(
        "User", order_by="User.id", back_populates="department", cascade="all, delete, delete-orphan")


class User(Base):
    "所有用户表，包括管理员和领料人"
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=True)

    "多个用户在一个单位中"
    department = relationship('Department', back_populates="users")

    def is_admin_user(self):
        return self.is_admin or self.password

    @staticmethod
    def new_(username):
        return User(name=username)


class Material(Base):
    "材料库存表"
    __tablename__ = "material"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type_no = Column(String)
    count = Column(Integer, default=0)
    unit = Column(String, default=0)
    price = Column(Float, default=0.0)
    note = Column(String, nullable=True, default='')
    creation = Column(Date, default=date.today())
    last_update = Column(Date, default=date.today())

    def get_ui_list(self):
        return [self.name, self.type_no, self.unit, self.count, self.price, self.creation, self.last_update, self.note]

    @staticmethod
    def new_(name, type_no, count=0):
        return Material(name=name, type_no=type_no, count=count)


@event.listens_for(Material, 'before_update')
def materialPostUpdate(mapper, connect, target):
    "在更新Material对象之后，将其最后更新时间更新为当前日期"
    print u'更新材料的更新时间'
    target.last_update = date.today()


class OutMaterial(Base):
    "出库材料表"
    __tablename__ = "out_material"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    material_id = Column(Integer)
    count = Column(Integer)
    out_time = Column(Date, default=date.today())
    usage = Column(String, nullable=True, default='')
    project = Column(String, nullable=True, default='')

    def get_ui_list(self):
        "出库人，材料名，型号， 数量，用途，出库时间"
        return [self.user_id, self.material_id, None, self.count, self.usage, self.out_time]


class InMaterial(Base):
    "入库材料表"
    __tablename__ = "in_material"

    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    in_time = Column(Date, default=date.today())
    user_id = Column(Integer)
    material_id = Column(Integer)

    def get_ui_list(self):
        "用户名，材料名，型号，数量，入库时间"
        return [self.user_id, self.material_id, None, self.count, self.in_time]
