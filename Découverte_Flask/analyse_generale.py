#!/usr/bin/python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Projet Python 4BIM 2019
#                                                             Analyse de sequences nucleiques et proteiques
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import lire_fasta as lf
import analyse_sequence_fasta as asf

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
  else:
    fichier,error,type_error=asf.resultat_ADN(des,seq)
  return(fichier,error,type_error)
