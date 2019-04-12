#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#																Projet Prog web 4BIM
#															 Analyse de sequences fasta
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#Import de modules locaux :
import analyse_ADN as an
import analyse_proteine as ap


def resultat_ADN(des, seq, nom_fichier , numero_fichier, compo=-1, keys=-1  ): 
	# Permet d'obtenir les tableaux de resultats et les graphiques correspondants de l'analyse de la sequence ADN.
	"""Pour fonctionner, ce module fait appel a cinq autres modules qui doivent se trouver dans le meme repertoire courant que lui :
	recuperation_sequence_fasta, lire_fasta, analyse_ADN, analyse_proteine, et creation_seq_aleatoires. Cette procedure permet d'effectuer
	une etude de sequence nucleique. Cette etude consiste en un calcul du pourcentage de C+G et de CpG dans la sequence entiere, et en un 
	calcule du rapport CpG, du pourcentage de C+G, et du nombre de CpG par fenetre glissante de deux cents nucleotides ainsi qu'une conclsion 
	sur la presence ou non d'ilots CpG. La procedure cree un a deux fichiers de sortie : un fichier tabule (pouvant etre ouvert avec un editeur
	de texte ou un tableur comme Excel) et une image des graphiques qu'elle engendre sous certaines conditions. Elle prend en arguments une 
	description et la sequence correspondante au minimum. En troisieme argument elle prend la composition de la sequence (compo=) sous forme de 
	dictionnaire, par defaut cette composition est calculee dans la procedure. De meme en quatrieme argument elle prend la liste des caracteres 
	composants la sequence (keys=) (chacun ecrit entre guillemets), par defaut cette liste est calculee par la procedure."""
	sortie=open(nom_fichier+"(%i).txt" % numero_fichier,'a')	
	compo=an.composition(seq)
	keys=[]
	for key in compo.keys():
	  keys.append(key)

	CG,pourcentCpG=an.contenu_C_et_G_et_nb_CpG(seq,  comp=compo) # Recuperation du pourcentage de C+G dans la sequence.
	pourcentCpG=pourcentCpG[0]/len(seq)*100 # Recuperation  de nombre de "CG" dans la sequence.
	num_fenetre=[]
	sortie.write("\tC+G(%)\tCpG(%)") # Redaction des entetes du tableau resultat consernant l'etude de la sequence entiere.

	resultats="\n sequence entiere\t%.3f" % CG[0] + "\t%.3f" % pourcentCpG # Puis des resultats correspondants.
	for ele in keys:
		sortie.write("\t%s"%(ele))
		resultats+="\t"+str(compo[str(ele)])
		resultats=resultats.replace(".",",")
	sortie.write(resultats)
	if len(seq)>=200: # Si la longueur de la sequence est inferieure a 200 nucleotides, cette partie de l'analyse n'a pas pu etre effectuee car elle necessite des fenetres glissantes de 200 nucleotides.
		sortie.write("\n \n \nFenetres\tC+G(%)\tCpG\tRapport CpG\tIlot CpG\n" )# Redaction des entetes du tableau resultat consernant l'etude de la sequence par fenetres glissantes. 
		rapportCpG,CpGfenetre,CGfenetre=an.rapport_CpG_nb_CpG_contenu_C_et_G(seq, 200)# Recuperation du porcentage de C+G dans chaque fenetre, du nombre de "CG" et du rapport CpG.
		ilot_CpG=False
		plt_rapportCpG=True
		for i,ele in enumerate(CGfenetre): # On parcours l'une des liste de resultat de l'analyse par fenetre, elles ont toutes la meme taille.
			num_fenetre.append(i+1)
			if rapportCpG[i]!="NA":
				if rapportCpG[i]>=0.6 and CGfenetre[i]>=50: # Permet de verifier la presence d'ilot CpG.
					ilot_CpG=True
					resultatsfenetres=str(i+1)+"\t%.3f" % CGfenetre[i] +"\t"+str(CpGfenetre[i])+"\t%.3f" % rapportCpG[i] +"\tOui\n" # Redaction des resultats obtenus pour la fenetre i (si presence d'un ilot CpG,cf "else" sinon)
				else:
					resultatsfenetres=str(i+1)+"\t%.3f" % CGfenetre[i] +"\t"+str(CpGfenetre[i])+"\t%.3f" % rapportCpG[i] +"\tNon\n"
			else:
				resultatsfenetres=str(i+1)+"\t%.3f" % CGfenetre[i] +"\t"+str(CpGfenetre[i])+"\t%s" % rapportCpG[i] +"\tNon\n"
				plt_rapportCpG=False
			resultatsfenetres=resultatsfenetres.replace(".",",") # On remplace les points par des virgules pour que les valeurs soient reconnus comme des nombres par Excel
			sortie.write(resultatsfenetres)
			error=""
			type_error=0
 
	else:
	  error="---------------\nAttention : Execution incomplete du programme.\n\nSeule l'analyse sur la sequence entiere a pu etre effectuee.\nLes analyses par fenetre requierent une sequence de longueur minimum 200 nucleotides.\n---------------\n"
	  type_error=500
	sortie.close()
	fichier = "ok :)"
	return(fichier, error, type_error)

		

	
