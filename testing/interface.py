# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 13:41:32 2022

@author: Bérénice
"""
from tkinter import *
from PIL import ImageTk, Image
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import sys
import os
#from regTest3 import *



root = Tk()
root.title('Rheocal: Rheology model regression!')    
root.geometry("800x400")

def run_regression():
    os.system('regTest3.py')
    
def run_button_lab():
    myLabel=Label(frame, text="Solving for "+select_mod.get()+" model...").grid(row=2, column=0)

# def graph():
#     dgammaE=[0.01,0.0147,0.0215,0.0316,0.0464,0.0681,0.1,0.147,0.215,0.316]
#     etaE=[426,419,417,409,402,396,388,379,368,355]
#     plt.plot(dgammaE,etaE,'bx')
#     plt.show
    
frame= LabelFrame(root, text="Select parameters", padx=20,pady=20)
frame.grid(row=0,column=0,padx=10,pady=10)

# frame2= LabelFrame(root, text="Figures", padx=20,pady=20)
# frame2.grid(row=0,column=1,padx=10,pady=10)
#Rheology Model list of options
options=[
    "Power Law",
    "Carreau-Yasuda",
    "Cross"]

#User enters model
select_mod=StringVar()
select_mod.set(options[0])

choice = OptionMenu(frame, select_mod,*options)
choice.grid(row=0, column=0) 



#Run program after selection of model and file
myButton=Button(frame,text="Run", padx=30,pady=10, command=run_regression).grid(row=1, column=0)  
#myButton=Button(frame,text="Run", padx=30,pady=10, command=graph).grid(row=1, column=0) 

root.mainloop() 