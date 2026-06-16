from flask import Flask,Blueprint,redirect,url_for
from app.controllers.backend import auth_controller

users_bp = Blueprint('users',__name__)

@users_bp.route('/user/create',methods = ['GET'])
def create():
    return auth_controller.signup()

@users_bp.route('/user/login',methods = ['GET'])
def login():
     return auth_controller.login()





