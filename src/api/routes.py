from crypt import methods
from flask import Flask, Blueprint, jsonify, request
from api.models import User, Unore, News, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import cloudinary.uploader as uploader
import smtplib

api = Blueprint('api', __name__)


@api.route("/verify", methods=["GET"])
@jwt_required()
def verify():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).one_or_none()
    if user:
        return jsonify({"verified": True}), 200
    return jsonify({"verified": False}), 401


@api.route('/user', methods=['GET'])
@api.route('/user/<int:id>', methods=['GET'])
def get_users(id=None):
  if request.method == 'GET':
    if id is not None:
      user = User.get_user(id)
      if type(user) == User:
        return user.serialize()
      if user is None:
        return jsonify({'message':"User not found"}), 404
      return jsonify(user), 500
    
    if id is None:
      users = User.get_all_users()
      if users:
        return jsonify(list(map(lambda user: user.serialize(), users))), 200
      else:
        return jsonify(users),500
  return jsonify({'message':'method not allowed'}),405


@api.route('/user', methods=['POST'])
def create_user():
  if request.method == 'POST':
    data = request.json
    if data is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('email') is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('fullname') is None:
      return jsonify({'message':'Bad request'}), 400

    user = User.create(data)
    if type(user) == User:
      return user.serialize(), 201
    if user is None:
      return jsonify({'message':'User already exists'}), 400
    return jsonify(user), 500
  return jsonify({'message':'method not allowed'}),405


@api.route('/login', methods=['POST'])
def login():
  if request.method == 'POST':
    data = request.json
    if data is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('email') is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('password') is None:
      return jsonify({'message':'Bad request'}), 400

    user = User.login(data["email"], data["password"])
    if type(user) == User:
      access_token = create_access_token(identity=user.id)
      return jsonify(access_token=access_token), 200
    if user is None:
      return jsonify({'message':'Bad credentials'}), 400
    return jsonify(user), 500
  return jsonify({'message':'method not allowed'}),405


@api.route('/unore', methods=['GET'])
def get_unore():
  unore = Unore.get_unore()
  if unore is not None:
    return jsonify(list(map(lambda item: item.serialize(), unore))), 200
  if unore is None: 
    return jsonify({'message':"Unore not found"}), 404
  return jsonify(unore), 500


@api.route('/unore', methods=['POST'])
@jwt_required()
def create_unore():
  if request.method == 'POST':
    data = request.json
    data.update({'user_id':get_jwt_identity()})
    if data is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('amount') is None:
      return jsonify({'message':'Bad request'}), 400
    
    unore = Unore.create(data)
    if type(unore) == Unore:
      return unore.serialize(), 201
    if unore is None:
      return jsonify({'message':'Error try again later'}), 500
    
    unore = Unore.create(data)
    if type(unore) == Unore:
      return unore.serialize(), 201
    if unore is None:
      return jsonify({'message':'Error try again later'}), 500
    return jsonify(unore), 500
  return jsonify({'message':'method not allowed'}),405


@api.route('/news', methods=['GET'])
def get_news():
  news = News.get_news()
  if news is not None:
    return jsonify(list(map(lambda item: item.serialize(), news))), 200
  if news is None: 
    return jsonify({'message':"News not found"}), 404
  return jsonify(news), 500


