'''
@author: trise
@studioe: JCAI
@software: pycharm
@time: 2020/8/11 14:45
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#链接数据库格式
db_url = 'mysql+pymysql://root:123456@localhost:3306/mydb'
#创建引擎
engine = create_engine(db_url)
#模型与数据库表进行关联的基类，模型必须继承于Base
Base = declarative_base(bind=engine)
#创建session会话
DbSession = sessionmaker(bind = engine)
session = DbSession()