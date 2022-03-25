# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:14:50 2022

#Newton Raphson 4 parameter regression functions

@author: Bérénice
"""
import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
import math as mt
import sys
import os
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image

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
        etainf,etazero,lambd,n=param
        eta=(etazero-etainf)*(1+(lambd*dgamma)**a)**((n-1)/a)+etainf
    #Cross model
    if law==models[2]:
        etainf,eta0,alpha,m=param
        eta=(eta0-etainf)/(1+(alpha*dgamma)**m)+etainf  
    return eta

#Matrice R(x)
def R(yexp,param,law,dgammaE):
    eta=estimate(param,law,dgammaE)
    R=np.zeros(len(param))
    if law==models[0]:
        m,n=param
        R[0]=np.sum((yexp-eta)*dgammaE**(n-1))
        R[1]=np.sum((yexp-eta)*m*dgammaE**(n-1)*np.log(dgammaE))
    if law==models[1]:
        etainf,eta0,lamb,n=param
        R[0]=np.sum((yexp-eta)*(1-(1+(dgammaE*lamb)**a)**((n-1)/a)))
        R[1]=np.sum((yexp-eta)*(1+(dgammaE*lamb)**a)**((n-1)/a))
        R[2]=np.sum((yexp-eta)*(dgammaE**a*lamb**(a-1)*(eta0-etainf)*(n-1)*(1+(dgammaE*lamb)**a)**((n-3)/a)))
        R[3]=np.sum((yexp-eta)*(eta0-etainf)/a*(np.exp((n-1)/a*np.log((dgammaE*lamb)**a+1))*np.log((dgammaE*lamb)**a+1)))
        etainf,eta0,alpha,m=param
    if law==models[2]:  
        etainf,eta0,alpha,m=param
        R[0]=np.sum((yexp-eta)*(1-(1/(1+(alpha*dgammaE)**m))))
        R[1]=np.sum((yexp-eta)*(1/(1+(alpha*dgammaE)**m)))
        R[2]=np.sum((yexp-eta)*((etainf-eta0)*m*dgammaE**m*alpha**(m-1))/(1+(alpha*dgammaE)**m)**2)
        R[3]=np.sum((yexp-eta)*((etainf-eta0)*np.log(alpha*dgammaE)*(alpha*dgammaE)**m)/(1+(alpha*dgammaE)**m)**2) 
    return R

# initial guesses
def guess(dgammaE,etaE,law):
    if law==models[0]:
    #param=[m,n]
    #    param0=[98.025251,-0.03266]
        param0=[1.0,0.05]
    if law==models[1]:
#       param0=[etainf,etazero,lambd,a,n]
        param0=[min(etaE),max(etaE),0.2,0.500000]
        if mt.ceil(etaE[len(etaE)-1])>mt.ceil(etaE[len(etaE)-2]):
            param0[3]=1.5
            print("passé ici!")
        #if mt.ceil(etaE[len(etaE)-1])==mt.ceil(etaE[len(etaE)-2]):
        #    param0[0]=0
    #eta_inf zero vs existe
    if law==models[2]:
    #param=[m,n]
    #    param0=[98.025251,-0.03266]
        param0=[0.1,1.2,0.1,1.2]
    return param0

# #%%

# #Fetching experimental data
# #nameFile= #DEMANDER NOM DU FICHIER UTILISATEUR?
models=[
        "Power Law",
        "Carreau",
        "Cross"]
# law=models[1]#DEMANDER NOM DE LA MÉTHODE UTILISATEUR
# [etaE,dgammaE]=readData("test3.txt")
# yexp=etaE
# if dgammaE[1]<dgammaE[0]:
#     dgammaE=dgammaE[::-1]
#     etaE=etaE[::-1]
#     print("Order of data was inversed")
    
# #Power Law model
# if law==models[0]:
#     param=np.zeros(2)
# #Carreau-Yasuda model
# if law==models[1]:
#     #param=etainf,etazero,lambd,a,n
#     param=np.zeros(4)
# if law==models[2]:
#     #param=etainf,etazero,lambd,a,n
#     param=np.zeros(4)
# param0=[min(etaE),max(etaE),0.2,0.500000]


# param0=guess(dgammaE,etaE,law)
# print(param0)
def regression(param0,law,dgammaE,yexp):
    tol=1e-04
    n=0
    N=100
    x=param0
    dxn=np.ones(len(x),dtype=float)
    J=np.zeros((len(x),len(x)),dtype=float)
    while la.norm(dxn)>tol and n<N:
        res=np.transpose(R(yexp,x,law,dgammaE))
        
        for i in range(len(x)):
            xp=np.zeros(len(x))
            xp[i]=tol*x[i]
            xp=x+xp
            rp=R(yexp,xp,law,dgammaE)
            r=R(yexp,x,law,dgammaE)
            J[:,i]=(rp-r)/(tol*x[i])
        dxn=-np.dot(la.inv(J),res)
        x=x+0.2*dxn
        n=n+1
    return x


# param= regression(param0,law,dgammaE,etaE)

# dgamma=np.logspace(np.log10(min(dgammaE)),np.log10(max(dgammaE)),100)
# eta = estimate(param,law,dgamma)


# #%%
# ###PRINTING RESULTS###
# # show final objective
# #print('Final SSE Objective: ' + str(objective(param)))

# # print solution
# print('Solution')
# if law==models[0]:
#     print('m = ' + str(param[0]))
#     print('n = ' + str(param[1]))
# if law==models[1]:
#     print('etainf = ' + str(param[0]))
#     print('etazero = ' + str(param[1]))
#     print('lambd = ' + str(param[2]))
#     print('a = ' + str(a))
#     print('n = ' + str(param[3]))
# if law==models[2]:
#     print('etainf = ' + str(param[0]))
#     print('etazero = ' + str(param[1]))
#     print('alpha = ' + str(param[2]))
#     print('a = ' + str(a))
#     print('n = ' + str(param[3]))

# #Statistics report    
# r2score(dgammaE,etaE,estimate(param,law,dgammaE))   

# # plot solution
# plt.figure(1)
# plt.plot(dgammaE,etaE,'bx')
# plt.plot(dgamma,eta,'k-')
# plt.yscale("log")
# plt.xscale("log")
# plt.xlabel('dgamma')
# plt.ylabel('eta')
# plt.title("NewtonRaphson")
# plt.legend(['Measured','Predicted'],loc='best')
# plt.savefig('results.png')
# plt.show()




# def NewRaph(param,dgammaE,etaE,law):
#     tol=1e-04
#     n=0
#     N=100
#     dxn=np.ones(len(param),dtype=float)
#     param=param0
#     J=np.zeros((len(param),len(param)),dtype=float)
#     while la.norm(dxn)>tol and n<N:
#         res=np.transpose(R(yexp,param,law,dgammaE))
        
#         for i in range(len(param)):
#             paramp=np.zeros(len(param))
#             paramp[i]=tol*param[i]
#             paramp=param+paramp
#             rp=R(yexp,paramp,law,dgammaE)
#             r=R(yexp,param,law,dgammaE)
#             J[:,i]=(rp-r)/(tol*param[i])
#         dxn=-np.dot(la.inv(J),res)
#         param=param+0.2*dxn
#         n=n+1
#         close=yexp-estimate(param, law, dgammaE)
#     return param