import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


# объекты класса пользователь
class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    snils = sqlalchemy.Column(sqlalchemy.Integer,  nullable=True)
    podal = sqlalchemy.Column(sqlalchemy.String, default="")
    vybor = sqlalchemy.Column(sqlalchemy.String, default="") #аттестат
    sogl = sqlalchemy.Column(sqlalchemy.String, default="") #согласие
    forma = sqlalchemy.Column(sqlalchemy.String, default="")
    ball = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    def __repr__(self):
        return f'{self.snils} {self.ball} {self.podal}'

