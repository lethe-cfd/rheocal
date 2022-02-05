# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 13:03:15 2022

@author: Bérénice
"""

import scipy.integrate as integrate
from scipy.integrate import odeint
import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
import math as mt
import cmath
import sys


# Reading
def PLRdata(inputFile):  #Power Law read data
    data = np.loadtxt(inputFile, dtype=float, usecols = (0,1))    
    eta=[]
    gamma_dot=[]
    for line in range(len(data)): 
        gamma_dot.append(data[line,0])
        eta.append(data[line,1])
        #print(eta[line])
        #print(gamma_dot[line])
    return gamma_dot,eta


gamma_dot,eta=PLRdata("test1.txt")

# Visualize data
plt.figure(figsize = (10,8))
plt.plot(gamma_dot, eta, 'b.')
plt.xlabel(r'$gamma_dot$')
plt.ylabel(r'$eta$')
plt.show()


A = np.vstack([np.log(gamma_dot), np.ones(len(np.log(gamma_dot)))]).T
nm1, log_m = np.linalg.lstsq(A, np.log(eta), rcond = None)[0]
m = np.exp(log_m)
print(f'm={m}, nm1={nm1}')


# Let's have a look of the data
plt.figure(figsize = (10,8))
plt.plot(gamma_dot, eta, 'b.')
plt.plot(gamma_dot, m*gamma_dot**nm1, 'r-')
plt.xlabel('gamma_dot')
plt.ylabel('eta')
plt.title("Regression Power law linéarisée (données completes)")
plt.ylim([0,0.025])
plt.savefig('PL_lineaire_complet_part2.png',dpi=300,bbox_inches='tight') 
plt.show()