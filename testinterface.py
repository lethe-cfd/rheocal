# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 13:41:32 2022

@author: Bérénice
"""
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from statistiques import *
import sys
import os
from testmain import *



root = Tk()
root.title('Rheocal: Rheology model regression!')    
root.geometry("800x400")
#Entry data frame
frame= LabelFrame(root, text="Select parameters", padx=20,pady=20)
frame.grid(row=0,column=0,padx=10,pady=10)

#Rheology Model list of options
options=[
    "Power Law",
    "Carreau-Yasuda",
    "Cross",
    "autofit"]

filename="test2.txt"
[etaE,dgammaE]=readData(filename) 
param0=guess(dgammaE,etaE,law)
yexp=etaE

#User enters model
select_mod=StringVar()
select_mod.set(options[0])

choice = OptionMenu(frame, select_mod,*options)
choice.grid(row=0, column=0) 

#root.filename=filedialog.askopenfilename(initialdir="C:/Users/Bérénice/OneDrive/Documents/GitHub/rheocal",title="Select the file of data to which we want to fit a curve",filetypes=(("txt files","*.txt"))) 

#%%
# print solution
def graph(param,law,etaE,dgammaE):
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
    #Regression curve data:
    dgamma=np.logspace(np.log10(min(dgammaE)),np.log10(max(dgammaE)),100)
    eta = estimate(param,law,dgamma)
    
    # plot solution
    f=plt.figure(figsize=(7,7))
    reg=f.add_subplot(111)
    reg.plot(dgammaE,etaE,'gx')
    reg.plot(dgamma,eta,'k-')
    reg.set_yscale("log")
    reg.set_xscale("log")
    reg.xlabel('dgamma')
    reg.ylabel('eta')
    reg.title("Carreau-Yasuda Regression")
    reg.legend(['Measured','Predicted'],loc='best')
    reg.savefig("results"+filename+".png")
    
    canvas=FigureCanvasTkAgg(f,self)
    canvas.show()
    canvas.get_tk_widget().grid(row=0,column=1)
    
#%%    
def func(param):
    eta = estimate(param,law,dgammaE)
    etainf,eta0,lamb,a,n=param
    eq1=np.sum((yexp-eta)*(1+(dgammaE*lamb)**a)**((n-1)/a))
    eq2=np.sum((yexp-eta)*(1-(1+(dgammaE*lamb)**a)**((n-1)/a)))
    eq3=np.sum((yexp-eta)*(dgammaE**a*lamb**(a-1)*(eta0-etainf)*(n-1)*(1+(dgammaE*lamb)**a)**((n-1)/a)))
    eq4=np.sum((yexp-eta)*(eta0-etainf)*((np.log(dgammaE*lamb)*(dgammaE*lamb)**a)/(a*((lamb*dgammaE)**a+1))-np.log((lamb*dgammaE)**a+1)/a**2)*((lamb*dgammaE)**a+1)**((n-1)/a))
    eq5=np.sum((yexp-eta)*(eta0-etainf)/a*(np.exp((n-1)/a*np.log((dgammaE*lamb)**a+1))*np.log((dgammaE*lamb)**a+1))) 
    return [eq1, eq2, eq3, eq4, eq5]
  
def run_button_lab():
    myLabel=Label(frame, text="Solving for "+select_mod.get()+" model...").grid(row=2, column=0)
    law=select_mod.get()
    param=fsolve(func,param0)
    graphBtn=Button(root,text="Show graph",padx=30,pady=10, command=lambda: graph(param,law,etaE,dgammaE)).grid(row=2, column=0)
    
#Run program after selection of model and file
runBtn=Button(frame,text="Run", padx=30,pady=10, command=run_button_lab).grid(row=1, column=0) 




    
root.mainloop() 