from datetime import datetime
from enum import Enum
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from base64 import b64encode


db = SQLAlchemy()


class UserRol(Enum):
	ADMINISTRATOR='administrator',
	GENERAL ='general'


class UserStatus(Enum):
	ACTIVE = "active",
	DISABLED = "disabled",
	DELETE = "delete"


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(80), unique=True, nullable=False)
  fullname = db.Column(db.String(80), nullable=False)
  password = db.Column(db.String(250), nullable=False, default="")
  salt = db.Column(db.String(120), nullable=False)
  created_at = db.Column(db.DateTime(timezone=False), nullable=False)
  rol = db.Column(db.Enum(UserRol), nullable=False, default="GENERAL")
  status = db.Column(db.Enum(UserStatus), nullable=False, default="ACTIVE")
  unore = db.relationship('Unore', backref='user', uselist=True)
  news = db.relationship('News', backref='user', uselist=True)


  def __init__(self, email, fullname, password, rol):
    self.email = email,
    self.fullname = fullname,
    self.password = password
    self.rol = rol
    self.salt = b64encode(os.urandom(32)).decode("utf-8")


  def serialize(self):
    return {
      'id':self.id,
      'fullname':self.fullname,
      'email':self.email,
      'created_at': self.created_at,
      'salt':self.salt,
			'password':self.password,
      'status':self.status.value,
			'rol':self.rol.value
    }


  def set_password(self, password):
    self.password = generate_password_hash(f'{password}{self.salt}')


  def check_password(self, password):
    return check_password_hash(self.password, f'{password}{self.salt}')
  

  def get_user(id):
    try:
      user = User.query.get(id)
      if user is not None:
        return user
      else:
        return None
    except Exception as error:
      return {
        "message": "Error query failed, please try again",
      }


  def get_all_users():
    try:
      users = User.query.all()
      return users
    except Exception as error:
      return {
        "message": "Error query failed, please try again",
      }


  @classmethod
  def create(cls, data):
    try:
      data = cls(**data)
      print(data)
      data.set_password(data.password)
      data.created_at = datetime.now()
      db.session.add(data)
      db.session.commit()
      return data
    except Exception as error:
      db.session.rollback()
      print(error.args)
      return None
  

  @classmethod
  def login(cls, email, password):
    try:
      user = cls.query.filter_by(email=email).first()
      if user is not None:
        if user.check_password(password):
          return user
        else:
          return None
      else:
        return None
    except Exception as error:
      return None
    

class Unore(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  update_at = db.Column(db.DateTime(timezone=False), nullable=False)	
  amount = db.Column(db.Float, nullable=False, default=0)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


  @classmethod
  def create(cls, data):
    try:
      data = cls(**data)
      data.update_at = datetime.now()
      data.user_id = user_id
      db.session.add(data)
      db.session.commit()
      return data
    except Exception as error:
      db.session.rollback()
      print(error.args)
      return None


  def get_unore():
    try:
      unore = Unore.query.all()
      if unore is not None:
        return unore
      else:
        return None
    except Exception as error:
      return {
        "message": "Error query failed, please try again",
      }

  @classmethod
  def create(cls, data):
    try:
      data = cls(**data)
      data.update_at = datetime.now()
      db.session.add(data)
      db.session.commit()
      return data
    except Exception as error:
      db.session.rollback()
      print(error.args)
      return None


  def serialize(self):
    return {
      'id':self.id,
      'update_at':self.update_at,
      'amount':self.amount,
      'user_id':self.user_id
    }


class News(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(250), nullable=False)
  subtitle = db.Column(db.Text, nullable=False)
  summary = db.Column(db.Text, nullable=False)
  highlighted =db.Column(db.Text, nullable=False)
  complete = db.Column(db.Text, nullable=False)
  image = db.Column(db.String(200), nullable=False)
  image_secondary = db.Column(db.String(200), nullable=True)
  image_preview = db.Column(db.String(200), nullable=False)
  public_id_image = db.Column(db.String(100), nullable=False)
  public_id_secondary = db.Column(db.String(100), nullable=False)
  public_id_preview = db.Column(db.String(100), nullable=False)
  created_at = db.Column(db.DateTime(timezone=False), nullable=False)	
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


  def get_news():
    try:
      news = News.query.all()
      if news is not None:
        return news
      else:
        return None
    except Exception as error:
      return {
        "message": "Error query failed, please try again",
      }


  @classmethod
  def create(cls, data):
    try:
      data = cls(**data)
      data.created_at = datetime.now()
      db.session.add(data)
      db.session.commit()
      return data
    except Exception as error:
      db.session.rollback()
      print(error.args)
      return None

  def serialize(self):
    return {
      'id':self.id,
      'title':self.title,
      'subtitle':self.subtitle,
      'summary':self.summary,
      'complete':self.complete,
      'image':self.image,
      'image_secondary':self.image_secondary,
      'image_preview':self.image_preview,   
      'highlighted':self.highlighted,
    }

  