def resultat_prot(des,seq, nom_fichier , numero_fichier): # Permet d'obtenir les tableaux de resultats et les graphiques correspondants de l'analyse de la sequence proteique. (Fonctionnement tres similaire a "resultat_ADN")
	"""Pour fonctionner ce module fait appel a cinq autres modules qui doivent se trouver dans le meme repertoire courant que lui :
	recuperation_sequence_fasta, lire_fasta, analyse_ADN, analyse_proteine, et creation_seq_aleatoires. Cette procedure permet d'effectuer
	une etude de sequence proteique. Cette etude consiste en un calcul du nombre d'acide amines hydrophobe presents, du nombre d'acide 
	amines charges presents, et de la charge net de la sequence entriere, et en un calcul de l'hydrophobicite moyenne dans chaque fenetre
	glissante de neuf acides amines. La procedure cree un a deux fichiers de sortie : un fichier tabule (pouvant etre ouvert avec un editeur
	de texte ou un tableur comme Excel) et une image des graphiques qu'elle engendre sous certaines conditions. Elle prend en arguments une 
	description et la sequence correspondante au minimum. En troisieme argument elle prend la composition de la sequence (compo=) sous forme 
	de dictionnaire, par defaut cette composition est calculee dans la procedure. De meme en quatrieme argument elle prend la liste des caracteres 
	composants la sequence (keys=) (chacun ecrit entre guillemets), par defaut cette liste est calculee par la procedure.""" 

	sortie=open(nom_fichier+"(%i).txt" % numero_fichier,'a')
	compo=ap.composition(seq)
	keys=[]
	for key in compo.keys():
		keys.append(key)

	nb_aa_hydrophobe,aa_charges,charge=ap.nb_residus_hydrophobes_et_residus_charges_et_chage_net(seq,compo) # Recuperation les resultats de l'etude de la sequence entiere.
	num_fenetre=[]
	sortie.write("\taa hydrophobes\taa charges (%)\tcharge net") # Redaction du tableau de resultat de l'etude sur la sequence entiere (sur cette ligne et les 5 suivantes).
	resultats="\nsequence entiere\t"+str(nb_aa_hydrophobe)+"\t%.3f" % aa_charges +"\t%.3f" % charge
	for ele in keys:
		sortie.write("\t%s"%ele)
		resultats+="\t"+str(compo[str(ele)])
		resultats=resultats.replace(".",",")
	sortie.write(resultats)
	if len(seq)>=9: # Dans ce "if" recuperation et traitement des resultats par fenetre glissante de 9 acide amines.
		hydrophobicite=ap.hydrophobicite_moyenne(seq, 9)
		sortie.write("\n \n \nFenetres\thydrophobicite moyenne\n")
		for i,ele in enumerate(hydrophobicite):
			num_fenetre.append(i+1)
			resultatsfenetres= str(i+1)+"\t%.3f" % hydrophobicite[i] +"\n"
			resultatsfenetres=resultatsfenetres.replace(".",",") # On remplace les points par des virgules pour que les valeurs soient reconnus comme des nombres par Excel
			sortie.write(resultatsfenetres)
			error=""
			type_error=0
	else:
		error="---------------\nAttention : Execution incomplete du programme.\n\nSeule l'analyse sur la sequence entiere a pu etre effectuee.\nLes analyses par fenetre requierent une sequence de longueur minimum 9 acides amines.\n---------------\n"
		type_error=500
	sortie.close()
	fichier = "ok :)"
	return(fichier, error, type_error)
		
		
	
