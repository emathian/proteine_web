#!/usr/bin/env python3
# coding: utf-8



import analyse_generale as ag
import os
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
    # récupération des données d'entrée (séquence) et appel de la fonction d'analyse
    app.logger.debug('serving root URL /')
    if request.method == 'POST':
        type_seq = request.form["type"]
        localisation = request.form["where"]
        ID =  request.form["id"]
        fichier =  request.form["seq"]
        ##graph = request.form["choix"] # On l'a enlevé finalement
        fichier,error,type_error=ag.choix(type_seq,ID,fichier,localisation) #(type_seq,graph,ID,fichier,localisation)
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


@app.route('/refs/', methods=['GET'])
@app.route('/refs/<ID>/')
def ref(ID=None):
     if not ID:
            return render_template('ref.html', refs=REFS)

def readfile(nomfichier):
	text = open(nomfichier, 'r+')
	content = text.read()
	text.close()
	return content

@app.route('/analyses/', methods=['GET', 'POST'])
@app.route('/analyses/<nomdossier>/')
def analyses(nomdossier=None):
    """ Affiche la liste des analyses déjà effectuées ainsi que le contenu (fichier texte+images) des résultats des analyses """
    app.logger.debug('Client request: method:"{0.method}'.format(request))
    if not nomdossier:
        list_dossier=os.listdir("./data/")
        return render_template('analyses.html', repertories=list_dossier)
    else: 
        list_fichier=os.listdir("./data/{nomdossier}/".format(nomdossier=nomdossier))
        texte=[] # liste contenant le contenu des différents fichiers texte
        image=[] # liste contenant le lien vers les différents images
        for item in list_fichier:
            if item.find(".txt")>=0:
                app.logger.debug(item)
                texte.append(readfile("./data/{nomdossier}/{item}".format(nomdossier=nomdossier, item=item)))
            elif item.find(".png")>=0:
                image.append(item)
        #return render_template('analyses.html',analysis=[nomdossier, texte, image])
        return render_template('analyses.html',analysis=texte, images=image)

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
