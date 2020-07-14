# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 17:13:17 2020

@author: Nicole Benker
"""

import numpy as np
from scipy import constants as const
import math
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

def pep():
        
    # these constants will be used in calculating normalized emittance

    global e_amu

    e_amu = 931.5 # rest energy of 1 AMU in MeV

    global c

    c = float(const.c) # speed of light

    global rfq_e

    rfq_e = 0.0305 # RFQ acceptance energy 0.0305 MeV/u

    global v

    v = ((2*rfq_e)/e_amu)**0.5 * c # ion velocity in meters/second

    global lorentz_beta

    lorentz_beta = v/c # lorentz beta

    global lorentz_gamma

    lorentz_gamma = 1/((1-lorentz_beta**2)**0.5) # lorentz gamma

    def user_prompt():
        
        global L
        global dh
        global res
        
        try:
            choice = float(input('''Please select pepperpot configuration: 
                      1: Stable ion (ECR)
                      2: Weak beam (CARIBU)
                      3: User Defined setup
                      
                      '''))
            if choice != 1 and choice != 2 and choice != 3:
                raise Exception
                
        except:
            print("Please select option 1, 2, or 3.")
            user_prompt()                
    
        if choice == 3: 
            L = float(input("Enter distance from mask to phosphor in mm: "))
            dh = float(input("Enter spacing between mask holes: "))
            res = float(input("Enter image resolution in mm/pixel: "))
            
        if choice == 1:
            L = 20.0 # distance from mask to phosphor
            dh = 1.5 # spacing between mask holes
            res = 0.0412 # resolution in mm/pixel
            print("Stable Ion (ECR) Configuration")
    
        if choice == 2:
            L = 13.7 # distance from mask to phosphor
            dh = 1.2 # spacing between mask holes
            res = 0.0412 # resolution in mm/pixel
            print("Weak Beam (CARIBU) Configuration")
            
    user_prompt()

    def import_data(res, L):
        
        # import the data from excel
  
        data = pd.read_excel(r'C:\Users\mizam\rotated_beamlets_for_133Cs26.xls') 
                
        data['y_prime'] = data.y_prime_times_L / L  # adding y_prime and x_prime properly into the dataframe
        
        data['x_prime'] = data.x_prime_times_L / L
        
        y_pos_raw = pd.DataFrame(data, columns= ['y_pos']) # making dataframe from single column
        y_pos_raw_array = y_pos_raw.to_numpy()        # sending columnar dataframe to array
        y_pos = res * y_pos_raw_array                   # scaling pixel values by camera resolution in mm/pixel
        
        x_pos_raw = pd.DataFrame(data, columns= ['x_pos'])
        x_pos_raw_array = x_pos_raw.to_numpy()        
        x_pos = res * x_pos_raw_array
        
        intensity = pd.DataFrame(data, columns= ['intensity'])
        I_pix = intensity.to_numpy()               
    
        x_prime_raw = pd.DataFrame(data, columns= ['x_prime'])
        x_prime_array = x_prime_raw.to_numpy()        
        x_p = res * x_prime_array
        
        y_prime_raw = pd.DataFrame(data, columns= ['y_prime'])
        y_prime_array = y_prime_raw.to_numpy()        
        y_p = res * y_prime_array
    
        return y_pos, x_pos, I_pix, x_p, y_p
    
    import_data(res, L)

    y_pos, x_pos, I_pix, x_p, y_p = import_data(res, L)     
    
    def phase_space_components(y_pos, x_pos, I_pix, x_p, y_p):

        # I will call a pixel's intensity value I_pix, and the coordinates x_pos and y_pos and moments x_p and y_p    
        
        I_tot = np.sum(I_pix) # sum of all pixel intensities; this is used as a scaling factor for normalization.
    
        x_avg = (np.sum(x_pos*I_pix))/I_tot
        
        x_p_avg = (np.sum(x_p*I_pix))/I_tot
        
        x_sq_avg = (np.sum(((x_pos-x_avg)**2)*I_pix))/I_tot
        
        x_p_sq_avg = (np.sum(((x_p-x_p_avg)**2)*I_pix))/I_tot
        
        x_x_p_avg = (np.sum(((x_pos-x_avg)*(x_p-x_p_avg))*I_pix))/I_tot
        
        y_avg = (np.sum(y_pos*I_pix))/I_tot
        
        y_p_avg = (np.sum(y_p*I_pix))/I_tot
        
        y_sq_avg = (np.sum(((y_pos-y_avg)**2)*I_pix))/I_tot
        
        y_p_sq_avg = (np.sum(((y_p-y_p_avg)**2)*I_pix))/I_tot
        
        y_y_p_avg = (np.sum(((y_pos-y_avg)*(y_p-y_p_avg))*I_pix))/I_tot
    
        return x_avg, x_p_avg, x_sq_avg, x_p_sq_avg, x_x_p_avg, y_avg, y_p_avg, y_sq_avg, y_p_sq_avg, y_y_p_avg

    phase_space_components(y_pos, x_pos, I_pix, x_p, y_p)
    
    x_avg, x_p_avg, x_sq_avg, x_p_sq_avg, x_x_p_avg, y_avg, y_p_avg, y_sq_avg, y_p_sq_avg, y_y_p_avg = phase_space_components(y_pos, x_pos, I_pix, x_p, y_p)
    
    def emittance_calc(x_avg, x_p_avg, x_sq_avg, x_p_sq_avg, x_x_p_avg, y_avg, y_p_avg, y_sq_avg, y_p_sq_avg, y_y_p_avg):
        
        # and now calculating emittance using the phase space components:
            
        eps_rms_x = math.sqrt((x_sq_avg * x_p_sq_avg - x_x_p_avg))
        
        eps_rms_y = math.sqrt((y_sq_avg * y_p_sq_avg - y_y_p_avg))
        
        eps_norm_x = 4 * lorentz_gamma * lorentz_beta * eps_rms_x
        
        eps_norm_y = 4 * lorentz_gamma * lorentz_beta * eps_rms_y
        
        twiss_beta_x = x_sq_avg / eps_rms_x
        
        twiss_gamma_x = x_p_sq_avg / eps_rms_x
        
        twiss_alpha_x = math.sqrt((twiss_beta_x * twiss_gamma_x - 1))
        
        twiss_beta_y = y_sq_avg / eps_rms_y
        
        twiss_gamma_y = y_p_sq_avg / eps_rms_y
        
        twiss_alpha_y = math.sqrt((twiss_beta_y * twiss_gamma_y - 1))
    
        # print everything
        
        print("non-normalized rms emittance x", eps_rms_x)
        print("non-normalized rms emittance y", eps_rms_y)
        print("normalized rms emittance x", eps_norm_x)
        print("normalized rms emittance y", eps_norm_y)
        print("alpha x", twiss_alpha_x)
        print("beta x", twiss_beta_x)
        print("gamma x", twiss_gamma_x)
        print("alpha y", twiss_alpha_y)
        print("beta y", twiss_beta_y)
        print("gamma y", twiss_gamma_y)
    
        return eps_rms_x, eps_rms_y, eps_norm_x, eps_norm_y, twiss_beta_x, twiss_gamma_x, twiss_alpha_x, twiss_beta_y, twiss_gamma_y, twiss_alpha_y

    emittance_calc(x_avg, x_p_avg, x_sq_avg, x_p_sq_avg, x_x_p_avg, y_avg, y_p_avg, y_sq_avg, y_p_sq_avg, y_y_p_avg)

    eps_rms_x, eps_rms_y, eps_norm_x, eps_norm_y, twiss_beta_x, twiss_gamma_x, twiss_alpha_x, twiss_beta_y, twiss_gamma_y, twiss_alpha_y = emittance_calc(x_avg, x_p_avg, x_sq_avg, x_p_sq_avg, x_x_p_avg, y_avg, y_p_avg, y_sq_avg, y_p_sq_avg, y_y_p_avg)

    data = pd.read_excel(r'C:\Users\mizam\rotated_beamlets_for_133Cs26.xls') 
            
#    data['y_prime'] = data.y_prime_times_L / L  # adding y_prime and x_prime properly into the dataframe
    
#    data['x_prime'] = data.x_prime_times_L / L
        
    y_pos, x_pos, I_pix, x_p, y_p = import_data(res, L)  
    
    data = pd.read_excel(r'C:\Users\mizam\rotated_beamlets_for_133Cs26.xls') 

    data['y_prime'] = data.y_prime_times_L / L  # adding y_prime and x_prime properly into the dataframe

    data['x_prime'] = data.x_prime_times_L / L
    
    def make_heatmap():
        
        # make pretty heatmaps to show the phase space and then overlay ellipses generated by the twiss parameters to show that the parameters are a good match
        
        phase_space = data.pivot("y_pos", "y_prime", "I_pix")
        
        sns.heatmap(phase_space)
        
        print(phase_space)
        
#        trace = go.Heatmap(
#            x = y_pos,
#            y = y_p,
#            z = I_pix,
#            type = 'heatmap',
#            colorscale = 'Viridis'
#        )
#        data = [trace]
#        fig = go.Figure(data = data)

        
#        fig = px.density_heatmap(phase_space, x="y_pos", y="y_prime", color="intensity")
    
#        fig.update_layout(coloraxis_showscale=False)
    
#        fig.show()
        
    make_heatmap()
    
pep()
