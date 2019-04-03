#!/usr/bin/python3

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Projet Python L3 BIM 2017
#                                                        Lecture de fichier fasta et de fiche fasta en ligne
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import urllib.request

def lire_fasta(fichier): # Recupere une sequence dans un fichier au format fasta place dans le meme dossier que ce module grace au nom complet du fichier.
    "Cette fonction permet de recuperer une sequence et sa description dans un fichier place dans le repertoire courant grace a son nom donne en argument (entre guillemets, sans oublier l'extension)."
    sequence=""
    lines=fichier.split("\n")
    description=lines[0]
    description=description[1:]
    for line in lines[1:]:
      line=line.strip() # Pour enlever d'éventuel espace en début ou fin de ligne
      sequence+=line
    return(description,sequence)



def recup_fasta_web(id_seq,type_seq):
	try:
		description,sequence=lire_fasta_web(id_seq,type_seq)
	except urllib.error.HTTPError : # Si le lien internet n'existe pas.
		error="\n----------------\nAttention : Le lien est introuvable\nVerifiez qu'il n'y a pas de faute de frappe\nou que vous n'avez pas oublie l'extention du fichier.Sinon verifiez que l'identifiant correspond bien a une sequence du type : %s eique.Veuillez modifiez vos entrees en consequence. \nAttention : Relance du programme\n---------------\n" %(type_seq)
		type_error=404
		return(error,type_error)
	except urllib.error.URLError : # Si la connexion internet ne fonctionne pas.
		error="\n----------------\nAttention : Impossible d'acceder a la base de donnees en ligne.\nVerifiez que vous avez bien une connnection internet active sur ce poste.\nAttention : Relance du programme\n---------------\n"
		type_error=503
		return(error,type_error)
	except UnicodeEncodeError : # Si l'identifiant contient des caracteres speciaux non reconnus (accents, guillemets...). 
		error="\n----------------\nAttention : L'identifiant entre est incorecte\nVerifiez qu'il n'y a pas de faute de frappe,d'espaces\nou que vous n'avez pas oublie l'extention du fichierVeuillez modifiez vos entrees en consequence.Attention : Relance du programme\n---------------\n"
		type_error=404
		return(error,type_error)
	if description=="La sequence n'est pas referencee.": # Le lien internet a mene a une page informant que la sequence demandee n'est pas referencee.
		error="\n----------------\nAttention : La sequence n'est pas referencee.\nVerifiez qu'il n'y a pas de faute de frappe dans le nom de la sequence.Sinon verifiez que l'identifiant correspond bien a une sequence du type : %s eique.Veuillez modifiez vos entrees en consequence. \nAttention : Relance du programme\n---------------\n" %(type_seq)
		type_error=404
		return(error,type_error)
	else :
		return(description,sequence)



def lire_fasta_web(adresse,type_seq): # Recupere une sequence fasta sur internet grace a son identifiant entre guillemets et au type de la sequence ("prot" ou "nucl").
    "Cette fonction permet de recuperer une sequence et sa decription dans une fiche fasta en ligne grace a son identifiant donne en premier argument et au type de sequence donne en deuxieme argument ('prot' ou 'nucl')."
    adresse=adresse.upper()
    if type_seq=="prot":
        url="http://www.uniprot.org/uniprot/"+adresse+".fasta"
    else:
        url="http://www.ebi.ac.uk/ena/data/view/"+adresse+"&display=fasta"
    u=urllib.request.urlopen(url) # Ouvre la page internet correspondant a l'url determine ci-dessus.
    sequence=""
    ligne=u.readline().strip().decode("utf8") # Enleve les eventuels espaces en debut et fin de chaine de caractere et decode la ligne internet qui est codee en "utf8".
    if ligne != "Entry: %s display type is either not supported or entry is not found." %adresse and ligne!="": 
        while ligne[0] != ">": 
            ligne=u.readline().strip().decode("utf8")             
        description=ligne[1:]
        while ligne != "":
            ligne=u.readline().strip().decode("utf8") 
            sequence=sequence+ligne
        u.close() # Referme la page internet ouverte. 
    else : # La page touvee indique que la sequence demandee n'est pas referencee ou introuvable.
        description="La sequence n'est pas referencee."
    return(description,sequence)

