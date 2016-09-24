# encoding: utf-8
'''
数据库触发器相关事件处理器定义
'''
from sqlalchemy import event
from model.models import Material
from datetime import date


@event.listens_for(Material, 'before_update')
def materialPostUpdate(mapper, connect, target):
    "在更新Material对象之后，将其最后更新时间更新为当前日期"
    target.last_update = date.today()
