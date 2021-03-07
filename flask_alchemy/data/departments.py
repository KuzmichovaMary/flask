import datetime
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_alchemy.data.db_session import SqlAlchemyBase

from sqlalchemy import orm


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey("users.id"))
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True, unique=True)

    user = orm.relation("User")  # in User departments = orm.relation("Department", back_populates='user')
