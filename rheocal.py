# -*- coding: utf-8 -*-
"""
Rheocal: Non linear regression program for certain rheology models including:
    - Power Law (2 parameters)
    - Carreau (4 parameters)
    - Cross (4 parameters)
    
Created on Mon Mar 21 17:37:18 2022
@author: Bérénice Dubois
"""

#Import librairies
from tkinter import *
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfile
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
import sys
from NR4functions import * #Also accessible in rheocal project

#%%

#Rheology Model list of options
options=[
    "Power Law",
    "Carreau",
    "Cross"]

#Beginning of user interface main loop
root = Tk()
root.title('Rheocal: Rheology model regression!') 
#window first automaticaly fits whole screen but can be resized
root.state('zoomed')   
root.resizable(True, True)
#Create notebook to make tabs
window=ttk.Notebook(root)
window.grid(row=0, column=0)

#Main frame on each tab to place all other frames/widgets
help_tab_frame= LabelFrame(root, width=1200,heigh=500)
help_tab_frame.grid(row=0,column=0)

input_tab_frame= LabelFrame(root, width=1200,heigh=800)
input_tab_frame.grid(row=0,column=0)

result_tab_frame= LabelFrame(root, width=1200,heigh=800)
result_tab_frame.grid(row=0,column=0)

#%% Class definition

class NLR:
    """
    Non Linear Regression: Store values printed on the user interface
    - n: number of iterations on solving method
    - tol: tolerance on regression answer
    - dgammaE, etaE, guess: user input for experimental shear rate, viscosity and initial guesses on parameters
    - dgamma, eta, param: calculated values for viscosity for a sample shear rate vector, calculated parameters
    - param_lbl: parameters label for user interface
    """
    def __init__(self,n=0,tol=1e-05,theta=1.0,dgammaE=[],etaE=[],guess=[],dgamma=[],eta=[],param=[],param_lbl=[]):
        self.dgammaE = dgammaE
        self.etaE=etaE
        self.guess=guess
        self.param=param
        self.dgamma=dgamma
        self.eta=eta
        self.n=n
        self.tol=tol
        self.theta=theta
        self.param_lbl=param_lbl
        
#%%Functions        

