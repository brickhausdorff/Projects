# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 22:24:42 2020

@author: Nicole Benker
"""

import numpy as np
from scipy import constants as const
import math # this is for the sqrt function

def declare_variables():
    
    global e_amu

    e_amu = 931.5 # rest energy of 1 AMU in MeV

    global c

    c = float(const.c) # speed of light

    global pi

    pi = float(const.pi) #pi

    global degtorad

    degtorad = -0.017453 # -1 degree in radians

    # The following is from res_db and res_params_db for resonator 331:

    op_freq = 109.125 # MHz; resonator operating frequency from RES_VDB::R331:OPERATING_FREQUENCY

    amp_calibrate_intercept = 0 # RES_PARAMS_VDB::R331:AMPLITUDE_CALIBRATE_INTERCEPT

    amp_calibrate_slope = 0.8 # RES_PARAMS_VDB::R331:AMPLITUDE_CALIBRATE_SLOPE

    amp_after_scan = 5.25 # RES_PARAMS_VDB::R331:AMPLITUDE_AFTER_SCAN

    amp_scale_factor = 1 # RES_PARAMS_VDB::R331:AMPLITUDE_SCALE_FACTOR

    cavity_length = 0.355 # RES_PARAMS_VDB::R331:CAVITY_LENGTH
    
    El = (amp_calibrate_intercept + amp_calibrate_slope * amp_after_scan) * amp_scale_factor

declare_variables()

def generate_arrays():

    # tryphi is a series of values of phi, spanning 360 degrees with a step size of 0.1 degree,
    # that will be run through the 200 loops of Uzero to maximize the total energy gain

    tryphi = np.linspace(0, 360, num = 3600)

    # the following are taken from Eax21.dat, corresponding to location and field values for R331 to R338

    z = np.array([-0.1798, -0.1780, -0.1762, -0.1744, -0.1726, -0.1708, -0.1690, -0.1672, -0.1654, -0.1636, 
    -0.1618, -0.1600, -0.1582, -0.1564, -0.1546, -0.1528, -0.1510, -0.1492, -0.1474, -0.1456, -0.1438, -0.1420, 
    -0.1402, -0.1384, -0.1366, -0.1348, -0.1330, -0.1312, -0.1294, -0.1276, -0.1258, -0.1240, -0.1222, -0.1204, 
    -0.1186, -0.1168, -0.1150, -0.1132, -0.1114, -0.1096, -0.1078, -0.1060, -0.1042, -0.1024, -0.1006, -0.0988, 
    -0.0970, -0.0952, -0.0934, -0.0916, -0.0898, -0.0880, -0.0862, -0.0844, -0.0826, -0.0808, -0.0790, -0.0772, 
    -0.0754, -0.0736, -0.0718, -0.0700, -0.0682, -0.0664, -0.0646, -0.0628, -0.0610, -0.0592, -0.0574, -0.0556, 
    -0.0538, -0.0520, -0.0502, -0.0484, -0.0466, -0.0448, -0.0430, -0.0412, -0.0394, -0.0376, -0.0358, -0.0340, 
    -0.0322, -0.0304, -0.0286, -0.0268, -0.0250, -0.0232, -0.0214, -0.0196, -0.0178, -0.0160, -0.0142, -0.0124, 
    -0.0106, -0.0088, -0.0070, -0.0052, -0.0034, -0.0016, 0.0002, 0.0020, 0.0038, 0.0056, 0.0074, 0.0092, 
    0.0110, 0.0128, 0.0146, 0.0164, 0.0182, 0.0200, 0.0218, 0.0236, 0.0254, 0.0272, 0.0290, 0.0308, 0.0326, 
    0.0344, 0.0362, 0.0380, 0.0398, 0.0416, 0.0434, 0.0452, 0.0470, 0.0488, 0.0506, 0.0524, 0.0542, 0.0560, 
    0.0578, 0.0596, 0.0614, 0.0632, 0.0650, 0.0668, 0.0686, 0.0704, 0.0722, 0.0740, 0.0758, 0.0776, 0.0794, 
    0.0812, 0.0830, 0.0848, 0.0866, 0.0884, 0.0902, 0.0920, 0.0938, 0.0956, 0.0974, 0.0992, 0.1010, 0.1028, 
    0.1046, 0.1064, 0.1082, 0.1100, 0.1118, 0.1136, 0.1154, 0.1172, 0.1190, 0.1208, 0.1226, 0.1244, 0.1262, 
    0.1280, 0.1298, 0.1316, 0.1334, 0.1352, 0.1370, 0.1388, 0.1406, 0.1424, 0.1442, 0.1460, 0.1478, 0.1496, 
    0.1514, 0.1532, 0.1550, 0.1568, 0.1586, 0.1604, 0.1622, 0.1640, 0.1658, 0.1676, 0.1694, 0.1712, 0.1730, 
    0.1748, 0.1766, 0.1784])

    Ez = np.array([-1500.7220, -1632.3700, -1736.5730, -2062.5080, -2570.1250, -3278.9890, -4212.1470, -5592.1210, 
    -7269.8620, -9659.2260, -12894.2900, -17050.5600, -22265.7200, -30186.5600, -38808.9300, -52739.3300, -69875.2500, 
    -88384.7700, -122101.1000, -155824.0000, -207150.4000, -268306.0000, -347734.2000, -443900.2000, -561207.0000, 
    -700151.5000, -859881.8000, -1037574.0000, -1228496.0000, -1426467.0000, -1623417.0000, -1816092.0000, -1993002.0000, 
    -2153188.0000, -2296155.0000, -2421572.0000, -2529519.0000, -2617040.0000, -2691747.0000, -2755326.0000, 
    -2809402.0000, -2855128.0000, -2893429.0000, -2927386.0000, -2957775.0000, -2985252.0000, -3010111.0000, 
    -3032615.0000, -3053250.0000, -3071886.0000, -3088288.0000, -3101452.0000, -3110266.0000, -3114230.0000, 
    -3112236.0000, -3103038.0000, -3082388.0000, -3048298.0000, -2999728.0000, -2933991.0000, -2848711.0000, 
    -2740447.0000, -2602857.0000, -2440753.0000, -2255619.0000, -2050409.0000, -1828144.0000, -1599859.0000, 
    -1370397.0000, -1150016.0000, -946618.5000, -765528.6000, -610098.5000, -477631.9000, -373566.9000, 
    -288910.0000, -221109.7000, -167669.1000, -126283.6000, -96467.5000, -73171.3800, -55147.7300, -41338.8000, 
    -30841.7600, -23407.3800, -17690.0900, -13296.1300, -9946.1590, -7407.7480, -5598.2930, -4224.4250, -3167.0390, 
    -2358.3060, -1742.2850, -1293.8280, -950.8864, -678.4512, -461.8516, -283.4275, -128.4833, 15.7846, 161.2475, 
    319.8687, 504.8917, 731.4511, 1022.6530, 1393.5000, 1867.4330, 2498.5550, 3365.7260, 4506.9050, 6000.4200, 
    7940.9060, 10518.7100, 14112.2800, 18851.6100, 25059.7500, 33126.0700, 43685.4300, 58472.7500, 77866.0500, 
    103064.1000, 135482.6000, 176861.5000, 233788.3000, 306112.9000, 396408.3000, 507068.9000, 643567.6000, 
    805372.9000, 991532.7000, 1198666.0000, 1421139.0000, 1651171.0000, 1878195.0000, 2099186.0000, 2299625.0000, 
    2478480.0000, 2633689.0000, 2764505.0000, 2871360.0000, 2951885.0000, 3012317.0000, 3056509.0000, 3086976.0000, 
    3105907.0000, 3114044.0000, 3113954.0000, 3108458.0000, 3098526.0000, 3085005.0000, 3068137.0000, 3048863.0000, 
    3027668.0000, 3004586.0000, 2979552.0000, 2951553.0000, 2920238.0000, 2885010.0000, 2844967.0000, 2799084.0000, 
    2742823.0000, 2676190.0000, 2597646.0000, 2505531.0000, 2397584.0000, 2267002.0000, 2118710.0000, 1953689.0000, 
    1773709.0000, 1579757.0000, 1382312.0000, 1185115.0000, 996269.3000, 821952.1000, 666404.0000, 532053.4000, 
    419364.9000, 328910.0000, 254716.1000, 193559.7000, 148332.2000, 114609.3000, 83197.6300, 66066.9800, 48931.7100, 
    36892.3200, 28270.5200, 21107.0300, 15891.0000, 12099.1500, 9128.0370, 6786.6050, 5250.7550, 4004.7930, 3071.6350, 
    2457.3210, 1949.7050, 1693.5650, 1500.7220])

    print(np.shape(z))
    print(np.shape(Ez))

generate_arrays()

def calculate_gains():
    
    entrance_energy = 132.93 # MeV; exit energy from i = len(z) from previous resonator
    
    energy = np.zeros(200)
    
    beta = np.zeros(200)
    
    time = np.zeros(200)
    
    energy[0] = entrance_energy
    
    beta[0] = math.sqrt(1 - (1 + energy[0] / (e_amu * mass))**2) # where exit_energy_prev = U_out[i-1]
    
    
    for i in range(1, len(z)):
        
        # in the old code beta in resonator_calculation subroutine--which generates the energy on the printout--was btmp + Eztmp * Qdm0c * dz / btmp
            # where btmp was the previous beta (so we're incrementing the old beta by some amount)
            # where Eztmp = El * Ez0(I) <-- from the Eax file * cos(Phitmp)
            # where Phitmp = starts at Phi00 + Poffset and increments by Omc * Dz / Btmp each loop (just before incrementing beta)
            # where Qdm0c = q * 9.580838e7 / (m * c^2)
        
        beta[i] = beta[i-1] + (El * Ez[i] * np.cos(omega * time[i-1] + phi_opt + phi_off) * q * 9.580838e7 * dz) / (beta[i-1] * mass * c**2)
        
        gamma[i] = (1 / math.sqrt(1 - (beta[i])**2))
        
        energy[i] = e_amu * mass * (gamma[i] - 1)
        
        time[i] = time[i-1] + (z[i] - z[i-1]) / (beta[i] * c)
    
calculate_gains()