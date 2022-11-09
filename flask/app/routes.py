""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route("/")
def homepage():
    """ returns rendered homepage """

    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login():
    netId = request.form.get("netId")
    password = request.form.get("password")
    ret = db_helper.login(netId, password)
    if ret == 2:
        result = {'success': False, 'response': 'User Not Found (NetId: {})'.format(netId)}
    elif ret == 3:
        result = {'success': False, 'response': 'Password incorrect (NetId: {})'.format(netId)}
    else:
        result = {'success': True, 'response': 'Login Success. Your NetId is {}, UserType {}.'.format(netId, 'Student' if ret==0 else 'Professor')}
    return jsonify(result)
    #after log in, determine if student account or prof account, then render the according home page


#this is student home page
@app.route("/student", methods=['POST'])
def student():
    netId = request.form.get("netId")
    password = request.form.get("password")
    ret = db_helper.login(netId, password)
    if ret == 2:
        result = {'success': False, 'response': 'User Not Found (NetId: {})'.format(netId)}
    elif ret == 3:
        result = {'success': False, 'response': 'Password incorrect (NetId: {})'.format(netId)}
    else:
        result = {'success': True, 'response': 'Login Success. Your NetId is {}, UserType {}.'.format(netId, 'Student' if ret==0 else 'Professor')}
    return jsonify(result)

#faculty home page
@app.route("/faculty", methods=['POST'])
def faculty():
    netId = request.form.get("netId")
    password = request.form.get("password")
    ret = db_helper.login(netId, password)
    if ret == 2:
        result = {'success': False, 'response': 'User Not Found (NetId: {})'.format(netId)}
    elif ret == 3:
        result = {'success': False, 'response': 'Password incorrect (NetId: {})'.format(netId)}
    else:
        result = {'success': True, 'response': 'Login Success. Your NetId is {}, UserType {}.'.format(netId, 'Student' if ret==0 else 'Professor')}
    return jsonify(result)


