# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 17:37:18 2022

@author: Bérénice
"""

from tkinter import *
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib

import sys
import os

from NewtonRaphson4func import estimate


#Main variable of interest
dgammaE=[]
etaE=[]
guess_param=[]
param=[]
law=[]
dgamma=[]
eta=[]

#Rheology Model list of options
options=[
    "Power Law",
    "Carreau-Yasuda",
    "Cross",
    "autofit"]


root = Tk()
root.title('Rheocal: Rheology model regression!')    
root.resizable(False, False)
root.geometry("1200x800")


def open_file():
#function to open and read files
   file = filedialog.askopenfile(mode='r', filetypes=[('Text files', '*.txt'),('CSV files','*.csv')])
   if file:
      #Find the name of the file
      filepath = os.path.abspath(file.name)
      #Extract and print the file name      
      path=str(filepath).split("\\")
      name=path[len(path)-1]
      Label(frame, text=name, font=('Arial 11')).grid(row=0, column=1)
      #Extract data from file
      f = open(filepath, 'r')

      dgammaE.clear()
      etaE.clear()
      for line in f:
          # Split on any whitespace (including tab characters)
          row = line.split()
          # Convert strings to numeric values:
          dgammaE.append(float(row[0]))
          etaE.append(float(row[1]))
      
      fig = plt.Figure(figsize=(5, 4), dpi=100)
      ax = fig.add_subplot()
      #Plotting guess values
      line_exp = ax.plot(dgammaE,etaE,'kx')
      ax.set_yscale("log")
      ax.set_xscale("log")
      ax.set_xlabel("dgamma [1/s]")
      ax.set_ylabel("eta")
      


def initialGuess(event):
    label = Label(frame, text="Please define initial guesses on parameters:", font=('Arial 12'))
    label.grid(row=3, column=0,columnspan=3, pady=15)
    #Define label of each model's parameter
    if select_mod.get()==options[0]:
        param_lbl=["m","n"]
    if select_mod.get()==options[1]:
        param_lbl=["eta_inf","eta_0",'lambda',"n"]
    if select_mod.get()==options[2]:
        param_lbl=["eta_inf","eta_0",'alpha',"n"]

    for x in range(len(param_lbl)):
        guess_input=Entry(frame,width=15)
        guess_input.grid(row=4+x, column=1,sticky="w")
        lbl_m = Label(master=frame, text=param_lbl[x]+" =")
        lbl_m.grid(row=4+x, column=0, sticky="e")
        guess_param.append(guess_input)
        
def initialGraph():
    dgamma=np.logspace(np.log10(0.01),np.log10(100),100)
    
    for i in range(len(guess_param)):
        try:
            param.append(float(guess_param[i].get()))
        except ValueError:
            print("Make sure you entered numbers for each parameter")
    #Data corresponding to user defined parameters
    eta = estimate(param,select_mod.get(),dgamma)
    #Figure initialization
    # fig = plt.Figure(figsize=(5, 4), dpi=100)
    # ax = fig.add_subplot()
    #Plotting guess values
    line_guess = ax.plot(dgamma,eta,'b-')
    # ax.set_yscale("log")
    # ax.set_xscale("log")
    # ax.set_xlabel("dgamma [1/s]")
    # ax.set_ylabel("eta")
    ax.autoscale(enable=True, axis='both')
    
    #Set up of the graph frame
    gframe= LabelFrame(root, text="Figures", padx=20,pady=20)
    gframe.grid(row=0,column=1,rowspan=3,padx=10,pady=10)
    #Initialize guess canvas
    canvas = FigureCanvasTkAgg(fig, master=gframe)
    canvas.draw()
    
    toolbar = NavigationToolbar2Tk(canvas, gframe)
    toolbar.update()
    
    toolbar.grid(row=1,column=0,padx=10,pady=10)
    canvas.get_tk_widget().grid(row=0,column=0,padx=10,pady=10)
    #clear param to allow for iterations on the guess values
    param.clear()
            

#%% INPUT
### 1. INPUT FILE ###
#Set up of the input data frame
frame= LabelFrame(root, text="Select Parameters", padx=20,pady=20)
frame.grid(row=0,column=0,padx=10,pady=10)

# Label widget for file seletion
lbl_file = Label(frame, text="Select a data input file:", font=('Arial 12'))
lbl_file.grid(row=0, column=0, pady=10)

# Button to search for a file
Button(frame, text="Browse file", command=open_file).grid(row=0, column=2,pady=10)

### 2. INPUT RHEOLOGY MODEL ###
#User selects model
select_mod=StringVar()
select_mod.set(options[0])
#Label for rheology law selection
label = Label(frame, text="Select a rheology model:", font=('Arial 12')).grid(row=2, column=0)
#Dropdown menu with rheology law options
dropdown = OptionMenu(frame, select_mod,*options)
dropdown.config(width=20)
dropdown.grid(row=2, column=1)
law=select_mod.get()
#Ok button when model is selected
btn_ok=Button(frame, text="Ok")
btn_ok.bind("<Button-1>", initialGuess)
btn_ok.grid(row=2, column=2)

#%% FIGURES
### 3. GUESS INPUT PARAMETERS INITIAL VALUES ###
#Show the guess
btn_showguess=Button(frame, text="Show me my guess",command=initialGraph).grid(row=8, column=2)   





root.mainloop() 