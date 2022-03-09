# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:14:50 2022

@author: Bérénice
"""
#import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
from regTest2 import *


#Matrice R(x)
def R(yexp,param,law,dgammaE):
    eta=model(param,law,dgammaE)
    R=np.zeros(len(param))
    if law=="Power Law":
        R[0]=0
        R[1]=0
    if law=="Carreau-Yasuda":
        etainf,eta0,lamb,a,n=param
        R[0]=(yexp-eta)*(1+(dgammaE*lamb)**a)**((n-1)/a)
        R[1]=(yexp-eta)*(1-(1+(dgammaE*lamb)**a)**((n-1)/a))
        R[2]=(yexp-eta)*(dgammaE**a*lamb**(a-1)(eta0-etainf)*(n-1)*(1+(dgammaE*lamb)**a)**((n-1)/a))
        R[3]=(yexp-eta)*(eta0-etainf)*((np.log(dgammaE*lamb)*(dgammaE*lamb)**a)/(a*((lamb*dgammaE)**a+1))-np.log((lamb*dgammaE)**a+1)/a**2)*((lamb*dgammaE)**a+1)**((n-1)/a)
        R[4]=(yexp-eta)*(eta0-etainf)/a*(exp((n-1)/a*np.log((dgammaE*lamb)**a+1))*np.log((dgammaE*lamb)**a+1))
    return R

def J(yexp,param,law,dgammaE):
    J=np.zeros((len(param),len(param)))
    
    return J