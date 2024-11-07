import numpy as np

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


pf=49.3 #lbm/ft3
pg=0.0765 #lbm/ft^3
prcit=
g= 32.2 #ft/s^2
gc = 32.2
sigma = #lbf/ft
#Calcs From Data


A=np.pi*rad**2
mf=pf*jl*A
mg=pg*jg*A
P= np.pi*rad*2
Dh=4*A/P

Ref=mf*Dh/(A*muf)
Reg=mg*Dh/(A*mug)

D1 = .125 #ft Normalizing Diameter
D2= .3 #ft Normalizing Diameter

Re= max([Reg,Ref])

if Reg >= 0:
    Fr= (90-theta)/10
    C1=4*pcrit**2/(p*(pcrit-p))
 #for steam-water
    A1= 1/ [1+np.exp(-Re/60000)] # if Reg >Ref or Reg <0, otherwise Ref used instead
    B1= min ([.8, A1])
    K1=B1
    r=(1+1.57*pg/pf)(1-B1)

    C5=np.sqrt(150*(pg/pf))
    C6 = C5/(1-C5)

    if C5>=1:
        C2= 1
    else:
        C2=1/(1-np.exp(-C6))

    if upflow is True:

        C3 = max([0.50, 2*np.exp(-np.abs(Ref) 1/60,000)])
    else:
        C3 = 2*np.exp(np.abs(Ref)/350000)**.4-1.75*np.abs(Ref)**.03*np.exp(-np.abs(Ref)/50000*(D1/Dh)**2)+(D1/Dh)**.25*np.abs(Ref)**.001
    C7=(D2/Dh)**.6 
    C8 = C7/(1-C7)

    if C7 >= 1:
        C4=1
    else:
        C4 = 1/(1-np.exp(-C8))





    L = (1-np.exp(-C1*alpha))/(1-np.exp(-C1))
    Vgj=1.41*((pf-pg)*sigma*g*gc/pf**2)**(1/4)*(1-alpha)**K1*C2*C3*C4
    K0= B1+(1-B1)*(pg/pf)**(1/4)
    Cov= L/(K0 + (1-K0)*alpha**r)
    Coh=((1+alpha**.05)*(1-alpha)**2)Cov
    Co=Fr*Cov+(1-Fr)*Coh






else:
    Fr=max([1,(90-theta/10)])






# Vgj= (jg*alpha*Co*(jg+jf)/alpha)
# alpha=
