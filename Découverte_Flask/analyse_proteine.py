#!/usr/bin/python3

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Projet Python L3 BIM 2017
#                                                                  Analyse de sequence proteique
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import random

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Variables globales :

# Echelle d'hydrophobicite de Fauchere et Peliska :
dico_aa_hydrophobes={"E":-0.640,"D":-0.770,"A":0.310,"R":-1.010,"N":-0.600,"C":1.540,"Q":-0.220,"G":0.000,"H":0.130,"I":1.800,"L":1.700,"K":-0.990,"M":1.230,"F":1.790,"P":0.720,"S":-0.040,"T":0.260,"W":2.250,"Y":0.960,"V":1.220}

# Charge des differents acide amines a pH phisiologique (pH=7.4) :
dico_charge_aa={"E": -1.2,"D":-1.2,"A":-0.2,"R":0.8,"N":-0.2,"C":-0.3,"Q":-0.2,"G":-0.2,"H":-0.1,"I":-0.2,"L":-0.2,"K":0.8,"M":-0.2,"F":-0.2,"P":-0.2,"S":-0.2,"T":-0.2,"W":-0.2,"Y":-0.2,"V":-0.2}

# Corespondance code 3 lettres, code 1 lettre des acides amines : 
dico3aa1={"GLU":"E","ASP":"D","ALA":"A","ARG":"R","ASN":"N","CYS":"C","GLN":"Q","GLY":"G","HIS":"H","ILE":"I","LEU":"L","LYS":"K","MET":"M","PHE":"F","PRO":"P","SER":"S","THR":"T","TRP":"W","TYR":"Y","VAL":"V"}

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def code3aa1(seq): # Permet de convertir les sequences d'acide amines en code 3 lettres en sequence d'acide amines en code 1 lettre.
    "Cette fonction permet de convertir une sequence proteique codee en code trois lettres donnee en argument en une sequence proteique codee en code une lettre."
    if seq[0] in dico3aa1.keys(): # Verifie si la sequence est codee en code 3 lettres.
        for ele in seq: # Parcours la sequence donne en entree et convertie chacun de ces elements ecrits en code 3 lettres en code 1 lettre. 
            seq1l=dico3aa1(ele)
        return seq1l
    else: # Si la sequence est deja codee en code 1 lettre le programme ne la modifie pas.
        return seq

def composition(seq): # Donne la composition de la sequence en acide amines. (Fonctionne pour les sequence proteique ou nucleotidique)
    "Cette fonction donne la composition en chaque element d'une sequence donnee en entree." 
    seq=seq.strip()
    dico={}
    for ele in seq:
        if ele in dico: # Si la cle "ele" existe deja on rajoute 1 a sa valeur.
            dico[ele]+=1
        else: # Si la cle "ele" n'existe pas on la cree et on lui associe la valeur 1.
            dico[ele]=1
    return(dico)

def nb_residus_hydrophobes(seq): # Permet de compter le nombre de residus hydrophobes presents dans une sequence donnees.
    "Cette fonction calcule le nombre de residus hydrophobes presents dans une sequence donnee en argument." 
    dico=composition(seq)
    nb_aa_hydrophobe=0
    for ele in dico : 
        if dico_aa_hydrophobes[ele] > 0:
            nb_aa_hydrophobe+=dico[ele]
    return(nb_aa_hydrophobe)

def residus_charges_et_charge_net(seq,compo=-1): # Renvoi le pourcentage de residus charges presents dans la sequence et la charge net de la sequence.
    "Cette fonction calcule le pourcentage de residus charges (premiere sortie) presents dans une sequence donnee en argument et la charge net (deuxieme sortie) de cette meme sequence. Elle peut egalement prendre en deuxieme argument la composition de la sequence sous forme d'un dictionnaire elle ira alors plus vite. (Par defaut la composition est calculee par la fonction.)"
    if compo==-1:
        dico=composition(seq)
    else:
        dico=compo
    nb_aa_charges=0
    charge=0
    for ele in dico :
        charge+=dico_charge_aa[ele]*dico[ele]
        if dico_charge_aa[ele] < -0.5 or dico_charge_aa[ele] > 0.5: # Les element dont la charge est comprise entre -0.5 et 0.5 sont consideres comme neutres. 
            nb_aa_charges+=dico[ele]
    nb_aa_charges=nb_aa_charges/len(seq)*100
    return(nb_aa_charges,charge)

def nb_residus_hydrophobes_et_residus_charges_et_chage_net(seq,compo=-1): # Fonction qui renvoi le nombre de residus hydrophobe et le pourcentage de residus charges present et la charge net. Plus rapide puisqu'elle recupere l'information de la composition au lieu de la recalculer
    "Cette fonction calcule le nombre de residus hydrophobes (premiere sortie), le pourcentage de residus charges (deuxieme sortie) presents dans une sequence donnee en argument et la charge net (troisieme sortie) de cette meme sequence. Elle peut egalement prendre en deuxieme argument la composition de la sequence sous forme d'un dictionnaire elle ira alors plus vite. (Par defaut la composition est calculee par la fonction.)"
    nb_aa_hydrophobe=0
    nb_aa_charges=0
    charge=0
    if compo==-1:
        compo=composition(seq)
    for ele in compo : 
        if dico_aa_hydrophobes[ele] > 0:
            nb_aa_hydrophobe+=compo[ele]
        charge+=dico_charge_aa[ele]*compo[ele]
        if dico_charge_aa[ele] < -0.5 or dico_charge_aa[ele] > 0.5: # Les element dont la charge est comprise entre -0.5 et 0.5 sont consideres comme neutres. 
            nb_aa_charges+=compo[ele]
    nb_aa_charges=nb_aa_charges/len(seq)*100
    return(nb_aa_hydrophobe,nb_aa_charges,charge)

def hydrophobicite_moyenne(seq,taille=-1,compo=-1): # Permet de calculer l'hydrophobicite moyenne d'une sequence ou d'une fenetre glissate de taille donnee.
    "Cette fonction calcule l'hydrophobicite moyenne d'une sequence donnee en premier argument (par defaut) ou dans toutes les fenetres glissante de longueurs donnees en deuxieme argument."
    if taille==-1:
        taille=len(seq)
    seq=seq.upper()
    longueur=len(seq)
    hydrophobicite=0
    hydrophobicites=[]
    if taille<=longueur:
        for i,element in enumerate(seq[:longueur-(taille-1)]): # Cette boucle permet de parcourir l'ensemble des fenetres de taille donnee en entree (ou de la sequence entiere).
            fenetre=seq[i:i+taille]
            if taille==-1:
                if compo==-1:
                    dico=composition(fenetre)
                else:
                    dico=compo
            else:
                dico=composition(fenetre)
            for ele in dico : # Permet de calculer l'hydrophobicite d'une fenetre.
                hydrophobicite+=dico[ele]*dico_aa_hydrophobes[ele]/taille 
            hydrophobicites.append(hydrophobicite)
            hydrophobicite=0
        return(hydrophobicites)
    else:
        return('')
    

    
