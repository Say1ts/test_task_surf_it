from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.testing.schema import Table

Base = declarative_base()


class Ad(Base):
    __tablename__ = 'ad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer, ForeignKey('ad_type.id'))
    title = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    content = Column(Text)
    created_at = Column(DateTime)
    is_published = Column(Boolean)
    owner = Column(Integer, ForeignKey('user.id'))
    price = Column(Numeric)

    ad_type = relationship('AdType', back_populates='ads')
    category = relationship('Category', back_populates='ads')


class AdType(Base):
    __tablename__ = 'ad_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    ads = relationship('Ad', back_populates='ad_types')


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)

    ads = relationship('Ad', back_populates='categories')


class Complain(Base):
    __tablename__ = 'complain'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(Integer, ForeignKey('ad.id'))
    title = Column(String)
    description = Column(Text)
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('user.id'))


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(Integer, ForeignKey('ad.id'))
    score = Column(Integer)
    content = Column(Text)
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('user.id'))

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    salt = Column(String)
    role_id = Column(Integer, ForeignKey('role.id'))
    is_banned = Column(Boolean)

    role = relationship('Role', back_populates='users')


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String)
    description = Column(Text)

    users = relationship('User', back_populates='role')
    permissions = relationship('Permission', secondary='user_role_permission', back_populates='roles')


class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(Text)

    roles = relationship('Role', secondary='user_role_permission', back_populates='permissions')


user_role_permission = Table('user_role_permission', Base.metadata,
                            Column('role_id', ForeignKey('role.id'), primary_key=True),
                            Column('permission_id', ForeignKey('permission.id'), primary_key=True)
                            )
