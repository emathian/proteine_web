#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#																Projet Réseaux 4BIM
#															 Analyse de sequences fasta
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#Import de modules locaux :
import analyse_ADN as an
import analyse_proteine as ap
import creation_seq_aleatoires as csa


def resultat_ADN(des, seq, compo=-1, keys=-1): 
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


	if compo==-1: # Permet une utilisation dans un cas plus general dans lequel l'utilisateur ne disposerait pas de la composition de la sequnece.
		compo=an.composition(seq)
	if keys==-1: # Permet une utilisation dans un cas plus general dans lequel l'utilisateur ne disposerait pas d'une liste des caractères composants la sequnece.
		keys=[]
		for key in compo.keys():
			keys.append(key)
	nom="Analyse_seq_nucl_%s\n"%(des)

#------Envoie du nom fichier au client-------#
	nom=nom.encode()
	con.sendall(nom)
	rep=con.recv(255).decode()
#---------------------------------------------#

	CG,pourcentCpG=an.contenu_C_et_G_et_nb_CpG(seq, con, comp=compo) # Recuperation du pourcentage de C+G dans la sequence.
	pourcentCpG=pourcentCpG[0]/len(seq)*100 # Recuperation  de nombre de "CG" dans la sequence.
	num_fenetre=[]
	fichier="\tC+G(%)\tCpG(%)" # Redaction des entetes du tableau resultat consernant l'etude de la sequence entiere.
	resultats="\n sequence entiere\t%.3f" % CG[0] + "\t%.3f" % pourcentCpG # Puis des resultats correspondants.
	for ele in keys:
		fichier+="\t%s"%(ele)
		resultats+="\t"+str(compo[str(ele)])
		resultats=resultats.replace(".",",")
	fichier+=resultats
	if len(seq)>=200: # Si la longueur de la sequence est inferieure a 200 nucleotides, cette partie de l'analyse n'a pas pu etre effectuee car elle necessite des fenetres glissantes de 200 nucleotides.
		fichier+="\n \n \nFenetres\tC+G(%)\tCpG\tRapport CpG\tIlot CpG\n" # Redaction des entetes du tableau resultat consernant l'etude de la sequence par fenetres glissantes. 
		rapportCpG,CpGfenetre,CGfenetre=an.rapport_CpG_nb_CpG_contenu_C_et_G(seq, con, 200)# Recuperation du porcentage de C+G dans chaque fenetre, du nombre de "CG" et du rapport CpG.
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
			fichier+=resultatsfenetres