@api.route('/news', methods=['POST'])
@jwt_required()
def create_news():
  if request.method == 'POST':
    data_files = request.files
    data_form = request.form
    
    data = {
      'title':data_form.get('title'),
      'subtitle':data_form.get('subtitle'),
      'summary':data_form.get('summary'),
      'complete':data_form.get('complete'),
      'user_id':get_jwt_identity(),
      'image':data_files.get('image'),
      'image_secondary':data_files.get('image_secondary'),
      'image_preview':data_files.get('image_preview'),
      'highlighted':data_form.get('highlight')
    }

    
    if data is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('title') is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('subtitle') is None:  
      return jsonify({'message':'Bad request'}), 400
    if data.get('summary') is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('complete') is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('image') is None:
      return jsonify({'message':'Bad request'}), 400
    # if data.get('image_secondary') is None:
    #   return jsonify({'message':'Bad request'}), 400
    if data.get('image_preview') is None:
      return jsonify({'message':'Bad request'}), 400

    if data.get('image_secondary') is None:
      res_image_preview = uploader.upload(data_files["image_preview"])
      res_image = uploader.upload(data_files["image"])

      data.update({'image':res_image['secure_url']})
      data.update({'image_preview':res_image_preview['secure_url']})
      data.update({'public_id_image':res_image['public_id']})
      data.update({'public_id_preview':res_image_preview['public_id']})
      data.update({'image_secondary':""})
      data.update({'public_id_secondary':""})
    else:
      # si mandan las tres imagenes
      res_image = uploader.upload(data_files["image"])
      res_image_secondary = uploader.upload(data_files["image_secondary"])
      res_image_preview = uploader.upload(data_files["image_preview"])

      data.update({'image':res_image['secure_url']})
      data.update({'image_secondary':res_image_secondary['secure_url']})
      data.update({'image_preview':res_image_preview['secure_url']})
      data.update({'public_id_image':res_image['public_id']})
      data.update({'public_id_secondary':res_image_secondary['public_id']})
      data.update({'public_id_preview':res_image_preview['public_id']})

   
    news = News.create(data)
    if type(news) == News:
      return news.serialize(), 201
    if news is None:
      uploader.destroy(data['public_id_image'])
      uploader.destroy(data['public_id_secondary'])
      uploader.destroy(data['public_id_preview'])
      return jsonify({'message':'Error try again later'}), 500
    return jsonify(), 500
  return jsonify({'message':'method not allowed'}),405


@api.route("/news/<int:news_id>", methods=["DELETE"])
@jwt_required()
def delete_news(news_id=None):
  if request.method == "DELETE":
    if news_id is None:
      return jsonify({'message':'Bad request'}), 400

    if news_id is not None:
      news = News.query.get(news_id)

      if news is None:
        return jsonify({'message':'News not found'}), 404
      
      if news.user_id != get_jwt_identity():
        return jsonify({'message':'Unauthorized'}), 401
      
      try:
        # uploader.destroy(news.public_id_image)
        # uploader.destroy(news.public_id_secondary)
        # uploader.destroy(news.public_id_preview)
        db.session.delete(news)
        db.session.commit()
        return jsonify({'message':'News deleted'}), 204
      except Exception as error:
        print(error.args)
        return jsonify({'message':'Error try again later'}), 500
  return jsonify({'message':'method not allowed'}),405

@api.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id=None):
  if request.method == "PUT":
    print("entro")
    user = User.query.get(user_id)
    if user is None:
      return jsonify({'message':'User not found'}), 404

    user.email = "adjbermudez@gmail.com"

    try:
      db.session.commit()
      return jsonify({'message':'User updated'}), 200
    except Exception as error:
      print(error.args)
      return jsonify({'message':'Error try again later'}), 500
      
    print(user.serialize())
  return jsonify({'message':'method not allowed'}),405

@api.route("/contact", methods=["POST"])
def send_email():
  if request.method == "POST":
    data = request.get_json()
    if data is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('name') is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('emailAddress') is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('message') is None:
      return jsonify({'message':'Bad request'}), 400
    if data.get('subject') is None:
      return jsonify({'message':'Bad request'}), 400

    # message = f"Subject: {data.get('subject')}\n\n Reply-to: {data.get('email')}\n\n{data.get('message')}"
    message = f"Subject: {data.get('subject')}\nReply-To: {data.get('emailAddress')}\nFrom: {data.get('emailAddress')}\nTo: alexis.bermudez@undp.org\n\n{data.get('message')}"

   
    try:
      server = smtplib.SMTP('mail.merawear.com', 587)
      server.starttls()
      # server.login("ropamera@gmail.com", "whepujvkjcxgmvkh")
      server.login("sending@ppdvenezuela.org", "Kenco800")
      server.sendmail("sending@ppdvenezuela.org", "alexis.bermudez@undp.org" , message)
      server.quit()
      print("Email send")
      return jsonify({'message':'Email send'}), 200
    except Exception as error:
      print(error.args)
      print("Email not sending error ")
      return jsonify({'message':'Error try again later'}), 500
    return jsonify([]), 200




