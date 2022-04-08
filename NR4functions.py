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
        "Cross"]

def r2score(yexp,yreg):
    print(np.sum(abs((yexp-yreg)/yexp)))
    meanerror=np.sum(abs((yexp-yreg)/yexp))/len(yexp)
    print(meanerror)
  
    yavg=np.sum(yexp)/len(yexp)
    avg=(yexp-yavg)
    reg=(yexp-yreg)
    R2=(np.sum(np.power(avg,2))-np.sum(np.power(reg,2)))/np.sum(np.power(avg,2))  
    return R2,meanerror


def readData(inputFile):
    data = np.loadtxt(inputFile, dtype=float, usecols = (0,1))
    dgammaE=data[:,0]
    etaE=data[:,1]
    return etaE, dgammaE

def estimate(param,law,dgamma):
    """
    evaluate the viscosity according to a rheology law for a shear rate vector
    Inputs:
    - param: rheology model parameters
    - law: rheology model
    - dgamma: shear rate vector
    Output
    eta: viscosity
    """
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
    if law==models[2]:  
        etainf,eta0,alpha,m=param
        R[0]=np.sum((yexp-eta)/(yexp**2)*(1-(1/(1+(alpha*dgammaE)**m))))
        R[1]=np.sum((yexp-eta)/(yexp**2)*(1/(1+(alpha*dgammaE)**m)))
        R[2]=np.sum((yexp-eta)/(yexp**2)*((etainf-eta0)*m*dgammaE**m*alpha**(m-1))/(1+(alpha*dgammaE)**m)**2)
        R[3]=np.sum((yexp-eta)/(yexp**2)*((etainf-eta0)*np.log(alpha*dgammaE)*(alpha*dgammaE)**m)/(1+(alpha*dgammaE)**m)**2) 
    return R

def regression(param0,law,dgammaE,yexp,tol,n,theta):
    N=500
    x=param0
    dxn=np.ones(len(x),dtype=float)
    J=np.zeros((len(x),len(x)),dtype=float)
    while la.norm(dxn)>tol and n<N:
        relaxation=False
        theta=1
        res=np.transpose(R(yexp,x,law,dgammaE))
        
        for i in range(len(x)):
            xp=np.zeros(len(x))
            xp[i]=0.0001*x[i]
            xp=x+xp
            rp=R(yexp,xp,law,dgammaE)
            r=R(yexp,x,law,dgammaE)
            J[:,i]=(rp-r)/(tol*x[i])
        dxn=-np.dot(la.inv(J),res)
        
        try:
            relaxation=la.norm(R(yexp,x+theta*dxn,law,dgammaE))>la.norm(R(yexp,x,law,dgammaE))
        except:
            relaxation=True
        while relaxation: 
            theta=0.5*theta
            relaxation=la.norm(R(yexp,x+theta*dxn,law,dgammaE))>la.norm(R(yexp,x,law,dgammaE))
        x=x+theta*dxn
        n=n+1
    return x,n,theta
