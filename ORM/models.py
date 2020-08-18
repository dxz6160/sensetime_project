'''
@author: trise
@studioe: JCAI
@software: pycharm
@time: 2020/8/11 14:41
'''
from sqlalchemy import Column, Integer, String
from ORM.conn import Base

#添加
def create_db():
    Base.metadata.create_all()
#删除
def drop_db():
    Base.metadata.drop_all()

class Students(Base):
    #主键自增的int类型的id主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    #定义不能为空的唯一的姓名字段
    s_name = Column(String(10), unique=True, nullable=False)
    s_age = Column(Integer, default=18)

    __tablename__ = 'students'

    # def __repr__(self):