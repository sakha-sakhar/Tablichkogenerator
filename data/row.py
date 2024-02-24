import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Row(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'row'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    # title = sqlalchemy.Column(sqlalchemy.String, nullable=True) (а нам оно надо?)
    mem = sqlalchemy.Column(sqlalchemy.Integer,
                            sqlalchemy.ForeignKey("mem.id"))
    oc_table = sqlalchemy.Table(
        'oc_row_association',
        SqlAlchemyBase.metadata,
        sqlalchemy.Column('oc', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('oc.id')),
        sqlalchemy.Column('row', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('row.id')))
