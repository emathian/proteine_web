#!/usr/bin/python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Projet Python 4BIM 2019
#                                                             Analyse de sequences nucleiques et proteiques
#----------------------------------------------------------------------------------------------------------------------------------------#

# IMPORTS -------------------------------------------------------------------------------------------------------------------------------#
import os
import lire_fasta as lf
import analyse_sequence_fasta as asf
# Pour pouvoir tracer les graphiques-----------------------------------------------------------------------------------------------------#
try:
    import matplotlib.pyplot as plt # Permet de tester la presence du module matplotlib sur le poste.
except ImportError:
    print("---------------\nAttention : Votre poste de travail n'est pas equipe du module matplotlib,\npar consequent le programme ne pourra pas generer de resultats graphiques\nseuls les tableaux de resultats seront generes.\n---------------")
    plt_dispo=False # (Variable globale) Si le module matplotlib n'est pas insatlle sur le poste la variable plt_dispo prend la valeur False et les graphiques des resultats ne seront pas traces.
else:
    plt.rcdefaults() # Permet de reinitialiser les parametres par defaut de matplotlib au cas ou ils aient ete modifier
    import numpy as np
    plt_dispo=True # (Variable globale) Si le module matplotlib est insatlle sur le poste la variable plt_dispo prend la valeur True.
#----------------------------------------------------------------------------------------------------------------------------------------#


def analyse_graph(nom_fichier, numero_fichier):
    """ Cette fonction permet de tracer un histogramme représentant la composition d'une séquence nucléique ou protéique,
    dont l'analyse a déjà été effectuée. Ainsi cette fonction prend en argument le nom du répertoire et celui du fichiers des 
    résultats. Cette analyse requiert le module matplotlib.  Si cette librairie est installée, l'utilisateur pourra choisir 
    de lancer ou non ce module graphique. Cette fonction ouvre une fenêtre graphique qui sera complétée par analyse_graph_adn
    ou analyse_graph_prot selon la nature de la séquence.
    """

    file=open(nom_fichier+"(%i).txt" % numero_fichier,'r') # Ouverture du fichier resultat en mode lecture.
    line=file.readline()[:-1].split("\t") #[:-1] pour ne pas prendre le "\n" en fin de ligne.
    if "Analyse_seq_prot" in nom_fichier:
        keys=line[4:]
        line=file.readline()[:-1].split("\t") 
        valeurs=line[4:] # Pour recuperer la liste des elements qui composent la sequence proteique.
    else :
        keys=line[3:]
        line=file.readline()[:-1].split("\t") 
        valeurs=line[3:] # Pour recuperer la liste des elements qui composent la sequence nucleique.
    valeurs=[int(i) for i in valeurs]
    objets = np.arange(len(valeurs))
    plt.subplots(figsize=(12,7)) # Permet de choisir la taille de la fenetre surgissante contenants les graphiques.
    plt.subplot(231) # Permet de choisir la position du graphique au sein de la fenetre surgissante.
    plt.gca().yaxis.grid() # Permet de faire apparaitre une grille horizontale uniquement.(Pour une meilleur lisibilite.)
    plt.bar(objets, valeurs, align='center', alpha=0.5 ,color='b')
    plt.xticks(objets, keys) # Pour faire apparaitre les elements composant la sequence sur l'axe des abscisses.
    plt.ylabel('Nombre de nucleotides')
    plt.title('Composition de la sequence')
    file.close()