#-------Envoie du fichier au client-----------#
		fichier=fichier.encode()
		taille=str(len(fichier))
		con.sendall(taille.encode())
		rep=con.recv(255).decode()		   
		if rep=="OK":
			if int(taille)> 30000: # Si la taille du fichier à envoyer est supérieur à 30kb
				if int(taille)% 30000 !=0 :
					nb_file = (int(taille) // 30000) +1  # Nombre de fichiers à envoyer
					con.sendall(str(nb_file).encode()) # Envoie du nombre de fichiers
					rep=con.recv(255).decode()  # Confirmation de la réception
					for i in range(0,nb_file-1): # Envoi par paquet de 30kb
						fichier_c = fichier[i*30000:(i+1)*30000]
						con.sendall(fichier_c)
						rep=con.recv(255).decode() # Confirmation de la réception
					last_file_size = int(taille) - ((int(taille) // 30000)*30000) # Taille du dernier block 
					last_file_size =  str(last_file_size)
					con.sendall(last_file_size.encode()) # Envoi de la taille 
					rep=con.recv(255).decode() # Confirmation de la réception
					last_file = fichier[((int(taille) // 30000)*30000) : int(taille)] # Envoi du dernier block
					con.sendall(last_file)
					rep=con.recv(255).decode()
				else : # La taille des résultats est un multiple de 30000
					nb_file = (int(taille) // 30000)   # Nombre de fichiers à envoyer
					con.sendall(str(nb_file).encode()) # Envoie du nombre de fichiers
					rep=con.recv(255).decode()  # Confirmation de la réception
					for i in range(0,nb_file): # Envoi par paquet de 30kb
						fichier_c = fichier[i*30000:(i+1)*30000]
						con.sendall(fichier_c)
						rep=con.recv(255).decode() # Confirmation de la réception

			else :	
				con.sendall(fichier)
				rep=con.recv(255).decode()
#---------------------------------------------#
 
	else:
#---------------Mise en reseau----------------#
		con.sendall("---------------\nAttention : Execution incomplete du programme.\n\nSeule l'analyse sur la sequence entiere a pu etre effectuee.\nLes analyses par fenetre requierent une sequence de longueur minimum 200 nucleotides.\n---------------\n".encode())
		con.recv(255).decode()
#---------------------------------------------#
		
#-------Envoie du fichier au client-----------#
		fichier=fichier.encode()
		taille=str(len(fichier))
		con.sendall(taille.encode())
		rep=con.recv(255).decode()
		if rep=="OK":
			con.sendall(fichier)
#---------------------------------------------#

		

	
def resultat_prot(des,seq): # Permet d'obtenir les tableaux de resultats et les graphiques correspondants de l'analyse de la sequence proteique. (Fonctionnement tres similaire a "resultat_ADN")
	"""Pour fonctionner ce module fait appel a cinq autres modules qui doivent se trouver dans le meme repertoire courant que lui :
	recuperation_sequence_fasta, lire_fasta, analyse_ADN, analyse_proteine, et creation_seq_aleatoires. Cette procedure permet d'effectuer
	une etude de sequence proteique. Cette etude consiste en un calcul du nombre d'acide amines hydrophobe presents, du nombre d'acide 
	amines charges presents, et de la charge net de la sequence entriere, et en un calcul de l'hydrophobicite moyenne dans chaque fenetre
	glissante de neuf acides amines. La procedure cree un a deux fichiers de sortie : un fichier tabule (pouvant etre ouvert avec un editeur
	de texte ou un tableur comme Excel) et une image des graphiques qu'elle engendre sous certaines conditions. Elle prend en arguments une 
	description et la sequence correspondante au minimum. En troisieme argument elle prend la composition de la sequence (compo=) sous forme 
	de dictionnaire, par defaut cette composition est calculee dans la procedure. De meme en quatrieme argument elle prend la liste des caracteres 
	composants la sequence (keys=) (chacun ecrit entre guillemets), par defaut cette liste est calculee par la procedure.""" 

 
	compo=ap.composition(seq)
	keys=[]
	for key in compo.keys():
		keys.append(key)

	nb_aa_hydrophobe,aa_charges,charge=ap.nb_residus_hydrophobes_et_residus_charges_et_chage_net(seq,compo) # Recuperation les resultats de l'etude de la sequence entiere.
	num_fenetre=[]
	fichier="\taa hydrophobes\taa charges (%)\tcharge net" # Redaction du tableau de resultat de l'etude sur la sequence entiere (sur cette ligne et les 5 suivantes).
	resultats="\n sequence entiere\t"+str(nb_aa_hydrophobe)+"\t%.3f" % aa_charges +"\t"+str(charge)
	for ele in keys:
		fichier+="\t%s"%ele
		resultats+="\t"+str(compo[str(ele)])
		resultats=resultats.replace(".",",")
	fichier+=resultats
	if len(seq)>=9: # Dans ce "if" recuperation et traitement des resultats par fenetre glissante de 9 acide amines.
		hydrophobicite=ap.hydrophobicite_moyenne(seq, 9)
		fichier+="\n \n \nFenetres\thydrophobicite moyenne\n"
		for i,ele in enumerate(hydrophobicite):
			num_fenetre.append(i+1)
			resultatsfenetres= str(i+1)+"\t%.3f" % hydrophobicite[i] +"\n"
			resultatsfenetres=resultatsfenetres.replace(".",",") # On remplace les points par des virgules pour que les valeurs soient reconnus comme des nombres par Excel
			fichier+=resultatsfenetres
			error=""
			type_error=0
	else:
		error="---------------\nAttention : Execution incomplete du programme.\n\nSeule l'analyse sur la sequence entiere a pu etre effectuee.\nLes analyses par fenetre requierent une sequence de longueur minimum 9 acides amines.\n---------------\n"
		type_error=500
	return(fichier, error, type_error)
		
"""
def resultats_analyse_seq(addr): # Permet d'optenir les resultats de l'analyse d'une sequence ADN ou proteique sous forme de tableaux et de graphiques  
	reponse="Initialisation" # Condition utile pour commencer l'etude d'une nouvelle fonction.
	type_seq=""
	premiere_analyse=True # variable servant a ne pas refaire l'analyse d'une sequence deja effectuee.
	while reponse!="4":
		keys=[]
		valeurs=[]
		if type_seq=="": # Seulement si c'est la premiere analyse ou que l'utilisateur a demande a en commencer une nouvelle.
			des,seq,type_seq=rs.entree(addr)
			des=des.replace(",","_") # Ensemble de commande permettant de creer un nom de fichier sans caracteres compromettants.
			des=des.replace(".","")
			des=des.replace(" ","_")
			des=des.replace("\\","")
			des=des.replace("/","")
			des=des.replace("|","_")
			
#--------------Mise en reseau-----------------#
			con.sendall(("creation dossier:%s"%des).encode())
			premiere_analyse=con.recv(255).decode()
			premiere_analyse=premiere_analyse=="True"
			con.sendall("OK".encode())
#--------------------------------------------#
			
			sequence=seq # Permet de garder en memoire la sequence de reference de chaque analyse dans la variable 'seq'.
			description=""
		elif type_seq!="":
			if reponse=="Initialisation":
				if premiere_analyse: # Si une analyse identique a deja ete effectuee on ne la refait pas.
					seq=ap.code3aa1(sequence) # Permet de passer du code d'acide amines 3 lettres au code 1 lettre si besoin (si 'sequence' est nucleotidique ou deja en code 1 lettre rien ne change.)
					compo=ap.composition(sequence)
					for key in compo.keys():
						keys.append(key)
						valeurs.append(compo[str(key)])
					if type_seq=="prot":
						
#--------------Mise en reseau-----------------#
						con.sendall("resultat_prot".encode()) # mot clé pour lancer l'ecriture du fichier resultat chez le client
						rep=con.recv(255).decode()
#---------------------------------------------#
						
						resultat_prot(des+description,sequence,compo,keys,con)
					else :

#--------------Mise en reseau-----------------#
						con.sendall("resultat_adn".encode()) # mot clé pour lancer l'ecriture du fichier resultat chez le client
						rep=con.recv(255).decode()
#---------------------------------------------#
						
						resultat_ADN(des+description,sequence, con ,compo,keys)
			elif reponse=="1":
				reponse="Initialisation" # Permet de repartir dans la condition menant a l'analyse de la sequence.
				type_seq=""

#--------------Mise en reseau-----------------#
				con.sendall("nouvelle analyse".encode())
				rep=con.recv(255).decode()
#---------------------------------------------#
				
				premiere_analyse=True # On va passer a une nouvelle analyse on reinitialise donc la variable premiere_analyse.
				continue # Permet de passer au tour de boucle while suivant, pour retester les conditions sur la variable "reponse".
			elif reponse=="2":
				reponse="Initialisation"
				seq_meme_compo=csa.seq_meme_compo(seq) # Recupere une sequence de meme composition que "seq".
				description="_seq_meme_compo"
				sequence=seq_meme_compo # Ecrase "sequence" mais pas "seq" ce qui permet de garder en memoire la sequence de reference de chaque analyse dans la variable 'seq'.
				premiere_analyse=True # Pour les sequences aleatoire, la sequence change a chaque fois donc l'analyse est toujours nouvelle.
				continue
			elif reponse=="3":
				reponse="Initialisation"
				compo=ap.composition(seq)
				seq_al=csa.seq_aleatoire(seq,compo) # Recupere une sequence de composition aleatoire de meme type et de meme longueur que "seq".
				description="_seq_aleatoire"
				sequence=seq_al # Ecrase "sequence" mais pas "seq" ce qui permet de garder en memoire la sequence de reference de chaque analyse dans la variable 'seq'
				premiere_analyse=True
				continue
			else :

#--------------Mise en reseau-----------------#
				con.sendall("\n---------------\nAttention : votre reponse ne correspond a aucune des propositions.\n\nVeuillez reconsiderer votre reponse.\n\nAttention : Relance du programme\n--------------\n \nPour relancer le programme sur une nouvelle sequence tapez 1\nPour faire la meme etude pour une sequence de meme composition tapez 2,\nPour faire la meme etude sur une sequence aleatoire tapez 3,\nPour arreter le programme tapez 4 :\n".encode())
				reponse=con.recv(1024).decode()
#---------------------------------------------#

				continue

#--------------Mise en reseau-----------------#
			if premiere_analyse:
				con.sendall((" \nL analyse de votre sequence a ete effectuee avec succes. \n \nPour relancer le programme sur une nouvelle sequence tapez 1\nPour faire la meme etude pour une sequence de meme composition tapez 2,\nPour faire la meme etude sur une sequence aleatoire tapez 3,\nPour arreter le programme tapez 4 :\n ".encode()))
			else:
				con.sendall("\nPour relancer le programme sur une nouvelle sequence tapez 1\nPour faire la meme etude pour une sequence de meme composition tapez 2,\nPour faire la meme etude sur une sequence aleatoire tapez 3,\nPour arreter le programme tapez 4 :\n ".encode())
			reponse=con.recv(1024).decode()
	con.sendall("\n---------------\nArret du programme\nVous etes deconnecte du serveur\n---------------\n".encode())
	con.shutdown(1)
	con.close()
#--------------------------------------------#
"""
