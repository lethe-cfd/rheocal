# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 14:32:30 2022

@author: Bérénice
"""
import numpy as np


def r2score(xexp,yexp,yreg):
    yavg=np.sum(yexp)/len(yexp)
    avg=yexp-yavg
    reg=yexp-yreg
    coeff=(np.sum(np.power(avg,2))-np.sum(np.power(reg,2)))/np.sum(np.power(avg,2))
    print('\nR2 = ')
    print(coeff)
    return coeff

# def pvalue(x,y):
    
#     return coeff