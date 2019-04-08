#!/usr/bin/python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Projet Python 4BIM 2019
#                                                             Analyse de sequences nucleiques et proteiques
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import lire_fasta as lf
import analyse_sequence_fasta as asf
import os

def choix(type_seq, graph, id_seq, fichier, loc):
  if loc=="web":
    des,seq=lf.recup_fasta_web(id_seq,type_seq)
  else :
    des,seq=lf.lire_fasta(fichier)
    print("FICHIER:"+id_seq)
    print("DESCRIPTION:"+des)
    print("SEQUENCE:"+seq)
  if type(seq)==int:
    error=des
    type_error=seq
    return("",error,type_error)
  if type_seq=="prot":
    fichier,error,type_error=asf.resultat_prot(des,seq)
    file_name = "Analyse_proteine_"+des
  else:
    fichier,error,type_error=asf.resultat_ADN(des,seq)
    file_name = "Analyse_adn_"+des
  creation_repertoire(des)
  creation_fichier(file_name)
  
  return(fichier,error,type_error)



def creation_repertoire(des):
    """Cette fonnction permet de créer un répertoire pour contenir les fichiers des résultats. Le répertoire crée se nommera Analyse_(Descrition),
    la description est donnée en argument. Si le répertoire a déjà été crée lors d'une précédente analyse un Warning est envoyé à l'utilisateur.
    Il pourra faire le choix d'approfondir l'analyse de la séquence ou de lancer le programme sur une autre séquence."""
    premiere_analyse=True
    try:
        os.mkdir("Analyse_"+des) # Permet de tester si le dossier '"Analyse_"+des' existe.
    except FileExistsError:
        premiere_analyse=False # Si le dossier existe deja alors l'analyse de la sequence entree existe deja, on ne souhaite pas la refaire inutilement.
        print(" \nL'analyse de cette sequence a deja ete effectuee, vous pouvez \napprofondir cette analyse ou effectuer une annalyse sur une nouvelle sequence. \n")
    os.chdir("./Analyse_"+des) # Si le dossier existe deja il n'est pas cree et on rentre simplement dedans, sinon il a deja ete creer dans le 'try' et donc on rentre dedans.



def creation_fichier(nom_fichier) :
    """Cette fonction permet de créer les fichiers textes contenant les résultats. Cette fonction prévient la redondance des fichiers,
    ainsi le nom de chaque fichier est unique. """

    nom_fichier=nom_fichier.replace("\n","")
    fichier_existe=True # Variable permettant de verifier que le fichier qu'on va creer n'en ecrase pas un preexistant.
    numero_fichier=0
    while fichier_existe: # Tant que le fichier "nom_fichier.png" existe le nom change.
        try:
            sortie=open(nom_fichier+"(%i).txt" % numero_fichier,'r') # Test si le fichier "nom_fichier.py" existe.
        except FileNotFoundError:
            fichier_existe=False
        else:
            sortie.close()
            numero_fichier+=1
            nom_fichier=nom_fichier.replace("(%i)" % (numero_fichier-1),"(%i)" % numero_fichier)  
    return(nom_fichier, numero_fichier)