if __name__=='__main__':
    #regression problem is initialized
    reg=NLR()
          
    def formula_img(law):
        """
        Display the select model's formula in a canvas
           * equation canvas created to show equation
        """
        #Figure settings
        eqfig = plt.figure(figsize=(3, 1), dpi=100)
        formula = eqfig.add_subplot()
        formula.get_xaxis().set_visible(False)
        formula.get_yaxis().set_visible(False)
        #Selected equation to print
        if law==options[0]:
            equation="$\eta (\dot \gamma) = m\dot \gamma^{n-1}$"
        if law==options[1]:
            equation="$\\frac {\eta (\dot \gamma) - \eta _{\infty}}{\eta _0 - \eta _{\infty}} = [1+(\dot \gamma \lambda )^a]^{\\frac {n-1}{a}}$"
        if law==options[2]:
            equation="$\eta (\dot \gamma) = \eta _{\infty} + \\frac {\eta _0 - \eta _{\infty}}{ 1+ (\\alpha_c \lambda )^m }$"
            
        #Print model law with the grec letter parameters
        formula.text(0.5,0.5,equation,horizontalalignment='center',verticalalignment='center', fontsize = 13)
        eqcanvas = FigureCanvasTkAgg(eqfig, master=rframe)
        eqcanvas.draw()
        eqcanvas.get_tk_widget().grid(row=0,column=0)
          
    def show_performance(frame):
        """
        Display the regression's performance data
         - tolerance
         - number of iteration
         - mean error
         - R2
        """
        #Calculating R2 score and mean error
        R2,meanerror=r2score(reg.etaE,estimate(reg.param,select_mod.get(),reg.dgammaE))
        #Printing regression data results
        lbl_n = Label(master=frame, text=" - Regression performed in: "+'{:.0f}'.format(reg.n)+"/500 iterations.")
        lbl_n.grid(row=0, column=0,pady=10, sticky="w")
        lbl_tol = Label(master=frame, text=" - Tolerance of: "+'{:.3e}'.format(reg.tol))
        lbl_tol.grid(row=1, column=0, pady=10, sticky="w")
        lbl_mean2err = Label(master=frame, text=" - Average error on input data: "+'{:.3%}'.format(meanerror))
        lbl_mean2err.grid(row=3, column=0, pady=10, sticky="w")   
        lbl_R2 = Label(master=frame, text=" - Determination coefficient: "+'{:.5f}'.format(R2))
        lbl_R2.grid(row=4, column=0, pady=10, sticky="w") 
          
    def open_file():
       """
       Open and read files, then extract the data and plot it on the interface
         * canvas created in input tab on the right to plot
       """
       file = filedialog.askopenfile(mode='r', filetypes=[('Text files', '*.txt'),('CSV files','*.csv')])
       path=[]
       if file:
          #Extract and print the file name 
          path=str(file.name).split("/")#list of the filepath directory path
          file_name=path[len(path)-1]
          Label(frame, text=file_name, font=('Arial 11')).grid(row=0, column=1)
          
          #Extract data from file
          f = open(file.name, 'r')
          [reg.dgammaE,reg.etaE]=readData(file.name)
          f.close()
          
          ### Draw input data ###
          #Initialize canvas
          fig = plt.Figure(figsize=(5, 4), dpi=100)
          canvas = FigureCanvasTkAgg(fig, master=gframe)
          canvas.draw()

          #Plotting input values
          ax = fig.add_subplot()
          line_input = ax.plot(reg.dgammaE,reg.etaE,'gx')
          figure_opt(ax)
          fig.tight_layout()
         
          #Navigation Toolbar
          toolbar = NavigationToolbar2Tk(canvas, gframe)
          toolbar.update()
          toolbar.grid(row=1,column=0,padx=10,pady=10)
          
          #Printing embedded canvas onto the interface
          canvas.get_tk_widget().grid(row=0,column=0)
          
    def enter_guess(event):
        """
        Ask for and retrieve user entered initial guesses on parameters
           * Tkinter variables only, must be transformed into floats
        """
        #show equation of the selected model
        formula_img(select_mod.get())
        
        #Asking for initial guesses
        label = Label(frame, text="Please define initial guesses on parameters (decimal separator is dot):", font=('Arial 12'))
        label.grid(row=3, column=0,columnspan=3, pady=15)       
        #Define label of each model's parameter
        if select_mod.get()==options[0]:
            reg.param_lbl=["m","n"]
        if select_mod.get()==options[1]:
            reg.param_lbl=["eta _inf","eta _0","lambda","n"]
        if select_mod.get()==options[2]:
            reg.param_lbl=["eta_inf","eta_0","alpha","m"]

        #Print the parameter labels and show entry box to the right
        for i in range(len(reg.param_lbl)):
            lbl_m = Label(master=frame, text=reg.param_lbl[i]+" =")
            lbl_m.grid(row=4+i, column=0, sticky="e")
            #Entry boxes showed with suggestions for eta_0 and eta_inf
            guess_input=Entry(frame,width=15)
            guess_input.grid(row=4+i, column=1,sticky="w")
            if (select_mod.get()==options[1] or select_mod.get()==options[2]) and (i==0 or i==1):
                if i==0:
                    guess_input.insert(0,str(1.1*min(reg.etaE)))
                if i==1:
                    guess_input.insert(0,str(0.99*max(reg.etaE)))
            #retrieve the input value of the parameter guess
            reg.guess.append(guess_input)
                      
    def show_guess():
        """
        Show the user's guess on the parameters, guess against input plot
          * canvas created in input tab on the right to plot
        """
        #clear param to allow reentering guesses multiple times
        if len(reg.param)!=[]:
            del_vec=np.arange(0,len(reg.param),1,dtype=int)
            reg.param=np.delete(reg.param,del_vec)
                  
        #retrieve the numerical values of the guess or infor user of error
        for i in range(len(reg.guess)):
            try:
                reg.param=np.append(reg.param,float(reg.guess[i].get()))
            except ValueError:
                entry_error_lbl =Label(master=frame, text="Make sure you entered numbers for each parameter. Please run rheocal again.",fg='red')
                entry_error_lbl.grid(row=9, column=0, columnspan=3)
        
        #Viscosity data corresponding to user defined parameters
        reg.dgamma=np.logspace(np.log10(min(reg.dgammaE)),np.log10(max(reg.dgammaE)),100)
        reg.eta = estimate(reg.param,select_mod.get(),reg.dgamma)

        #Figure initialization
        fig2 = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig2.add_subplot()
        #Plotting new figure with guess values AND input data
        line_guess = ax.plot(reg.dgammaE,reg.etaE,'gx',reg.dgamma,reg.eta,'b-')
        figure_opt(ax)     
        ax.legend(['input data','guess'])
        fig2.tight_layout()
        
        #printing onto the canvas the modified plot
        canvas = FigureCanvasTkAgg(fig2, master=gframe)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0)

    def Runregression():
        """
        Show regression result for parameters in input tab and performance in result tab
          * canvas created in result tab on the left to plot
        """
        #caling the regression function
        reg.param,reg.n,reg.theta= newton_solve(reg.param,select_mod.get(),reg.dgammaE,reg.etaE,reg.tol,reg.n,reg.theta)  
        #viscosity found with the calculated parameters (to be plotted)
        reg.eta = estimate(reg.param,select_mod.get(),reg.dgamma)
        
        #Printing parameters newfound values    
        for i in range(len(reg.param_lbl)):
            lbl_ans = Label(master=rframe, text=reg.param_lbl[i]+" = "+'{:.4f}'.format(reg.param[i]))
            lbl_ans.grid(row=1+i, column=0, sticky="w")

        #Figure initialization
        finalfig = plt.Figure(figsize=(6, 5), dpi=100)
        axf = finalfig.add_subplot()
        #Plotting new figure with guess values AND input data
        line_final = axf.plot(reg.dgammaE,reg.etaE,'gx',reg.dgamma,reg.eta,'k-')
        figure_opt(axf)
        axf.legend(['input data','result'])
        finalfig.tight_layout()
        
        #Printing onto the canvas
        fcanvas = FigureCanvasTkAgg(finalfig, master=fframe)
        fcanvas.draw()
        
        #Navigation Toolbar
        ftoolbar = NavigationToolbar2Tk(fcanvas, fframe)
        ftoolbar.update()
        ftoolbar.grid(row=1,column=0,padx=10,pady=10)
        
        fcanvas.get_tk_widget().grid(row=0,column=0)
        show_performance(result_data_frm)
               
    
    #%% 1. HELP TAB WIDGETS
    #Resize help figure for input file layout  
    open_help_img= Image.open("input_help.png")
    resized_img=open_help_img.resize((400,500), Image.ANTIALIAS)
    sized_help_img= ImageTk.PhotoImage(resized_img)
    
    #Display help image
    help_lbl=Label(help_tab_frame, image=sized_help_img)
    help_lbl.grid(row=0,column=0)
    
    #%% 2. INPUT TAB WIDGETS
    #Every variable changed/input by user within this frame
    frame= LabelFrame(input_tab_frame, text="Select Parameters", padx=20,pady=20)
    frame.grid(row=0,column=0,padx=10,pady=10,sticky="n")
    
    # Label widget for file seletion
    lbl_file = Label(frame, text="Select a data input file:", font=('Arial 12'))
    lbl_file.grid(row=0, column=0, pady=10)
    
    # Button "Browse" to search for a file
    Button(frame, text="Browse file", command=open_file).grid(row=0, column=2,pady=10)
    
    #Dropdown menu to select model
    select_mod=StringVar()
    select_mod.set(options[0])
    label = Label(frame, text="Select a rheology model:", font=('Arial 12')).grid(row=2, column=0)

    dropdown = OptionMenu(frame, select_mod,*options)
    dropdown.config(width=20)
    dropdown.grid(row=2, column=1)
    
    #"Ok" button to confirm choice
    btn_ok=Button(frame, text="Ok")
    btn_ok.bind("<Button-1>", enter_guess)
    btn_ok.grid(row=2, column=2)
    
    #Input file is read and initial guesses are set by users
    btn_showguess=Button(frame, text="Show me my guess",command=show_guess).grid(row=8, column=2)   
    
    #Run button to run regression    
    btn_run=Button(frame, text="Run",bg="orange",command=Runregression)
    btn_run.grid(row=8, column=9,padx=10,sticky="e")

    #Initial graph frame
    gframe= LabelFrame(input_tab_frame, text="Figures", padx=10,pady=10)
    gframe.grid(row=0,column=1,rowspan=3,padx=10,pady=10)

    #Parameter final values and formula frame
    rframe= LabelFrame(input_tab_frame, text="Results", padx=40,pady=20)
    rframe.grid(row=1,column=0,padx=10,pady=10)

    #%% 3. RESULT TAB WIDGETS

    #Result graph frame
    fframe= LabelFrame(result_tab_frame, text="Non linear regression graph", padx=10,pady=10)
    fframe.grid(row=0,column=0,padx=10,pady=10)
    
    #Result performance data frame  
    result_data_frm=LabelFrame(result_tab_frame, text="Regression performance", padx=10,pady=10)
    result_data_frm.grid(row=0,column=1,padx=10,pady=10, sticky="n")
    
    #Show tabs
    window.add(help_tab_frame, text="Help")
    window.add(input_tab_frame, text="Input")
    window.add(result_tab_frame, text="Results")
    
root.mainloop() 