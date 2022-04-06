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
import sys

from NR4functions import *


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

window=ttk.Notebook(root)
window.grid(row=0, column=0)

help_tab_frame= LabelFrame(root, width=1200,heigh=800)
help_tab_frame.grid(row=0,column=0)

input_tab_frame= LabelFrame(root, width=1200,heigh=800)
input_tab_frame.grid(row=0,column=0)

result_tab_frame= LabelFrame(root, width=1200,heigh=800)
result_tab_frame.grid(row=0,column=0)
class NLR:
    def __init__(self, law='Power Law',n=0,tol=1e-04,dgammaE=[],etaE=[],guess=[],param=[],dgamma=[],eta=[]):
        self.dgammaE = dgammaE
        self.etaE=etaE
        self.law=law
        self.guess=guess
        self.param=param
        self.dgamma=dgamma
        self.eta=eta
        self.n=n
        self.tol=tol

if __name__=='__main__':
    reg=NLR()
    def open_file():
    #function to open and read files
       file = filedialog.askopenfile(mode='r', filetypes=[('Text files', '*.txt'),('DAT files','*.dat'),('CSV files','*.csv')])
       if file:
          #Extract and print the file name 
          path=str(file.name).split("/")#list of the filepath directory path
          file_name=path[len(path)-1]
          Label(frame, text=file_name, font=('Arial 11')).grid(row=0, column=1)
          
          #Extract data from file
          f = open(file.name, 'r')
          del_vec=np.arange(0,len(reg.dgammaE),1,dtype=int)
          reg.dgammaE=np.delete(reg.dgammaE,del_vec)
          reg.etaE=np.delete(reg.etaE,del_vec)
          [reg.etaE,reg.dgammaE]=readData(file.name)
          
          ### Draw input data ###
          #Initialize guess canvas
          fig = plt.Figure(figsize=(5, 4), dpi=100)
          canvas = FigureCanvasTkAgg(fig, master=gframe)
          canvas.draw()


          #Plotting guess values
          ax = fig.add_subplot()
          line_input = ax.plot(reg.dgammaE,reg.etaE,'bx')
          ax.set_yscale("log")
          ax.set_xscale("log")
          ax.set_xlabel("$\dot \gamma [1/s]$")
          ax.set_ylabel("$\eta$")
          fig.tight_layout()
          ax.autoscale(enable=True, axis='both')
               
          toolbar = NavigationToolbar2Tk(canvas, gframe)
          toolbar.update()
        
          toolbar.grid(row=1,column=0,padx=10,pady=10)
          canvas.get_tk_widget().grid(row=0,column=0)
          
    
    def initialGuess(event):
        label = Label(frame, text="Please define initial guesses on parameters:", font=('Arial 12'))
        label.grid(row=3, column=0,columnspan=3, pady=15)
        
        eqfig = plt.figure(figsize=(3, 1), dpi=100)
        formula = eqfig.add_subplot()
        formula.get_xaxis().set_visible(False)
        formula.get_yaxis().set_visible(False)
        #Default Power Law equation
        equation="$\eta (\dot \gamma) = m\dot \gamma^{n-1}$"
        #Define label of each model's parameter
        if select_mod.get()==options[0]:
            param_lbl=["m","n"]
            equation="$\eta (\dot \gamma) = m\dot \gamma^{n-1}$"
        if select_mod.get()==options[1]:
            param_lbl=["eta _inf","eta _0","lambda","n"]
            equation="$\\frac {\eta (\dot \gamma) - \eta _{\infty}}{\eta _0 - \eta _{\infty}} = [1+(\dot \gamma \lambda )^a]^{\\frac {n-1}{a}}$"
        if select_mod.get()==options[2]:
            param_lbl=["eta_inf","eta_0",'alpha',"n"]
            #equation="$\eta _a = \eta _{\infty} + \\frac {\eta _0 - \eta _{\infty}}{1+(\alpha _c \lambda )^m}$"
            
        #Image of the model law with the grec letter parameters
        formula.text(0.1,0.1,equation, fontsize = 13)
        eqcanvas = FigureCanvasTkAgg(eqfig, master=rframe)
        eqcanvas.draw()
        eqcanvas.get_tk_widget().grid(row=0,column=0)
        
        #Print the parameter labels and show entry box to the right
        for x in range(len(param_lbl)):
            guess_input=Entry(frame,width=15)

            lbl_m = Label(master=frame, text=param_lbl[x]+" =")
            lbl_m.grid(row=4+x, column=0, sticky="e")
            if (select_mod.get()==options[1] or select_mod.get()==options[2]) and (x==0 or x==1):
                if x==0:
                    guess_input.insert(0,str(1.1*min(reg.etaE)))
                if x==1:
                    guess_input.insert(0,str(0.99*max(reg.etaE)))
            guess_input.grid(row=4+x, column=1,sticky="w")
            #retrieve the input value of the parameter guess
            reg.guess.append(guess_input)
            


    
            
    def initialGraph():
        #clear param to allow for iterations on the guess values
        if len(reg.param)!=[]:
            del_vec=np.arange(0,len(reg.param),1,dtype=int)
            reg.param=np.delete(reg.param,del_vec)
                  
        #retrieve the numerical values of the guessed parameters to evaluate the function
        for i in range(len(reg.guess)):
            try:
                reg.param=np.append(reg.param,float(reg.guess[i].get()))
            except ValueError:
                print("Make sure you entered numbers for each parameter")
        
        #Viscosity data corresponding to user defined parameters
        reg.dgamma=np.logspace(np.log10(min(reg.dgammaE)),np.log10(max(reg.dgammaE)),100)
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
        fig2.tight_layout()
        ax.autoscale(enable=True, axis='both')
        #printing onto the canvas the modified plot
        canvas = FigureCanvasTkAgg(fig2, master=gframe)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0)

    
    def Runregression():
        #caling the regression function
        reg.param,n= regression(reg.param,select_mod.get(),reg.dgammaE,reg.etaE,reg.tol,reg.n)  
        #viscosity found with the calculated parameters (to be plotted)
        reg.eta = estimate(reg.param,select_mod.get(),reg.dgamma)
        
        ###PRINTING RESULTS###
        if select_mod.get()==options[0]:
            param_lbl=["m","n"]
        if select_mod.get()==options[1]:
            param_lbl=["eta_inf","eta_0",'lambda',"n"]
        if select_mod.get()==options[2]:
            param_lbl=["eta_inf","eta_0",'alpha',"n"]
    
        for x in range(len(param_lbl)):
            lbl_ans = Label(master=rframe, text=param_lbl[x]+" = "+'{:.4f}'.format(reg.param[x]))
            lbl_ans.grid(row=1+x, column=0, sticky="w")

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
        ffig.tight_layout()
        #printing onto the canvas
        fcanvas = FigureCanvasTkAgg(ffig, master=fframe)
        fcanvas.draw()
        
        ftoolbar = NavigationToolbar2Tk(fcanvas, fframe)
        ftoolbar.update()
      
        ftoolbar.grid(row=1,column=0,padx=10,pady=10)
        fcanvas.get_tk_widget().grid(row=0,column=0)
        
        #Printing regression data results
        lbl_nandtol = Label(master=result_data_frm, text=" - Regression performed in "+'{:.0f}'.format(n)+"/500 iterations.\n - Tolerance of "+'{:.3e}'.format(reg.tol))
        lbl_nandtol.grid(row=0, column=0, sticky="w")


    
    #%% INPUT
    ### 1. HELP FIGURE FRAME ###    
    
    ### 2. INPUT DATA FRAME ###
    frame= LabelFrame(input_tab_frame, text="Select Parameters", padx=20,pady=20)
    frame.grid(row=0,column=0,padx=10,pady=10,sticky="n")
    
    # Label widget for file seletion
    lbl_file = Label(frame, text="Select a data input file:", font=('Arial 12'))
    lbl_file.grid(row=0, column=0, pady=10)
    
    # Button to search for a file
    Button(frame, text="Browse file", command=open_file).grid(row=0, column=2,pady=10)
    
    #Dropdown menu to select model
    select_mod=StringVar()
    select_mod.set(options[0])
    label = Label(frame, text="Select a rheology model:", font=('Arial 12')).grid(row=2, column=0)

    dropdown = OptionMenu(frame, select_mod,*options)
    dropdown.config(width=20)
    dropdown.grid(row=2, column=1)
    #Ok button to confirm choice
    btn_ok=Button(frame, text="Ok")
    btn_ok.bind("<Button-1>", initialGuess)
    btn_ok.grid(row=2, column=2)
    
    #Input file is read and initial guesses are set by users
    btn_showguess=Button(frame, text="Show me my guess",command=initialGraph).grid(row=8, column=2)   
    
    #Run button to run regression    
    btn_run=Button(frame, text="Run",bg="orange",command=Runregression)
    btn_run.grid(row=8, column=9,padx=10,sticky="e")
    
    ### INITIAL GRAPH FRAME ###
    #graph frame#
    gframe= LabelFrame(input_tab_frame, text="Figures", padx=10,pady=10)
    gframe.grid(row=0,column=1,rowspan=3,padx=10,pady=10)


    #%% RESULTS

    rframe= LabelFrame(input_tab_frame, text="Results", padx=40,pady=20)
    rframe.grid(row=1,column=0,padx=10,pady=10)

    ### RESULT GRAPH FRAME ###
    fframe= LabelFrame(result_tab_frame, text="Non linear regression graph", padx=10,pady=10)
    fframe.grid(row=0,column=0,padx=10,pady=10)
      
    result_data_frm=LabelFrame(result_tab_frame, text="Regression performance", padx=10,pady=10)
    result_data_frm.grid(row=0,column=1,padx=10,pady=10, sticky="n")
    
    #Show tabs
    window.add(help_tab_frame, text="Help")
    window.add(input_tab_frame, text="Input")
    window.add(result_tab_frame, text="Results")
    
root.mainloop() 