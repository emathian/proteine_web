#!/usr/bin/env python3
# coding: utf-8



import analyse_generale as ag
import os
from flask import Flask
from flask import abort, request, make_response
from flask import render_template, redirect, url_for
import json
import re
from flask import send_from_directory
# from data import USERS
# Set API dev in an another file
#from api import SITE_API

app = Flask(__name__)
# Add the API
# app.register_blueprint(SITE_API)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<identifiant>')
def index(identifiant=None):
    exist=False
    # récupération des données d'entrée (séquence) et appel de la fonction d'analyse
    app.logger.debug('serving root URL /')
    if request.method == 'POST':
        type_seq = request.form["type"]
        localisation = request.form["where"]
        ID =  request.form["id"]
        fichier =  request.form["seq"]
        ##graph = request.form["choix"] # On l'a enlevé finalement
        liste_dossier=os.listdir("static/data/")
        for file in liste_dossier :
            if ID in file :
                exist=True
        if not exist :
            nom_dossier,error,type_error=ag.choix(type_seq,ID,fichier,localisation) #(type_seq,graph,ID,fichier,localisation)
            if type_error!=0:
                #abort(make_response(error, type_error))
                return render_template('index.html',error=error,type_error=type_error)
            else:
                identifiant=ID
                os.chdir("./..")
                image,texte=get_infos_analyse(nom_dossier)
                return render_template('analyses.html',analysis=texte, images=image)
        else :
            return render_template('index.html',error="L'analyse que vous souhaitez effectuer existe déjà dans notre base de donnée.\nRendez-vous sur la page Analyses pour la consulter ou demandez une autre analyse.")
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


def get_infos_analyse(nomdossier):
    list_fichier=os.listdir("static/data/{nomdossier}/".format(nomdossier=nomdossier))
    texte=[] # liste contenant le contenu des différents fichiers texte
    image=[] # liste contenant le lien vers les différents images
    for item in list_fichier:
        if item.find(".txt")>=0:
           app.logger.debug(item)
           texte.append(readfile("static/data/{nomdossier}/{item}".format(nomdossier=nomdossier, item=item)))
        elif item.find(".png")>=0:
            app.logger.debug(item)
            image.append("../../static/data/{nomdossier}/{image}".format(nomdossier=nomdossier, image=item))
    return(image,texte)



@app.route('/analyses/')#, methods=['GET', 'POST'])
@app.route('/analyses/<nomdossier>/')
def analyses(nomdossier=None,filtred_data=None):
    """ Affiche la liste des analyses déjà effectuées ainsi que le contenu (fichier texte+images) des résultats des analyses """
    app.logger.debug('Client request: method:"{0.method}'.format(request))
    if not nomdossier:
        if filtred_data:
            return render_template('analyses.html', repertories=filtred_data)
        else:
            list_dossier=os.listdir("static/data/")
            return render_template('analyses.html', repertories=list_dossier)
    else:
        image,texte=get_infos_analyse(nomdossier)
        return render_template('analyses.html',analysis=texte, images=image)
    return render_template("analyses.html")



def get_info_filtred_data(liste_dossier, pattern):
    filtered_data=[]
    exist=False
    for file_name in liste_dossier :
        try:
            if re.match(pattern, file_name):
                filtered_data.append(file_name)
                exist=True
        except:
            return render_template('analyses.html',error="Le pattern %s n'est pas une expression régulière correcte."%(pattern))
    if exist:
        return(analyses(filtred_data=filtered_data))
    else:
        return render_template('analyses.html',error="Pas de nom d'analyse contenant %s."%(pattern))


def get_info(liste_dossier, pattern):
    if pattern in liste_dossier:
        image,texte=get_infos_analyse(pattern)
        return render_template('analyses.html',analysis=texte, images=image)
    else:
        return render_template('analyses.html',error="Pas de dossier d'analyse nommé %s."%(pattern))
        #abort(make_response('No user named %s'%(username), 501))



@app.route('/search/', methods=['GET'])
@app.route('/search/<nomdossier>/')
def search(nomdossier=None):
    app.logger.debug(request.args)
    if not nomdossier:
        pattern=request.args["pattern"]
        if "regexp" in request.args:
            liste_dossier=os.listdir("static/data/")
            return get_info_filtred_data(liste_dossier, pattern)
        else:
            liste_dossier=os.listdir("static/data/")
            return get_info(liste_dossier, pattern)
    else:
        image,texte=get_infos_analyse(nomdossier)
        return render_template('analyses.html',analysis=texte, images=image)





# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
