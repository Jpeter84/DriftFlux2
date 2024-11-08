import numpy as np
import pandas as pd
from icecream import ic
#Variables Defined
# Jg = superficial gas velocity
# Jl = superficial liquid velocity
# mug = viscosity of gas (lb/ft-sec)
# muf = viscosity of liquid
# A = Area of pipe (ft^2)
# mg= mass flow rate of vapor (must match units of mug, A, Dh)
# mf = mass flow rate of liquid
# theta= angle of inclination
# Cov = C0 for verticle
# L = Chexel-Lelloche Number
# sigma= surface tension
# pf = saturated density of fluid (lb/ft^3)
# pg = density of gas
# DH = hydraulic diameter (ft)

##Chexal


#Predefined

#Define from excel
#rad = radius
#jl = superficial liquid velocity
#jg = superifical gas velocity
#theta = inclination angle
#p = average pressure
# upflow boolian


excel_page = pd.read_excel('kokal_results.xlsx', sheet_name=None,skiprows=1)  # sheet_name=None loads all sheets


for sheet_name, sheet_df in excel_page.items():
    print(f"Processing sheet: {sheet_name}")

    rad = float(sheet_name.split('D')[1].split('_')[0])*0.00328084 #ft


    theta = float(sheet_name.split('angle')[1])
    ic(theta)
    if theta >= 0:
        upflow = True
    for col_name in sheet_df.columns:


        jl=sheet_df.iloc[1][col_name]*3.28084
        jg=sheet_df.iloc[2][col_name]*3.28084
        p=sheet_df.iloc[12][col_name]*20.885434273039








        pf=49.3 #lbm/ft3
        pg=0.0765 #lbm/ft^3
        pcrit=33*2116
        g= 32.2 #ft/s^2
        gc = 32.2
        sigma = 0.000171304414883076*12 #lbf/ft
        #Calcs From Data


        A=np.pi*rad**2
        mf=pf*jl*A
        mg=pg*jg*A
        P= np.pi*rad*2
        Dh=4*A/P
        muf=0.00695*0.67197
        mug=18.3*10**6*0.67197 #lb/ft-s

        Ref=mf*Dh/(A*muf)
        Reg=mg*Dh/(A*mug)

        D1 = .125 #ft Normalizing Diameter
        D2= .3 #ft Normalizing Diameter

        Re= max([Reg,Ref])


        Fr= (90-theta)/10
        C1=4*pcrit**2/(p*(pcrit-p))
        #for steam-water
        A1= 1/ (1+np.exp(-Re/60000)) # if Reg >Ref or Reg <0, otherwise Ref used instead
        B1= min ([.8, A1])
        K1=B1
        r=(1+1.57*pg/pf)*(1-B1)

        C5=np.sqrt(150*(pg/pf))
        C6 = C5/(1-C5)

        if C5>=1:
            C2 = 1
        else:
            C2=1/(1-np.exp(-C6))

        if upflow is True:

            C3 = max([0.50, 2*np.exp(-np.abs(Ref)* 1/60000)])
        else:
            C3 = 2*np.exp(np.abs(Ref)/350000)**.4-1.75*np.abs(Ref)**.03*np.exp(-np.abs(Ref)/50000*(D1/Dh)**2)+(D1/Dh)**.25*np.abs(Ref)**.001
        C7=(D2/Dh)**.6 
        C8 = C7/(1-C7)

        if C7 >= 1:
            C4=1
        else:
            C4 = 1/(1-np.exp(-C8))

        relaxation_factor = 0.5  # Damping factor (0 < relaxation_factor < 1)
        alpha = 0.5  # Initial guess, should be between 0 and 1
        tolerance = 1e-6  # Convergence tolerance
        max_iterations = 10000  # Maximum number of iterations

# To keep alpha within the range [0, 1]
        def clamp(value):
            return max(0, min(value, 1))

        # Iterative loop
        for iteration in range(max_iterations):
            # Calculate intermediate values
            L = (1 - np.exp(-C1 * alpha)) / (1 - np.exp(-C1))
            Vgj = 1.41 * ((pf - pg) * sigma * g * gc / pf**2)**(1/4) * (1 - alpha)**K1 * C2 * C3 * C4
            K0 = B1 + (1 - B1) * (pg / pf)**(1/4)
            Cov = L / (K0 + (1 - K0) * alpha**r)
            Coh = ((1 + alpha**0.05) * (1 - alpha)**2) * Cov
            Co = Fr * Cov + (1 - Fr) * Coh

            # Calculate the new value for alpha based on the equation
            new_alpha = jg / (Co * (jg + jl) + Vgj)
            
            # Apply relaxation to smooth the update (step size control)
            alpha = alpha + relaxation_factor * (new_alpha - alpha)
            
            # Ensure alpha stays within the range [0, 1]
            alpha = clamp(alpha)

            # Check for convergence
            if abs(new_alpha - alpha) < tolerance:
                print(f'Converged to alpha = {alpha} after {iteration + 1} iterations.')
                break
        else:
            print(f"Did not converge after {max_iterations} iterations.")

        # Final value of alpha
        print(f"Final value of alpha: {alpha}")

        # alpha = 0.0005  # Initial guess, should be between 0 and 1
        # tolerance = 1e-6  # Convergence tolerance
        # max_iterations = 1000  # Maximum number of iterations

        # for iteration in range(max_iterations):
        #     # Calculate intermediate values
        #     L = (1 - np.exp(-C1 * alpha)) / (1 - np.exp(-C1))
        #     Vgj = 1.41 * ((pf - pg) * sigma * g * gc / pf**2)**(1/4) * (1 - alpha)**K1 * C2 * C3 * C4
        #     K0 = B1 + (1 - B1) * (pg / pf)**(1/4)
        #     Cov = L / (K0 + (1 - K0) * alpha**r)
        #     Coh = ((1 + alpha**0.05) * (1 - alpha)**2) * Cov
        #     Co = Fr * Cov + (1 - Fr) * Coh

        #     # Update alpha based on the equation
        #     new_alpha = jg / (Co * (jg + jl) + Vgj)
            
        #     # Check for convergence
        #     if abs(new_alpha - alpha) < tolerance:
        #         print(f'Converged to alpha = {new_alpha} after {iteration + 1} iterations.')
        #         alpha = new_alpha
        #         break
            
        #     # Update alpha for the next iteration
        #     alpha = new_alpha
        # else:
        #     print(f"Did not converge after {max_iterations} iterations.")

        # # Final value of alpha
        # print(f"Final value of alpha: {alpha}")


