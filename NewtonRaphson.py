# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:14:50 2022

@author: Bérénice
"""
import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
from statistiques import *
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

#Matrice R(x)
def R(yexp,param,law,dgammaE):
    eta=estimate(param,law,dgammaE)
    R=np.zeros(len(param))
    if law=="Power Law":
        R[0]=0
        R[1]=0
    if law=="CarreauYasuda":
        etainf,eta0,lamb,a,n=param
        R[0]=2*np.sum((yexp-eta)*(1+(dgammaE*lamb)**a)**((n-1)/a))
        R[1]=2*np.sum((yexp-eta)*(1-(1+(dgammaE*lamb)**a)**((n-1)/a)))
        R[2]=2*np.sum((yexp-eta)*(dgammaE**a*lamb**(a-1)*(eta0-etainf)*(n-1)*(1+(dgammaE*lamb)**a)**((n-1)/a)))
        R[3]=2*np.sum((yexp-eta)*(eta0-etainf)*((np.log(dgammaE*lamb)*(dgammaE*lamb)**a)/(a*((lamb*dgammaE)**a+1))-np.log((lamb*dgammaE)**a+1)/a**2)*((lamb*dgammaE)**a+1)**((n-1)/a))
        R[4]=2*np.sum((yexp-eta)*(eta0-etainf)/a*(np.exp((n-1)/a*np.log((dgammaE*lamb)**a+1))*np.log((dgammaE*lamb)**a+1)))
    return R

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

#%%

#Fetching experimental data
#nameFile= #DEMANDER NOM DU FICHIER UTILISATEUR?
models=[
        "Power Law",
        "CarreauYasuda",
        "Cross"]
law=models[1]#DEMANDER NOM DE LA MÉTHODE UTILISATEUR
[etaE,dgammaE]=readData("test2.txt")
yexp=etaE
#if dgammaE[1]<dgammaE[0]:
 #   dgammaE.reverse()
    
#Power Law model
if law==models[0]:
    param=np.zeros(2)
#Carreau-Yasuda model
if law==models[1]:
    #param=etainf,etazero,lambd,a,n
    param=np.zeros(5)

param0=guess(dgammaE,etaE,law)

tol=1e-04
n=0
N=100
dxn=np.ones(len(param),dtype=float)
param=param0
J=np.zeros((len(param),len(param)),dtype=float)
while la.norm(dxn)>tol and n<N:
    res=np.transpose(R(yexp,param,law,dgammaE))
    
    for i in range(len(param)):
        paramp=np.zeros(len(param))
        paramp[i]=tol*param[i]
        paramp=param+paramp
        rp=R(yexp,paramp,law,dgammaE)
        r=R(yexp,param,law,dgammaE)
        J[:,i]=(rp-r)/(tol*param[i])
    dxn=-np.dot(la.inv(J),res)
    param=param+0.2*dxn
    n=n+1
    close=yexp-estimate(param, law, dgammaE)

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
plt.title("NewtonRaphson fonctionne")
plt.ylim((ymin,max(etaE)+0.5*max(etaE)))
plt.legend(['Measured','Predicted'],loc='best')
plt.savefig('results.png')
plt.show()