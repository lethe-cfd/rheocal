# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 13:41:32 2022

@author: Bérénice
"""
from tkinter import *
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import sys



root = Tk()


######################################################################
###PART 2: Regression functions###

mod=select_mod.get()
#Importing data function
def readData(inputFile):
    data = np.loadtxt(inputFile, dtype=float, usecols = (0,1))
    eta=data[:,0]
    dgamma=data[:,1]
    return eta, dgamma

#Theoric model
def model(param,mod):
    eta=[]
    #Power Law model
    if mod==options[0]:
        m,n=param
        eta=m*dgammaE**(n-1)
    #Carreau-Yasuda model
    if mod==options[1]:
        etainf,etazero,lambd,a,n=param
        eta=(etazero-etainf)*(1+(lambd*dgammaE)**a)**((n-1)/a)+etainf
    return eta

#Least squares definition
def objective(param):
    return np.sum(((model(param,select_mod.get())-etaE)/etaE)**2)

##############################################################################
###PART 3: Printing results functions###


#Show results
def graph(mod,param,options, etaE,dgammaE,eta):
    print('Solution')
    #Printing Power law result parameters
    if mod==options[0]:
        print('m = ' + str(param[0]))
        print('n = ' + str(param[1]))
    #Printing Carreau-Yasuda result parameters  
    if mod==options[1]:
        print('etainf = ' + str(param[0]))
        print('etazero = ' + str(param[1]))
        print('lambd = ' + str(param[2]))
        print('a = ' + str(param[3]))
        print('n = ' + str(param[4]))

    # plot solution
    plt.figure(1)
    plt.yscale("log")
    plt.xscale("log")
    plt.plot(etaE,dgammaE,'bx')
    plt.plot(etaE,eta,'k-');
    plt.xlabel('dgamma')
    plt.ylabel('eta')
    plt.legend(['Measured','Predicted'],loc='best')
    plt.savefig('results.png')
    plt.show()



###############################################################################
###PART4: Main functions###

def main(mod):
    #Fetching experimental data
    #Model="CarreauYasuda"#DEMANDER NOM DE LA MÉTHODE UTILISATEUR
    [etaE,dgammaE]=readData("test1.txt")
    
    # initial guesses
    if mod==options[0]:
        param0=[98.025251,-0.03266]
    if mod==options[1]:
        param0=[385.4,0.0005,0.0004209,1.0730147,-250.4070]
    
    
    # optimize
    # bounds on variables
    bnds100 = (-300.0, 300.0)
    no_bnds = (-1.0e10, 1.0e10)
    if mod==options[0]:
        bnds = (no_bnds, no_bnds)
    if mod==options[1]:
        bnds = (no_bnds, no_bnds, no_bnds, no_bnds, bnds100)
    solution = minimize(objective,param0,method='SLSQP',bounds=bnds)
    param = solution.x
    eta = model(param,mod)
    
    graph(mod,param,options, etaE,dgammaE,eta)
    
def show():
    myLabel=label(root, text=select_mod.get()).pack()

#Rheology Model list of options
options=[
    "Power Law",
    "Carreau-Yasuda",
    "Cross"]

#User enters model
select_mod=StringVar()
select_mod.set(options[0])

choice = OptionMenu(root, select_mod,*options)
choice.pack()

root.mainloop()

#Run program after selection of model and file
myButton=Button(root,text="Run", command=main).pack()   