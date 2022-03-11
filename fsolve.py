# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:56:01 2022
This method uses fsolve

@author: Bérénice
"""
from scipy.optimize import fsolve
from statistiques import *
import numpy as np
import matplotlib.pyplot as plt
import math as mt
import sys

#Importing data function
def readData(inputFile):
    data = np.loadtxt(inputFile, dtype=float, usecols = (0,1))
    dgammaE=data[:,0]
    etaE=data[:,1]
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


def func(param):
    eta = estimate(param,law,dgammaE)
    etainf,eta0,lamb,a,n=param
    eq1=np.sum((yexp-eta)*(1+(dgammaE*lamb)**a)**((n-1)/a))
    eq2=np.sum((yexp-eta)*(1-(1+(dgammaE*lamb)**a)**((n-1)/a)))
    eq3=np.sum((yexp-eta)*(dgammaE**a*lamb**(a-1)*(eta0-etainf)*(n-1)*(1+(dgammaE*lamb)**a)**((n-1)/a)))
    eq4=np.sum((yexp-eta)*(eta0-etainf)*((np.log(dgammaE*lamb)*(dgammaE*lamb)**a)/(a*((lamb*dgammaE)**a+1))-np.log((lamb*dgammaE)**a+1)/a**2)*((lamb*dgammaE)**a+1)**((n-1)/a))
    eq5=np.sum((yexp-eta)*(eta0-etainf)/a*(np.exp((n-1)/a*np.log((dgammaE*lamb)**a+1))*np.log((dgammaE*lamb)**a+1))) 
    return [eq1, eq2, eq3, eq4, eq5]

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

#%%
#Fetching experimental data
#nameFile= #DEMANDER NOM DU FICHIER UTILISATEUR?
models=[
        "Power Law",
        "CarreauYasuda",
        "Cross"]
law=models[1]#DEMANDER NOM DE LA MÉTHODE UTILISATEUR
[etaE,dgammaE]=readData("test2.txt")
if dgammaE[1]<dgammaE[0]:
    dgammaE=dgammaE[::-1]
    etaE=etaE[::-1]
    print("Order of data was inversed")
    
yexp=etaE    

param0=guess(dgammaE,etaE,law)
param=fsolve(func,param0)

dgamma=np.logspace(np.log10(min(dgammaE)),np.log10(max(dgammaE)),100)
eta = estimate(param,law,dgamma)
print(eta)
#graph=affichage(param,law,etaE,dgammaE)
#%%
# print solution
#def affichage(param,law,etaE,dgammaE):
print('Solution')
if law==models[0]:
    print('m = ' + str(param[0]))
    print('n = ' + str(param[1]))
if law==models[1]:
    print('etainf = ' + str(param[0]))
    print('etazero = ' + str(param[1]))
    print('lambd = ' + str(param[2]))
    print('a = ' + str(param[3]))
    print('n = ' + str(param[4]))

#Statistics report    
r2score(dgammaE,etaE,estimate(param,law,dgammaE))   

ymin=min(etaE)-0.5*min(etaE)
if min(eta)<ymin:
    ymin=min(eta)-0.5*min(eta)

# plot solution
plt.figure(1)
plt.plot(dgammaE,etaE,'bx')
plt.plot(dgamma,eta,'k-')
plt.yscale("log")
plt.xscale("log")
plt.xlabel('dgamma')
plt.ylabel('eta')
plt.ylim((ymin,max(etaE)+0.5*max(etaE)))
plt.legend(['Measured','Predicted'],loc='best')
plt.savefig('results.png')
plt.show()
    
