#!/usr/bin/env python3
# coding: utf-8

import analyse_generale as ag
from flask import Flask
from flask import abort, request, make_response
from flask import render_template, redirect, url_for
import json
from data import USERS
# Set API dev in an another file
from api import SITE_API

app = Flask(__name__)
# Add the API
app.register_blueprint(SITE_API)


@app.route('/', methods=['GET', 'POST'])
@app.route('/<identifiant>')
def index(identifiant=None):
    app.logger.debug('serving root URL /')
    if request.method == 'POST':
        type_seq = request.form["type"]
        localisation = request.form["where"]
        ID =  request.form["id"]
        fichier =  request.form["seq"]
        graph = request.form["choix"]
        fichier,error,type_error=ag.choix(type_seq,graph,ID,fichier,localisation)
        if type_error!=0:
            abort(make_response(error, type_error))
        else:
            identifiant=ID
            return(fichier) # user= [username, gender, birth , wiki]
    return render_template('index.html')


@app.route('/about')
def about():
    app.logger.debug('about')
    return render_template('about.html', page_title="About")


def find_ref(ID_search):
    for item in REFS :
        if item['ID'] ==  ID_search :
            return True
        else :
            return False

def find_user(user_name):
    for item in USERS : 
        if item['name'] == user_name :
            birth = item['birth']
            wiki   = item['wikipageid']
            gender = item['gender']
    return user_name ,gender, birth ,  wiki


@app.route('/refs/', methods=['GET'])
@app.route('/refs/<ID>/')
def ref(ID=None):
     if not ID:
            return render_template('ref.html', refs=REFS)



@app.route('/users/', methods=['GET', 'POST'])
@app.route('/users/<username>/')
def users(username=None):
    app.logger.debug('Client request: method:"{0.method}'.format(request))
    if request.method == 'POST':
        username = request.form["Name"]
        birth =  request.form["Birth"]
        gender = request.form["Gender"]
        wikipedia_id  = request.form["Wikipedia_ID"] 
        return render_template('users.html', user= [username, gender, birth , wiki])
    else :
        if not username:
            return render_template('users.html', users=USERS)
        else: 
            username, gender, birth , wiki = find_user(username)
            return render_template('users.html', user= [username, gender, birth , wiki])
        

@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    app.logger.debug('Client request: method:"{0.method}'.format(request))
    search = request.args["pattern"]
    Name =[]
    for user in USERS :
         Name.append(user['name'])
    if search in Name :
        username, gender, birth , wiki = find_user(search)
        return render_template('users.html', user= [username, gender, birth , wiki])
    else :
        resp =  make_response("Not found" , 401)
        
        return resps
  
    


# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
