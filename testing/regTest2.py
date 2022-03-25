# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:56:01 2022

@author: Bérénice
"""
#import scipy.integrate as integrate
#from scipy.integrate import odeint
from scipy.optimize import minimize
from scipy.optimize import least_squares
from scipy.optimize import curve_fit
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

# def CarYas(dgamma,etainf,etazero,lambd,a,n):
#     eta=(etazero-etainf)*(1+(lambd*dgamma)**a)**((n-1)/a)+etainf
#     return eta

#Least squares definition
def objective(param):
    return np.sum(((estimate(param,law,dgammaE)-etaE)/etaE)**2)
#    return np.log(estimate(param,law,dgammaE))-np.log(etaE)
#    return estimate(param,law,dgammaE)-etaE



# initial guesses
def guess(dgammaE,etaE,law):
    if law==models[0]:
    #param=[m,n]
    #    param0=[98.025251,-0.03266]
        param0=[1.0,0.05]
    if law==models[1]:
#        param0=[0.0005,385.4000,0.0004209,1.0730147,-250.4070]
#        etazero=max(etaE)
#        etainf=0
#        lamb=1/
        param0=[min(etaE),max(etaE),0.00050,1.07000,-0.500000]
#        param0=[etainf,etazero,lambd,a,n]
        #if 
    #eta_inf zero vs existe
    return param0

#%%
#Fetching experimental data
#nameFile= #DEMANDER NOM DU FICHIER UTILISATEUR?
models=[
        "Power Law",
        "CarreauYasuda",
        "Cross"]
law=models[1]#DEMANDER NOM DE LA MÉTHODE UTILISATEUR
[etaE,dgammaE]=readData("test3.txt")
#if dgammaE[1]<dgammaE[0]:
 #   dgammaE.reverse()
    

# optimize
# bounds on variables
bnds0 = (0.0, 1.0e3)
no_bnds = (-1.0e10, 1.0e10)
if law==models[0]:
    bnds = (no_bnds, no_bnds)
 #   bnds = (bnds0, bnds0)
if law==models[1]:
    bnds = (bnds0, bnds0, bnds0, bnds0, no_bnds)
param0=guess(dgammaE,etaE,law)

solution = minimize(objective,param0,method='SLSQP',bounds=bnds)
#solution = least_squares(objective,param0)
#solution, cov=curve_fit(CarYas,dgammaE,etaE,param0,bounds=[0,1.0e10])
param = solution.x

dgamma=np.logspace(np.log10(min(dgammaE)),np.log10(max(dgammaE)),100)
eta = estimate(param,law,dgamma)
print(eta)
#%%
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
    
