#!/usr/bin/env python3
# coding: utf-8

import re
from flask import Flask
from flask import abort, request, make_response
from flask import render_template, redirect, url_for

from data import USERS
# Set API dev in an another file
from api import SITE_API

app = Flask(__name__)
# Add the API
app.register_blueprint(SITE_API)

# Code d'origine
#@app.route('/hello_world')
#def hello_world(name=None):
#    app.logger.debug('Hello world')
#    return 'Hello, World!' , 200
    
# Question 1: Un header inutile !! header est un simple dictionnaire qu'on peut enrichier avec toutes les valeurs qu'on veut.
#@app.route('/hello_world')
#def hello_world(name=None):
#    app.logger.debug('Hello world')
#    resp=make_response('Hello, World!')
#    resp.headers['X-Parachutes'] = 'parachutes are cool'
#    return resp 
    
# Question 2 et 3: des headers utiles : content-type et content-language
#@app.route('/hello_world')
#def hello_world(name=None):
#    app.logger.debug('Hello world')
#    resp=make_response('Hello, World!')
#    resp.headers['Content-Type'] = 'text/css; charset=utf-8'
#    resp.headers['Content-Language'] = 'en-US, fr-FR'
#    return resp 


# Question 4: des headers utiles : Accept language
@app.route('/hello_world')
def hello_world(name=None):
    # Reponse dans la bonne langue :
    app.logger.debug('Hello world')
    resp=make_response('Hello, World!')
    resp.headers['Content-Type'] = 'text/css; charset=utf-8'
    resp.headers['Content-Language'] = 'en-US'
    # Recuperer la valeur de Accept-Language :
    if 'Accept-Language' in request.headers:
        lang=request.headers.get('Accept-Language')
        if 'fr' in lang :
            resp.headers['Content-Language'] = 'fr-FR'
            resp.data='Bonjour le monde !'
    return resp     


@app.route('/')
def index():
    app.logger.debug('serving root URL /')
    return render_template('index.html')
    

@app.route('/indexapi')
def indexapi():
    return render_template('indexapi.html')


# Code origine :
#@app.route('/about')
#def about():
#    app.logger.debug('about')
#    return render_template('about.html')
    
    
# Pour changer le titre dans la page About (mais ce n'est pas ça qu'il fallait faire) :
#@app.route('/about')
#@app.route('/about/<title>')
#def about(title='Lorem ipsum'):
#    app.logger.debug('about')
#    return render_template('about_change_title.html', title=title)


# Pour changer le titre dans la page About CORRECTION :
@app.route('/about')
def about():
    app.logger.debug('about')
    return render_template('about.html',page_title="About")
    
   


@app.route('/help')
def help():
    return render_template('help.html')


def find_user(name):
    for user in USERS:
        if user["name"]==name:
            birth=user["birth"].split("T")[0]
            fields=user["fields"]
            gender=user["gender"]
            user_id=user["id"]
            return(birth,fields,gender,user_id)
            

@app.route('/users/')
@app.route('/users/<username>/')
def users(username=None):
    if not username:
        return render_template('users.html',users=USERS) # USERS provient de from data import USERS
    else:
        birth,fields,gender,user_id=find_user(username)
        return render_template('users.html',users=USERS ,user=username, birth=birth ,fields=fields ,gender=gender ,user_id=user_id) 
    abort(404)


# Code d'origine : 
#@app.route('/search/', methods=['GET'])
#def search():
#    app.logger.debug(request.args)
#    abort(make_response('Not implemented yet ;)', 501))

def users_get_names():
    names=[]
    for user in USERS:
        names.append(user["name"])
    return names

def get_info_names(names, username):
    if username in names:
        birth,fields,gender,user_id=find_user(username)
        return render_template('users.html',users=USERS ,user=username, birth=birth ,fields=fields ,gender=gender ,user_id=user_id) 
    else:
        return render_template('users.html',error='No user named %s.'%(username)) 
        #abort(make_response('No user named %s'%(username), 501))

def get_info_filtred_names(names, username):
    filtered_names=[]
    exist=False
    for name in names :
        if re.match(username, name):
            filtered_names.append(name)
            exist=True
    if exist:
        return render_template('users.html',users=USERS,filtre=filtered_names) 
    else:
        return render_template('users.html',error='No user named %s.'%(username))
    
    
# Pour implementer la barre de recheche :
@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    username=request.args["pattern"]
    if "regexp" in request.args:
        names=users_get_names()
        return get_info_filtred_names(names, username)
    else:
        names=users_get_names()
        return get_info_names(names, username)
     
        

def users_get_id():
    ids=[]
    for user in USERS:
        ids.append(user["id"])
    return (max(ids)+1)
    

# Pour inscrire un nouvel utilisateur :
@app.route('/register', methods=['GET','POST']) # Si on ne met rien c'est POST par défaut
def register():
    if request.method == 'POST':
        user={}
        user['birth']=request.form["birth"]+"T00:00:00.000Z"
        user['fields']=request.form["fields"]
        user['gender']=request.form["gender"]
        user['id']=users_get_id()
        user['name']=request.form["name"]
        user['wikipageid']=request.form["wikipageid"]
        global USERS
        USERS.append(user)
        #print(type(USERS))
        return render_template('users.html',users=USERS ,user=user['name'], birth=request.form["birth"] ,fields=user['fields'] ,gender=user['gender'] ,user_id=user['id']) 
        #return "Your are in !"
    else:
        return render_template('register.html')
    #return render_template('register.html')

# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
