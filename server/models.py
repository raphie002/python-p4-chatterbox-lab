# server/models.py
from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin # type: ignore

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    username = db.Column(db.String)
    
    # Using server_default ensures the DB handles the timestamp
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # This prevents recursion errors and keeps the JSON clean
    serialize_rules = ('-updated_at',)