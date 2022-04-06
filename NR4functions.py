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

a=2.0

models=[
        "Power Law",
        "Carreau",
        "Cross",
        "autofit"]

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
        R[0]=np.sum((yexp-eta)/(yexp**2)*dgammaE**(n-1))
        R[1]=np.sum((yexp-eta)/(yexp**2)*m*dgammaE**(n-1)*np.log(dgammaE))
    if law==models[1]:
        etainf,eta0,lamb,n=param
        R[0]=np.sum((yexp-eta)/(yexp**2)*(1-(1+(dgammaE*lamb)**a)**((n-1)/a)))
        R[1]=np.sum((yexp-eta)/(yexp**2)*(1+(dgammaE*lamb)**a)**((n-1)/a))
        R[2]=np.sum((yexp-eta)/(yexp**2)*(dgammaE**a*lamb**(a-1)*(eta0-etainf)*(n-1)*(1+(dgammaE*lamb)**a)**((n-3)/a)))
        R[3]=np.sum((yexp-eta)/(yexp**2)*(eta0-etainf)/a*(np.exp((n-1)/a*np.log((dgammaE*lamb)**a+1))*np.log((dgammaE*lamb)**a+1)))
        etainf,eta0,alpha,m=param
    if law==models[2]:  
        etainf,eta0,alpha,m=param
        R[0]=np.sum((yexp-eta)/(yexp**2)*(1-(1/(1+(alpha*dgammaE)**m))))
        R[1]=np.sum((yexp-eta)/(yexp**2)*(1/(1+(alpha*dgammaE)**m)))
        R[2]=np.sum((yexp-eta)/(yexp**2)*((etainf-eta0)*m*dgammaE**m*alpha**(m-1))/(1+(alpha*dgammaE)**m)**2)
        R[3]=np.sum((yexp-eta)/(yexp**2)*((etainf-eta0)*np.log(alpha*dgammaE)*(alpha*dgammaE)**m)/(1+(alpha*dgammaE)**m)**2) 
    return R

# initial guesses
def guess(dgammaE,etaE,law):
    if law==models[0]:
    #param=[m,n]
    #    param0=[98.025251,-0.03266]
        param0=[80.0,0.05]
    if law==models[1]:
#       param0=[etainf,etazero,lambd,a,n]
        param0=[min(etaE),max(etaE),0.2,0.500000]
        #param0=[0.05,20,3,0.4]
        if mt.ceil(etaE[len(etaE)-1])>mt.ceil(etaE[len(etaE)-2]):
            param0[3]=1.5
            print("passé ici!")
        #if mt.ceil(etaE[len(etaE)-1])==mt.ceil(etaE[len(etaE)-2]):
        #    param0[0]=0
    #eta_inf zero vs existe
    if law==models[2]:
    #param=[m,n]
    #    param0=[98.025251,-0.03266]
        param0=[min(etaE),max(etaE),0.1,1.2]
    return param0

def regression(param0,law,dgammaE,yexp,tol,n):
    N=500
    x=param0
    dxn=np.ones(len(x),dtype=float)
    J=np.zeros((len(x),len(x)),dtype=float)
    while la.norm(dxn)>tol and n<N:
        theta=1
        res=np.transpose(R(yexp,x,law,dgammaE))
        
        for i in range(len(x)):
            xp=np.zeros(len(x))
            xp[i]=tol*x[i]
            xp=x+xp
            rp=R(yexp,xp,law,dgammaE)
            r=R(yexp,x,law,dgammaE)
            J[:,i]=(rp-r)/(tol*x[i])
        dxn=-np.dot(la.inv(J),res)

        while la.norm(R(yexp,x+theta*dxn,law,dgammaE))>la.norm(R(yexp,x,law,dgammaE)):
            theta=0.5*theta
        x=x+theta*dxn
        n=n+1
    return x,n
