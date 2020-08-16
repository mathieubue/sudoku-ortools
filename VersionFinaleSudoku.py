# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:48:51 2020

@author: M BUE
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import random
from ortools.sat.python import cp_model

def ElementsCases(cases):
    elementsCases = []
    e=[]
    for i in range(9):
        for j in range(3):
            e.extend(cases[i][j])
        elementsCases.append(e)
        e=[]
    return elementsCases

def CreationLignes(cases):
    lignes=[]
    e = []
    for numligne in range(9):
        e.extend(cases[(numligne//3)*3][numligne%3])
        e.extend(cases[(numligne//3)*3+1][numligne%3])
        e.extend(cases[(numligne//3)*3+2][numligne%3])
        lignes.append(e)
        e=[]
    return lignes

def ListeValeursNonNulles(lignes):
    mat=[]
    for i in range(9):
        e1=[]
        for j in range(9):
            if(lignes[i][j]!=None):
                e1.append(lignes[i][j])
        mat.append(e1)
    return mat

def CreationColonnes(lignes):
    colonnes=[]
    e=[]
    for j in range(0,len(lignes)):
        for i in range(0,len(lignes[j])):
            e.append(lignes[i][j])
        colonnes.append(e)
        e=[]
    return colonnes

def CreationValeur(model, nbvaleur, liste):
    for i in range(nbvaleur):
        ligne = random.randint(1,9)
        colonne = random.randint(1,9)
        liste[((ligne-1)//3)*3+((colonne-1)//3)][(ligne-1)%3][(colonne-1)%3] = model.NewIntVar(1,9,'A%s'%(i))
        
## Creation d'une grille initialisée

def CreationGrille(nbvaleurs):
    
    model = cp_model.CpModel()
    
    #On crée la grille a partir des cases (9 cases de 3 lignes par 3 colonnes)
    cases =[]
    C=[]
    L=[]
    for i in range(9):
        m=1
        for j  in range(3):
            for k in range(3):   
                L.append(None)
                m=m+1
            C.append(L)
            L=[]
        cases.append(C)
        C=[]
        
    #A partir de la matrice cases vide(avec des None) on attribue une valeur  aléatoire à une case aléatoire
    CreationValeur(model,nbvaleurs,cases)
    
    #On crée differentes matrices a partir des cases
    lignes = CreationLignes(cases)
    colonnes = CreationColonnes(lignes)
    elementsCases = ElementsCases(cases)
    
    #on extrait les valeurs non nulles dans chaque matrice / ligne et colonne 
    lignesValeurs = ListeValeursNonNulles(lignes)
    colonnesValeurs = ListeValeursNonNulles(colonnes)
    elementsCasesValeurs = ListeValeursNonNulles(elementsCases)
    
    #Contraintes
    #on verifie que les conditions de validité d'un sudoku sont respectées
    for i in range(len(lignesValeurs)):
        model.AddAllDifferent(lignesValeurs[i])
    for i in range(len(colonnesValeurs)):
        model.AddAllDifferent(colonnesValeurs[i])
    for i in range(len(elementsCasesValeurs)):
        model.AddAllDifferent(elementsCasesValeurs[i])   
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.FEASIBLE:
        print('Grille générée :')
        print(' ')
        for i in range(len(lignes)):
            for j in range(len(lignes[i])):
                if(lignes[i][j]==None):
                    print('_', end=' ')
                else:
                    print(str(solver.Value(lignes[i][j])),end=' ')
            print('\n') 
            
    #Matrice des cases avec les valeurs trouvées 
    res=[]
    for i in range(9):
        e1=[]
        for j in range(3):
            e2=[]
            for k in range(3):
                if(cases[i][j][k]==None):
                    e2.append(None)
                else:
                    e2.append(solver.Value(cases[i][j][k]))
            e1.append(e2)
        res.append(e1)
                    
        
    return res       

def ProgrammeGrille(cases):
    model = cp_model.CpModel()
    
    #Initialisation des variables
    for i in range(9):
        for j in range(3):
            for k in range(3):
                if(cases[i][j][k]==None):
                    cases[i][j][k]=model.NewIntVar(1,9,"v%s%s%s"%(i+1,j+1,k+1))
    

    #Initialisation des matrices
    lignes = CreationLignes(cases)
    colonnes = CreationColonnes(lignes)
    elementsCases = ElementsCases(cases)
    
    
    #Contraintes
    for i in range(9):
        model.AddAllDifferent(lignes[i])
        model.AddAllDifferent(colonnes[i])
        model.AddAllDifferent(elementsCases[i])
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.FEASIBLE:
        print('Grille résolue :')
        print(' ')
        for i in range(len(lignes)):
            for j in range(len(lignes[i])):
                    print(str(solver.Value(lignes[i][j])),end=' ')
            print('\n')    
  
ProgrammeGrille(CreationGrille(15))