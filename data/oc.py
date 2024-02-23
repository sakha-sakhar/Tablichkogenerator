import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Oc(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'oc'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # путь к картинке
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hidden = sqlalchemy.Column(sqlalchemy.Boolean)
    relevant = sqlalchemy.Column(sqlalchemy.Boolean)
    rows = orm.relation('Row',
                        secondary='oc_row_association',
                        backref='oc')
    

