from sqlalchemy import Column, ForeignKey, Integer, Float, String, Text, LargeBinary, DateTime

from db.database import engine, Base
from db.test_db import engine as test_engine, Base as test_base

from datetime import datetime


class Users(Base):

    __tablename__ = 'users'
    __tableargs__ = {
        'comment': 'Пользователи'
    }

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, comment='ID PK')
    email = Column(String(30), nullable=False, unique=True, comment='электронный почтовый адрес пользователя')
    phone = Column(Integer, nullable=False, unique=True, comment='телефонный номер пользователя')
    fam = Column(String(20), nullable=False, comment='фамилия пользователя')
    name = Column(String(20), nullable=False, comment='имя пользователя')
    otc = Column(String(20), comment='отчество пользователя')

    def __repr__(self):
        return f'{self.id} {self.email} {self.phone} {self.fam} {self.name} {self.otc}'


class PerevalAdded(Base):

    __tablename__ = 'pereval_added'
    __tableargs__ = {
        'comment': 'Данные перевалов'
    }

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, comment='ID PK')
    created_by = Column(Integer, ForeignKey('users.id'), comment='Пользователь, создавший запись')
    coord_id = Column(Integer, nullable=False, unique=True, comment='Ссылка на таблицу с координатами')
    levels_id = Column(Integer, nullable=False, unique=True, comment='Ссылка на таблицу с уровнями')
    beauty_title = Column(String(30), nullable=False, comment='Дополнение к наименованию')
    title = Column(String(30), nullable=False, comment='Наименование объекта')
    other_titles = Column(Text, comment='Прочие наименования объекта')
    connect = Column(Text, comment='Что соединяет')
    add_dt = Column(DateTime, default=datetime.now, comment='Дата и время добавления')
    status = Column(String(10), nullable=False, default='new', comment='Статус рассмотрения')

    def __repr__(self):
        return f'{self.id} {self.created_by} {self.coord_id} {self.levels_id} ' \
               f'{self.beauty_title} {self.title} {self.other_titles} ' \
               f'{self.connect} {self.add_dt} {self.status}'


class Coords(Base):

    __tablename__ = 'coords'
    __tableargs__ = {
        'comment': 'Координаты перевала'
    }

    id = Column(Integer, ForeignKey('pereval_added.coord_id'), primary_key=True, autoincrement=True, comment='ID PK')
    latitude = Column(Float, nullable=False, comment='Географическая широта объекта')
    longitude = Column(Float, nullable=False, comment='Географическая долгота объекта')
    height = Column(Integer, nullable=False, comment='Высота над уровнем моря')

    def __repr__(self):
        return f'{self.id} {self.latitude} {self.longitude} {self.height}'


class Levels(Base):

    __tablename__ = 'levels'
    __tableargs__ = {
        'comment': 'Уровни сложности по сезонам'
    }

    id = Column(Integer, ForeignKey('pereval_added.levels_id'), primary_key=True, autoincrement=True, comment='ID PK')
    winter = Column(String(2), comment='зимний уровень')
    summer = Column(String(2), comment='летний уровень')
    autumn = Column(String(2), comment='осенний уровень')
    spring = Column(String(2), comment='весенний уровень')

    def __repr__(self):
        return f'{self.id} {self.winter} {self.summer} {self.autumn} {self.spring}'


class Images(Base):

    __tablename__ = 'images'
    __tableargs__ = {
        'comment': 'Изображения'
    }

    id = Column(Integer, ForeignKey('pereval_image.image_id'), primary_key=True, autoincrement=True, comment='ID PK')
    add_dt = Column(DateTime, default=datetime.now, comment='Дата и время добавления')
    title = Column(String(30), nullable=False, comment='Наименование изображения')
    image = Column(LargeBinary, nullable=False, comment='Изображение')

    def __repr__(self):
        return f'{self.id} {self.add_dt} {self.title}'


class PerevalImage(Base):

    __tablename__ = 'pereval_image'
    __tableargs__ = {
        'comment': 'Соответствие перевала и изображения'
    }

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, comment='ID PK')
    pereval_id = Column(Integer, ForeignKey('pereval_added.id'), comment='Ссылка на перевал')
    image_id = Column(Integer, nullable=False, unique=True, comment='Ссылка на изображение')

    def __repr__(self):
        return f'{self.id} {self.pereval_id} {self.image_id}'


class PerevalAreas(Base):

    __tablename__ = 'pereval_areas'
    __tableargs__ = {
        'comment': 'Справочник зон'
    }

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, comment='ID PK')
    parent_id = Column(Integer, nullable=False, comment='В какую зону включается')
    title = Column(String(60), nullable=False, unique=True, comment='Наименование зоны')

    def __repr__(self):
        return f'{self.id} {self.parent_id} {self.title}'


class SprActivitiesTypes(Base):

    __tablename__ = 'spr_activities_types'
    __tableargs__ = {
        'comment': 'Справочник активностей'
    }

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, comment='ID PK')
    title = Column(String(30), nullable=False, unique=True, comment='Название активности')

    def __repr__(self):
        return f'{self.id} {self.title}'


if __name__ == '__main__':

    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    test_base.metadata.create_all(test_engine)