def analyse_graph_adn(nom_fichier, numero_fichier):
    """ Cette fonction permet de tracer les graphiques des rapport CpG et des pourcentages C+G locaux (calculés par fenêtre d'analyse), 
    pour une séquence d'ADN dont l'anlyse a déjà été réalisée. Cette fonction prend ainsi en argument le nom du répertoire et celui
    du fichier des résultats.  Cette fonction requiert la librairie matplotlib. Les graphiques seront présentés sur la même fenêtre 
    que celle générée par analyse_graph, puis sera enregistré sous le format .png.  """
    
    analyse_graph(nom_fichier, numero_fichier)
    file=open(nom_fichier+"(%i).txt" % numero_fichier,'r') # Ouverture du fichier resultat en mode lecture.
    line=file.readline()[:-1].split("\t")
    compo=line[3:]
    line=file.readline()[:-1].split("\t")
    compo_nb=line[3:]
    compo_nb=[int(i) for i in compo_nb]
    for i in range(len(compo)):
        if compo[i]=="N":
            plt.text(-1,-sum(compo_nb)/5, "Attention il y a "+str(compo_nb[i])+" 'N' dans la sequence etudiee\n de longueur : "+str(sum(compo_nb))+" nucleotides." , fontsize=10,color='r' , bbox=dict(boxstyle="square,pad=0.3",fc="w",ec="r", lw=1))
    else:
        plt.text(-1,-sum(compo_nb)/5, "La sequence etudiee est composee de "+str(sum(compo_nb))+"\nnucleotides." , fontsize=10,color='b', bbox=dict(boxstyle="square,pad=0.3",fc="w",ec="b", lw=1))
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    if "Fenetres" in line : # Si la longueur de la sequence est inferieure a 200 nucleotides, cette partie de l'annalyse n'a pas pu etre effectuee car elle necessite des fenetres glissantes de 200 nucleotides.
        ilot_CpG=False
        plt_rapportCpG=True
        num_fenetre=[]
        rapportCpG=[]
        CGfenetre=[]
        line=file.readline()[:-1].split("\t")

        while line[0] != "":
            num_fenetre.append(int(line[0]))
            rapportCpG.append(float(line[3].replace(",",".")))
            CGfenetre.append(float(line[1].replace(",",".")))
            if line[3]!="NA":
                if line[4]=="Oui":
                    ilot_CpG=True
                    plt.subplot(222) # Ensemble de commande permettant de faire apparaitre les ilots CpG en rouge sur les graphiques.
                    plt.plot([int(line[0])+1],[float(line[3].replace(",","."))],'.r')
                    plt.subplot(224)
                    plt.plot([int(line[0])+1],[float(line[1].replace(",","."))],'.r')
            else:
                plt_rapportCpG=False
            line=file.readline()[:-1].split("\t")
        if plt_rapportCpG: # Pour ne pas afficher le graph CpG si certaine valeur de rapportCpG valent "NA".
            plt.subplot(222) # Ensemble de commandes permettants de tracer les graphiques resultats. Ici pour determiner la place du graphique dasn la fenetre surgissante.
            plt.title("Analyse de la presence d'ilots CpG\npour chaque fenetres glissantes de 200 nucleotides\nde la sequence") # Pour ajouter un titre.
            plt.grid() # Pour que la grille soit apparente.
            plt.plot(num_fenetre,rapportCpG,color='b')
            plt.axhline(0.6, linestyle=':', color='r')
            plt.ylabel("Rapports CpG") # Pour choisir le titre de l'axe des ordonnees.
            if ilot_CpG:
                plt.text(0,max(rapportCpG)-0.1, "Ilot CpG", fontsize=10,color='b',bbox=dict(boxstyle="square,pad=0.3",fc="r",ec="w", lw=2)) # Pour faire apparaitre du texte en bleu dans un cadre blanc sur fond rouge.
            plt.subplot(224)
        else:
            plt.subplot(222)
        plt.grid()
        plt.plot(num_fenetre,CGfenetre,color='b')
        plt.axhline(50, linestyle=':', color='r')
        plt.xlabel("Numero des fenetres glissantes") # Permet de choisir le titre de l'axe des abcisses.
        plt.ylabel("Pourcentages de C+G")
        if ilot_CpG:
            plt.text(0,max(CGfenetre)-5, "Ilot CpG", fontsize=10,color='b',bbox=dict(boxstyle="square,pad=0.3",fc="r",ec="w", lw=2))
        fichier_existe=True # Variable permettant de verifier que le fichier qu'on va creer n'en ecrase pas un preexistant.
        numero_fichier=0
        while fichier_existe: # Tant que le fichier "nom_fichier.png" existe le nom change.
            try: 
                sortie=open(nom_fichier+"(%i).png" % numero_fichier,'r') # Test si le fichier "nom_fichier.txt" existe.
            except FileNotFoundError: 
                fichier_existe=False
            else:
                sortie.close()
                numero_fichier+=1
                nom_fichier=nom_fichier.replace("(%i)" % (numero_fichier-1),"(%i)" % numero_fichier) # Si le fichier "nom_fichier.png" existe on change de nom pour ne pas l'ecraser.
        plt.savefig(nom_fichier+"(%i).png" % numero_fichier,format='png')
    file.close()
    

