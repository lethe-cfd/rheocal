# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:56:01 2022
This method uses fsolve

@author: Bérénice
"""
from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt
import math as mt
import sys

a=2

def r2score(xexp,yexp,yreg):
    yavg=np.sum(yexp)/len(yexp)
    avg=yexp-yavg
    reg=yexp-yreg
    coeff=(np.sum(np.power(avg,2))-np.sum(np.power(reg,2)))/np.sum(np.power(avg,2))
    print('\nR2 = ')
    print(coeff)
    return coeff

#Importing data function
def readData(inputFile):
    data = np.loadtxt(inputFile, dtype=float, usecols = (0,1))
    dgammaE=data[:,0]
    etaE=data[:,1]
    return dgammaE, etaE

#Theoric model
def estimate(param,law,dgamma):
    eta=[]
    #Power Law model
    if law==models[0]:
        m,n=param
        eta=m*dgamma**(n-1)
    #Carreau model
    if law==models[1]:
        etainf,eta0,lambd,n=param
        eta=(eta0-etainf)*(1+(lambd*dgamma)**2)**((n-1)/2)+etainf
    #Cross model
    if law==models[2]:
        etainf,eta0,alpha,m=param
        eta=(eta0-etainf)/(1+(alpha*dgamma)**m)+etainf    
    return eta

def funcPow(param):
    eta = estimate(param,law,dgammaE)
    m,n=param
    eq1=np.sum((yexp-eta)*dgammaE**(n-1))
    eq2=np.sum((yexp-eta)*m*dgammaE**(n-1)*np.log(dgammaE))
    return [eq1, eq2]

def funcCar(param):
    eta = estimate(param,law,dgammaE)
    etainf,eta0,lamb,n=param
    eq1=np.sum((yexp-eta)*(1-(1+(dgammaE*lamb)**a)**((n-1)/a)))
    eq2=np.sum((yexp-eta)*(1+(dgammaE*lamb)**a)**((n-1)/a))
    eq3=np.sum((yexp-eta)*(dgammaE**a*lamb**(a-1)*(eta0-etainf)*(n-1)*(1+(dgammaE*lamb)**a)**((n-3)/a)))
    eq4=np.sum((yexp-eta)*(eta0-etainf)/a*(np.exp((n-1)/a*np.log((dgammaE*lamb)**a+1))*np.log((dgammaE*lamb)**a+1))) 
    return [eq1, eq2, eq3, eq4]

def funcCro(param):
    eta = estimate(param,law,dgammaE)
    etainf,eta0,alpha,m=param
    eq1=np.sum((yexp-eta)*(1-(1/(1+(alpha*dgammaE)**m))))
    eq2=np.sum((yexp-eta)*(1/(1+(alpha*dgammaE)**m)))
    eq3=np.sum((yexp-eta)*((etainf-eta0)*m*dgammaE**m*alpha**(m-1))/(1+(alpha*dgammaE)**m)**2)
    eq4=np.sum((yexp-eta)*((etainf-eta0)*np.log(alpha*dgammaE)*(alpha*dgammaE)**m)/(1+(alpha*dgammaE)**m)**2) 
    return [eq1, eq2, eq3, eq4]

#%%
#Fetching experimental data
#nameFile= #DEMANDER NOM DU FICHIER UTILISATEUR?
models=[
        "Power Law",
        "Carreau",
        "Cross"]
law=models[2]#DEMANDER NOM DE LA MÉTHODE UTILISATEUR
[dgammaE, etaE]=readData("test2.txt")

if dgammaE[1]<dgammaE[0]:
    dgammaE=dgammaE[::-1]
    etaE=etaE[::-1]
    print("Order of data was inversed")
    
yexp=etaE    
if law==models[0]:
    param0=[80,-0.9]
    param=fsolve(funcPow,param0)
elif law==models[1]:
    param0=[min(etaE),max(etaE),0.2,0.500000]
    param=fsolve(funcCar,param0)
elif law==models[2]:
    param0=[0.1,1.2,0.1,1.2]
    param=fsolve(funcCro,param0)

dgamma=np.logspace(np.log10(min(dgammaE)),np.log10(max(dgammaE)),100)
eta = estimate(param,law,dgamma)

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
    print('n = ' + str(param[3]))
if law==models[2]:
    print('etainf = ' + str(param[0]))
    print('etazero = ' + str(param[1]))
    print('alpha = ' + str(param[2]))
    print('m = ' + str(param[3]))

#Statistics report    
r2score(dgammaE,etaE,estimate(param,law,dgammaE))   

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
    
