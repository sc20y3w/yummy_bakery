# It was written because without it, the application would jump again and again
# between form and models.py and app.py.
from exts import db
from datetime import datetime


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class Baker(db.Model):
    __tablename__ = "baker"
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), primary_key=True,  nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    baker_name = db.Column(db.String(100), db.ForeignKey("baker.username"))
    bread_name = db.Column(db.String(100), db.ForeignKey("bread.bread_name"))
    client_id = db.Column(db.String(100), db.ForeignKey("client.client_name"))
    finish = db.Column(db.String(100), nullable=False)
    baker = db.relationship("Baker", backref="baker_order")
    bread = db.relationship("Bread", backref="bread_order")
    client = db.relationship("Client", backref="client_order")
    join_time = db.Column(db.DateTime, default=datetime.now)


class Client(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, autoincrement=True)
    client_name = db.Column(db.String(100), primary_key=True, nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)


class Type(db.Model):
    __tablename__ = "type"
    type_name = db.Column(db.String(100), primary_key=True, nullable=False)


# Define ORM model(total assessments)
class Bread(db.Model):
    __tablename__ = "bread"
    bread_name = db.Column(db.String(100), primary_key=True, nullable=False)
    m_date = db.Column(db.Date, nullable=False)
    e_date = db.Column(db.Date, nullable=False)
    # foreign key
    type_name = db.Column(db.String(100), db.ForeignKey("type.type_name"))
    type = db.relationship("Type", backref="bread_type")
