# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:56:01 2022

@author: Bérénice
"""
#import scipy.integrate as integrate
#from scipy.integrate import odeint
from scipy.optimize import minimize
from statistiques import *
#import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
#import math as mt
#import cmath
import sys

#Importing data function
def readData(inputFile):
    data = np.loadtxt(inputFile, dtype=float, usecols = (0,1))
    dgammaE=data[:,0]
    etaE=data[:,1]
    return etaE, dgammaE

#Theoric model
def model(param,law,dgamma):
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


#Least squares definition
def objective(param):
    return np.sum(((model(param,law,dgammaE)-etaE)/etaE)**2)


#Fetching experimental data
#nameFile= #DEMANDER NOM DU FICHIER UTILISATEUR?
models=[
        "Power Law",
        "CarreauYasuda"
        "Cross"]
law=models[1]#DEMANDER NOM DE LA MÉTHODE UTILISATEUR
[etaE,dgammaE]=readData("test1.txt")

# initial guesses
if law==models[0]:
    param0=[98.025251,-0.03266]
if law==models[1]:
#    param0=[0.0005,385.4000,0.0004209,1.0730147,-250.4070]
    param0=[etaE[len(etaE)-1],etaE[0],0.0005000,1.0600000,-251.000000]

# optimize
# bounds on variables
bnds0 = (0.0, 1.0e3)
no_bnds = (-1.0e10, 1.0e10)
if law==models[0]:
    bnds = (no_bnds, no_bnds)
if law==models[1]:
    bnds = (bnds0, bnds0, bnds0, bnds0, no_bnds)
solution = minimize(objective,param0,method='SLSQP',bounds=bnds)
#print(solution)
param = solution.x
#print(param)
#x=np.linspace(dgammaE[len(dgammaE)-1],dgammaE[0],300)
#print(dgammaE)
#print(x)
dgamma=np.linspace(dgammaE[0],dgammaE[len(dgammaE)-1],100)
eta = model(param,law,dgamma)
#print(eta)

#############################################################################
###PRINTING RESULTS###
# show final objective
#print('Final SSE Objective: ' + str(objective(param)))

# print solution
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
r2score(dgammaE,etaE,model(param,law,dgammaE))   

# plot solution
plt.figure(1)
plt.plot(dgammaE,etaE,'bx')
plt.plot(dgamma,eta,'k-')
plt.yscale("log")
plt.xscale("log")
plt.xlabel('dgamma')
plt.ylabel('eta')
plt.legend(['Measured','Predicted'],loc='best')
plt.savefig('results.png')
plt.show()
    
