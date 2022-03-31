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

from NR4functions import *

# matplotlib.use('TkAgg')


#Main variable of interest
# dgammaE=[]
# etaE=[]
# guess_param=[]
# param=[]
# law=[]
# dgamma=[]
# eta=[]

#Rheology Model list of options
options=[
    "Power Law",
    "Carreau",
    "Cross",
    "autofit"]


root = Tk()
root.title('Rheocal: Rheology model regression!') 
root.state('zoomed')   
root.resizable(False, False)
#root.geometry("1200x800")

my_notebook=ttk.Notebook(root)
my_notebook.grid(row=0, column=0)

masterf= LabelFrame(root, width=1200,heigh=800)
masterf.grid(row=0,column=0)

master2f= LabelFrame(root, width=1200,heigh=800)
master2f.grid(row=0,column=0)
class NLR:
    def __init__(self, law='Power Law',dgammaE=[],etaE=[],guess=[],param=[],dgamma=[],eta=[]):
        self.dgammaE = dgammaE
        self.etaE=etaE
        self.law=law
        self.guess=guess
        self.param=param
        self.dgamma=dgamma
        self.eta=eta

if __name__=='__main__':
    reg=NLR()
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
    
          del_vec=np.arange(0,len(reg.dgammaE),1,dtype=int)
          reg.dgammaE=np.delete(reg.dgammaE,del_vec)
          reg.etaE=np.delete(reg.etaE,del_vec)
          [reg.etaE,reg.dgammaE]=readData(file.name)
          # for line in f:
          #     # Split on any whitespace (including tab characters)
          #     row = line.split()
          #     # Convert strings to numeric values:
          #     reg.dgammaE.append(float(row[0]))
          #     reg.etaE.append(float(row[1]))
          #If values are in descending order, puts it back in ascending order
          # if dgammaE[1]<dgammaE[0]:
          #     dgammaE=dgammaE[::-1]
          #     etaE=etaE[::-1]
          #     print("Order of data was inversed")
          
          ### Draw input data ###
          ax = fig.add_subplot()
          #Plotting guess values
          line_input = ax.plot(reg.dgammaE,reg.etaE,'bx')
          ax.set_yscale("log")
          ax.set_xscale("log")
          ax.set_xlabel("$\dot \gamma [1/s]$")
          ax.set_ylabel("$\eta$")
          ax.autoscale(enable=True, axis='both')

          toolbar = NavigationToolbar2Tk(canvas, gframe)
          toolbar.update()
        
          toolbar.grid(row=1,column=0,padx=10,pady=10)
          canvas.get_tk_widget().grid(row=0,column=0)
          
    
    
    def initialGuess(event):
        label = Label(frame, text="Please define initial guesses on parameters:", font=('Arial 12'))
        label.grid(row=3, column=0,columnspan=3, pady=15)
        #Define label of each model's parameter
        if select_mod.get()==options[0]:
            param_lbl=["m","n"]
        if select_mod.get()==options[1]:
            param_lbl=["eta _inf","eta _0","lambda","n"]
        if select_mod.get()==options[2]:
            param_lbl=["eta_inf","eta_0",'alpha',"n"]
        #Print the parameter labels and show entry box to the right
        for x in range(len(param_lbl)):
            #Entry box pushed to the left
            guess_input=Entry(frame,width=15)
            guess_input.grid(row=4+x, column=1,sticky="w")
            #Label pushed to the right, next to the box
            lbl_m = Label(master=frame, text=param_lbl[x]+" =")
            lbl_m.grid(row=4+x, column=0, sticky="e")
            #retrieve the input value of the parameter guess
            reg.guess.append(guess_input)
    
            
    def initialGraph():
        #clear param to allow for iterations on the guess values
        if len(reg.param)!=[]:
            del_vec=np.arange(0,len(reg.param),1,dtype=int)
            reg.param=np.delete(reg.param,del_vec)
        #create the x gamma to evaluate in y    
        reg.dgamma=np.logspace(np.log10(min(reg.dgammaE)),np.log10(max(reg.dgammaE)),100)
        #retrieve the numerical values of the guessed parameters to evaluate the function
        for i in range(len(reg.guess)):
            try:
                reg.param=np.append(reg.param,float(reg.guess[i].get()))
            except ValueError:
                print("Make sure you entered numbers for each parameter")
        #Viscosity data corresponding to user defined parameters
        reg.eta = estimate(reg.param,select_mod.get(),reg.dgamma)

        #Figure initialization
        fig2 = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig2.add_subplot()
        #Plotting new figure with guess values AND input data
        line_guess = ax.plot(reg.dgammaE,reg.etaE,'gx',reg.dgamma,reg.eta,'b-')
        ax.set_yscale("log")
        ax.set_xscale("log")
        ax.set_xlabel("$\dot \gamma [1/s]$")
        ax.set_ylabel("$\eta$")
        ax.legend(['input data','guess'])
        ax.autoscale(enable=True, axis='both')
        #printing onto the canvas the modified plot
        canvas = FigureCanvasTkAgg(fig2, master=gframe)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0)

    
    def Runregression():
        #initial guess entered by the user are transfered to param0 variable
        param0=reg.param
        #caling the regression function
        reg.param= regression(param0,select_mod.get(),reg.dgammaE,reg.etaE)  
        #evaluating function with the newfound parameters from the regression
        reg.eta = estimate(reg.param,select_mod.get(),reg.dgamma)
        
        ###PRINTING RESULTS###
        if select_mod.get()==options[0]:
            param_lbl=["m","n"]
        if select_mod.get()==options[1]:
            param_lbl=["eta_inf","eta_0",'lambda',"n"]
        if select_mod.get()==options[2]:
            param_lbl=["eta_inf","eta_0",'alpha',"n"]
    
        for x in range(len(param_lbl)):
            lbl_ans = Label(master=rframe, text=param_lbl[x]+" = "+str(reg.param[x]))
            lbl_ans.grid(row=4+x, column=0, sticky="e")

        #Set up of the final frame
        fframe= LabelFrame(master2f, text="Non linear regression result", padx=10,pady=10)
        fframe.grid(row=0,column=0,padx=10,pady=10)
        
        #Figure initialization
        ffig = plt.Figure(figsize=(6, 5), dpi=100)
        axf = ffig.add_subplot()
        #Plotting new figure with guess values AND input data
        line_final = axf.plot(reg.dgammaE,reg.etaE,'gx',reg.dgamma,reg.eta,'k-')
        axf.set_yscale("log")
        axf.set_xscale("log")
        axf.set_xlabel("$\dot \gamma [1/s]$")
        axf.set_ylabel("$\eta$")
        axf.legend(['input data','result'])
        axf.autoscale(enable=True, axis='both')
        #printing onto the canvas the modified plot
        fcanvas = FigureCanvasTkAgg(ffig, master=fframe)
        fcanvas.draw()
        fcanvas.get_tk_widget().grid(row=0,column=0)
        


    
    #%% INPUT
    
    
    ### 1. INPUT FILE ###
    #Set up of the input data frame
    frame= LabelFrame(masterf, text="Select Parameters", padx=20,pady=20)
    frame.grid(row=0,column=0,padx=10,pady=10,sticky="n")
    
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
    #Ok button when model is selected
    btn_ok=Button(frame, text="Ok")
    btn_ok.bind("<Button-1>", initialGuess)
    btn_ok.grid(row=2, column=2)
    
    #%% FIGURES
    # ### 3. GUESS INPUT PARAMETERS INITIAL VALUES ###
    #Set up of the graph frame
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    gframe= LabelFrame(masterf, text="Figures", padx=10,pady=10)
    gframe.grid(row=0,column=1,rowspan=3,padx=10,pady=10)
    #Initialize guess canvas
    canvas = FigureCanvasTkAgg(fig, master=gframe)
    canvas.draw()
    #Show the guess
    btn_showguess=Button(frame, text="Show me my guess",command=initialGraph).grid(row=8, column=2)   
    
    #Run button to run regression    
    btn_run=Button(frame, text="Run",bg="orange",command=Runregression)
    btn_run.grid(row=8, column=9,padx=10,sticky="e")

    #%% RESULTS
    rframe= LabelFrame(masterf, text="Results", padx=40,pady=20)
    rframe.grid(row=1,column=0,padx=10,pady=10)

    my_notebook.add(masterf, text="Input")
    my_notebook.add(master2f, text="Results")
    
root.mainloop() 