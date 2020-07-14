# -*- coding: utf-8 -*-

import numpy as np
from scipy import constants as const
import math

np.set_printoptions(suppress=True)

def charge():

    try:
        a = float(input("Enter atomic mass (A): "))
        if a == 0:
            raise Exception
    except:
        print("Please enter (nonzero) numeric values.")
        charge()
    try:
        z = float(input("Enter atomic number (Z): "))
        if z == 0:
            raise Exception
    except:
        print("Please enter (nonzero) numeric values.")
        charge()
    try:
        e = float(input("Enter beam energy (E): "))
        if e == 0:
            raise Exception
    except:
        print("Please enter (nonzero) numeric values.")
        charge()
                
    global v0
    
    v0 = 2.188*10**6 # v0 = e^2/h = Bohr velocity of the electron in m/s
        
    global e_amu
    
    e_amu = 931.5 # rest energy of 1 AMU in MeV

    global c
    
    c = float(const.c) # speed of light
    
    def calc_qbar(energy, mass, atomic_number):
        
        v = (2/e_amu)**0.5*(energy/mass)**0.5*c # particle velocity; from E = 1/2mv^2
    
        qbar = atomic_number*(1-1.041*np.exp(-0.851*atomic_number**-0.432*(v/v0)**0.847)) # mean charge state
        
        return qbar

    def calc_fractional_pop(atomic_number, mean_charge):
        
        q = round(calc_qbar(e,a,z)) # the closest integer charge state to qbar
         
        d = 0.27*atomic_number**0.5 # distribution width (sigma) in a gaussian or normal distribution
    
        pop = np.linspace(q-10, q+10, num = 21)

        pnorm = (1/(d*math.sqrt(2*math.pi))*(np.exp((-(pop-mean_charge)**2)/(2*(d**2)))))*100 # fractional population percentage for each charge state in pop (self-normalized gaussian distribution)

        pop_complete = np.column_stack((pop, pnorm)) # print charge states and percentages in parallel columns           
             
        print("\r")

        print("mean charge state = ", round(mean_charge, 5))

        print("distribution width (sigma) = ", round(d, 5))

        print("charge state vs percentage")

        print(pop_complete)

        print("total percentage = ", round(sum(pnorm), 3))
    
    def repeat():
        again = input("Run another calculation (y/n)? ")
        
        if again == "y":
            charge()
        elif again == "Y":
            charge()
        else:
            quit()              
        
    calc_qbar(e,a,z)
    
    calc_fractional_pop(z,calc_qbar(e,a,z))
            
    repeat()

charge()