def analyse_graph_prot(nom_fichier, numero_fichier):
    """ Cette fonction permet de tracer le graphique de l'hydrophobicité local (hydrophobicité par fenêtre d'analyse), 
    pour une protéine dont l'anlyse a déjà été réalisée. Cette fonction prend ainsi en argument le nom du répertoire et celui
    du fichier des résultats.  Cette fonction requiert la librairie matplotlib. Le graphique sera présenté sur la même fenêtre 
    que celle générée par analyse_graph, puis sera enregistré sous le format .png.  """
  
    analyse_graph(nom_fichier, numero_fichier)
    file=open(nom_fichier+"(%i).txt" % numero_fichier,'r') # Ouverture du fichier resultat en mode lecture.
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    if "Fenetres" in line : # Dans ce "if" recuperation et traitement des resultats par fenetre glissante de 9 acide amines.
        num_fenetre=[]
        hydrophobicite=[]
        line=file.readline()[:-1].split("\t")
        while line[0] != "":
            num_fenetre.append(int(line[0]))
            hydrophobicite.append(float(line[1].replace(",",".")))
            line=file.readline()[:-1].split("\t")
        plt.subplot(212)
        plt.title("Hydrophobicite moyennes de chaque fenetre glissante de 9 acides amines de la sequence")
        plt.grid()
        plt.axhline(0, linestyle=':', color='k')
        plt.plot(num_fenetre,hydrophobicite)
        plt.xlabel("Numero des fenetres glissantes")
        plt.ylabel("hydrophobicite (Echelle de Fauchere et Peliska)")
        if max(hydrophobicite)>0:
            plt.annotate("",xy=(0.5,0), xycoords='data',xytext=(0.5,max(hydrophobicite)), textcoords='data',arrowprops=dict(arrowstyle="<->",connectionstyle="arc3",color='r'), )
            plt.text(-max(num_fenetre)/50,max(hydrophobicite)-0.2, "Partie hydrophobe", fontsize=8,color='r',rotation=85)
        if min(hydrophobicite)<0:
            plt.annotate("",xy=(0.5,0), xycoords='data',xytext=(0.5,min(hydrophobicite)), textcoords='data',arrowprops=dict(arrowstyle="<->",connectionstyle="arc3",color='b'), )
            plt.text(-max(num_fenetre)/50,0, "Partie hydrophile", fontsize=8,color='b',rotation=85)
        fichier_existe=True # Variable permettant de verifier que le fichier qu'on va creer n'en ecrase pas un preexistant.
        numero_fichier=0
        while fichier_existe: # Tant que le fichier "nom_fichier.png" existe le nom change.
            try: 
                sortie=open(nom_fichier+"(%i).png" % numero_fichier,'r') # Test si le fichier "nom.txt" existe.
            except FileNotFoundError: 
                fichier_existe=False
            else:
                sortie.close()
                numero_fichier+=1
                nom_fichier=nom_fichier.replace("(%i)" % (numero_fichier-1),"(%i)" % numero_fichier) # Si le fichier "nom_fichier.png" existe on change de nom pour ne pas l'ecraser.
        plt.savefig(nom_fichier+"(%i).png" % numero_fichier,format='png')
    file.close()
    


def choix(type_seq, graph, id_seq, fichier, loc):
  if loc=="web":
    des,seq=lf.recup_fasta_web(id_seq,type_seq)
  else :
    des,seq=lf.lire_fasta(fichier)
    print("FICHIER:"+id_seq)
    print("DESCRIPTION:"+des)
    print("SEQUENCE:"+seq)
  des = des.replace(" ", "")
  des = des.replace(",", "_")
  des = des.replace(".", "_")
  des = des.replace("|", "_")
  if type(seq)==int:
    error=des
    type_error=seq
    return("",error,type_error)
  creation_repertoire(des)
  if type_seq=="prot":
    file_name = "Analyse_proteine_"+des
    nom_fichier, numero_fichier =creation_fichier(file_name)
    fichier,error,type_error=asf.resultat_prot(des,seq, nom_fichier, numero_fichier)
    if plt_dispo:
      analyse_graph_prot(nom_fichier, numero_fichier)  
  else:
    file_name = "Analyse_adn_"+des
    nom_fichier, numero_fichier = creation_fichier(file_name)
    fichier,error,type_error=asf.resultat_ADN(des,seq, nom_fichier , numero_fichier)
    if plt_dispo:
      analyse_graph_adn(nom_fichier, numero_fichier)
  os.chdir("./../..")
  return(fichier,error,type_error)



def creation_repertoire(des):
	"""Cette fonnction permet de créer un répertoire pour contenir les fichiers des résultats. Le répertoire crée se nommera 		Analyse_(Descrition),
    la description est donnée en argument. Si le répertoire a déjà été crée lors d'une précédente analyse un Warning est envoyé à l'utilisateur.
    Il pourra faire le choix d'approfondir l'analyse de la séquence ou de lancer le programme sur une autre séquence."""
	
	os.chdir("./data")    
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
            sortie=open(nom_fichier+"(%i).txt" % numero_fichier,'r') # Test si le fichier "nom_fichier.txt" existe.
        except FileNotFoundError:
            fichier_existe=False
        else:
            sortie.close()
            numero_fichier+=1
            nom_fichier=nom_fichier.replace("(%i)" % (numero_fichier-1),"(%i)" % numero_fichier)  
    return(nom_fichier, numero_fichier)




