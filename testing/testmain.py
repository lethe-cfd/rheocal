# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 16:53:08 2022

@author: Bérénice
"""

from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from tkinter import *
import numpy as np
import math as mt

import sys

    
#Importing data function
def readData(inputFile):
    data = np.loadtxt(inputFile, dtype=float, usecols = (0,1))
    dgammaE=data[:,0]
    etaE=data[:,1]
    #if data in the wrong order:
    if dgammaE[1]<dgammaE[0]:
        dgammaE=dgammaE[::-1]
        etaE=etaE[::-1]
    return etaE, dgammaE


#Theoric model
def estimate(param,law,dgamma):
    eta=[]
    #Power Law model
    if law==models[0]:
        m,n=param
        eta=m*dgamma**(n-1)
    #Carreau-Yasuda model
    if law==models[1]:
        etainf,etazero,lambd,a,n=param
        eta=(etazero-etainf)*(1+(lambd*dgamma)**a)**((n-1)/a)+etainf
    return eta


# initial guesses
def guess(dgammaE,etaE,law):
    if law==models[0]:
    #param=[m,n]
    #    param0=[98.025251,-0.03266]
        param0=[1.0,0.05]
    if law==models[1]:
#       param0=[etainf,etazero,lambd,a,n]
        param0=[min(etaE),max(etaE),0.2,2.0,0.500000]
        if mt.ceil(etaE[len(etaE)-1])>mt.ceil(etaE[len(etaE)-2]):
            param0[4]=1.5
            print("passé ici!")
        #if mt.ceil(etaE[len(etaE)-1])==mt.ceil(etaE[len(etaE)-2]):
        #    param0[0]=0
    #eta_inf zero vs existe
    return param0

def bounds(dgammaE,etaE,law):
    # bounds on variables
    bnds0 = (0.0, 1.0e3)
    no_bnds = (-1.0e10, 1.0e10)
    if law==models[0]:
        bnds = (no_bnds, no_bnds)
     #   bnds = (bnds0, bnds0)
    if law==models[1]:
        bnds = (bnds0, bnds0, bnds0, bnds0, no_bnds)
    return bnds

def r2score(xexp,yexp,yreg):
    yavg=np.sum(yexp)/len(yexp)
    avg=yexp-yavg
    reg=yexp-yreg
    coeff=(np.sum(np.power(avg,2))-np.sum(np.power(reg,2)))/np.sum(np.power(avg,2))
    print('\nR2 = ')
    print(coeff)
    return coeff

#%%
#Fetching experimental data
#nameFile= #DEMANDER NOM DU FICHIER UTILISATEUR?
models=[
        "Power Law",
        "Carreau-Yasuda",
        "Cross"]
law=models[1]#DEMANDER NOM DE LA MÉTHODE UTILISATEUR


    