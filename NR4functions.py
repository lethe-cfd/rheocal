# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:14:50 2022

#Newton Raphson 4 parameter regression functions

@author: Bérénice
"""
import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt


#List of rheology models, must be identical to the one in "rheocal.py"
models=[
        "Power Law",
        "Carreau",
        "Cross"]

def readData(inputFile):
    """
    Retrieve the two first column on the left of a file
    Inputs:
        - .txt or .csv file (comma separated)
    Outputs:
        - dgammaE: shear rate values (float)
        - etaE: viscosity values (float)
    """
    extension=inputFile.split(".")
    #Comma separated csv file
    if extension[1]=="csv":
        data = np.loadtxt(inputFile, delimiter=',', dtype=float, usecols = (0,1))
    #txt file
    elif extension[1]=="txt":
        data = np.loadtxt(inputFile, dtype=float, usecols = (0,1))
    dgammaE=data[:,0]
    etaE=data[:,1]
    return dgammaE,etaE

def r2score(yexp,yreg):
    """
    Calculate R2 score and mean error in percentage
    Inputs:
        - yexp: viscosity data from initial input file
        - yreg: viscosity found after regression
    Outputs:
        - R2: determination coefficient
        - meanerror: mean error of yreg compared to yexp in percentage
    """
    #R2 calcul
    yavg=np.sum(yexp)/len(yexp)
    avg=(yexp-yavg)
    reg=(yexp-yreg)
    R2=(np.sum(np.power(avg,2))-np.sum(np.power(reg,2)))/np.sum(np.power(avg,2))  
    
    #meanerror calcul
    meanerror=np.sum(abs((yexp-yreg)/yexp))/len(yexp)
    return R2,meanerror

def figure_opt(subplot):
    """
    Set the visual options of a matplotlib subplot
        * logarithmic scale in x and y, shear rate and viscosity labels, autoscale
    Inputs:
        - subplot: subplot on which options are applied
    """
    #Adjust graph display
    subplot.set_yscale("log")
    subplot.set_xscale("log")
    subplot.set_xlabel("$\dot \gamma [1/s]$")
    subplot.set_ylabel("$\eta [Pa \cdot s]$")
    subplot.autoscale(enable=True, axis='both')

def estimate(param,law,dgamma):
    """
    Evaluate the viscosity according to a rheology law for a shear rate vector
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
    #Carreau model (Carreau-Yasuda with a=2)
    if law==models[1]:
        etainf,etazero,lambd,n=param
        eta=(etazero-etainf)*(1+(lambd*dgamma)**2)**((n-1)/2)+etainf
    #Cross model
    if law==models[2]:
        etainf,eta0,alpha,m=param
        eta=(eta0-etainf)/(1+(alpha*dgamma)**m)+etainf  
    return eta


def R(etaE,param,law,dgammaE):
    """
    Evaluate the equation system derived from the sum of relative square error
    If R is the zero vector, minimum of the relative error function is found and regression is done
        * Partial derives in the same order than parameters are read
    Inputs:
        - etaE: viscosity data from initial input file
        - param: current value for model parameters
        - law: chosen rheology model
        - dgammaE: shear rate data from initial input file 
    Output
    R: Analytic partial derivatives of relative square error function
    """
    #Evaluate the viscosity value with current parameter valuers
    eta=estimate(param,law,dgammaE)
    #Initializing the Residual vector
    R=np.zeros(len(param))
    #Power Law
    if law==models[0]:
        m,n=param
        R[0]=np.sum((eta-etaE)/(etaE**2)*dgammaE**(n-1))
        R[1]=np.sum((eta-etaE)/(etaE**2)*m*dgammaE**(n-1)*np.log(dgammaE))
    #Carreau Model (Carreau-Yasuda with a=2)
    if law==models[1]:
        etainf,eta0,lamb,n=param
        R[0]=np.sum((eta-etaE)/(etaE**2)*(1-(1+(dgammaE*lamb)**2)**((n-1)/2)))
        R[1]=np.sum((eta-etaE)/(etaE**2)*(1+(dgammaE*lamb)**2)**((n-1)/2))
        R[2]=np.sum((eta-etaE)/(etaE**2)*dgammaE**2*lamb*(eta0-etainf)*(n-1)*(1+(dgammaE*lamb)**2)**((n-3)/2))
        R[3]=np.sum((eta-etaE)/(etaE**2)*(eta0-etainf)/2*(1+(dgammaE*lamb)**2)**((n-1)/2)*np.log((dgammaE*lamb)**2+1))
    #Cross
    if law==models[2]:  
        etainf,eta0,alpha,m=param
        R[0]=np.sum((eta-etaE)/(etaE**2)*(1-(1/(1+(alpha*dgammaE)**m))))
        R[1]=np.sum((eta-etaE)/(etaE**2)*(1/(1+(alpha*dgammaE)**m)))
        R[2]=np.sum((eta-etaE)/(etaE**2)*((etainf-eta0)*m*dgammaE**m*alpha**(m-1))/(1+(alpha*dgammaE)**m)**2)
        R[3]=np.sum((eta-etaE)/(etaE**2)*((etainf-eta0)*np.log(alpha*dgammaE)*(alpha*dgammaE)**m)/(1+(alpha*dgammaE)**m)**2) 
    return R


def newton_solve(param0,law,dgammaE,yexp,tol,n,theta):
    """
    Solve a non-linear equation system by the Newton Raphson method with numerical jacobian matrix
    Inputs:
        - param0: Initial guess on parameters
        - law: chosen rheology model
        - dgammaE: shear rate data from initial input file 
        - yexp: viscosity data from initial input file 
        - tol: tolerance on residual matrix R
        - n: counter for the number of iterations performed
        - theta: relaxation factor (input should be a value of 1)
    Output:
        - x: final value of parameters
        - n: number of iterations performed
        - theta: final value of relaxation factor
    """
    N=500 #max number of iterations
    x=param0 #initialize parameter value
    #initialize matrices
    dxn=np.ones(len(x),dtype=float)
    jac=np.zeros((len(x),len(x)),dtype=float)
    disturb=0.0001
    res=np.transpose(R(yexp,x,law,dgammaE))
    while la.norm(dxn)>tol and n<N:
        #Initialize relaxation parameters
        relaxation=False
        theta=1
        #Current value of residual matrix
        res=np.transpose(R(yexp,x,law,dgammaE))
        #Numerical Jacobian matrix calcul
        for i in range(len(x)):
            xd=np.zeros(len(x))
            xd[i]=disturb*x[i]
            xd=x+xd
            rd=R(yexp,xd,law,dgammaE)
            r=R(yexp,x,law,dgammaE)
            jac[:,i]=(rd-r)/(disturb*x[i])

        #Solve system to find step to add on the parameter values
        dxn=la.solve(jac,-res)      
        try:
            # print("R(x+dxn)", R(yexp,x+theta*dxn,law,dgammaE))
            # print("R(x)", R(yexp,x,law,dgammaE))  
            relaxation=la.norm(R(yexp,x+theta*dxn,law,dgammaE))>la.norm(R(yexp,x,law,dgammaE))
        except:
            relaxation=True
        while relaxation: 
            theta=0.5*theta
            relaxation=la.norm(R(yexp,x+theta*dxn,law,dgammaE))>la.norm(R(yexp,x,law,dgammaE))
        # print("theta",theta)
        # print("R(x+dxn)", R(yexp,x+theta*dxn,law,dgammaE))
        # print("R(x)", R(yexp,x,law,dgammaE))
       #new value on parameters
        x=x+theta*dxn
        n=n+1
    return x,n,theta


