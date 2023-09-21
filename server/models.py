from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    id = db.Column(db.Integer, primary_key=True)
     # Establish a one-to-many relationship with BakedGood
    name = db.Column(db.String(255))
    baked_goods = relationship('BakedGood', back_populates='bakery')



class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    id = db.Column(db.Integer, primary_key=True)
    # Define a foreign key relationship with Bakery
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))
    name = db.Column(db.String(255)) 
    price = db.Column(db.Float)
     # Establish a many-to-one relationship with Bakery
    bakery = relationship('Bakery', back_populates='baked_goods')