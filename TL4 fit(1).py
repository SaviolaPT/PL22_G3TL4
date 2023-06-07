import numpy as np
import matplotlib.pyplot as plt
import uncertainties
from scipy.optimize import curve_fit
def readtabela(tabela):
    """Reads a .txt where each line is in the format: "first entry" "second entry", where the first and
       second entry are separated by a blank space " ".
       The first entry corresponds to the time since the measuring started
       The second entry corresponds to the value registered
       Returns two lists, one with the values of the first entries, another with the values of the second
       entries
       Args:
       tabela (string): name of the file
    """
    file1=open(tabela, "r")
    texto=file1.readlines()
    Tempos=[]
    Velocidades=[]
    for i in texto:
        Tempos.append(float(i.split(" ")[0]))
        Velocidades.append(float(i.split(" ")[1]))
    return Tempos, Velocidades
def v(t,v0,l,a):
    """maximum velocity at the moment t

    Args:
        t (float): time
        v0 (float): initial velocity
        l (float): lambda, friction coefficient
        a (float): friction acceleration
    """
    return v0*np.exp(-t*l)-a*t



def ajuste(dados,lim):
    """Finds the fit for the function v according to the given data.

    Args:
        dados (string): name of the file with the data
        lim (list): upper boundaries of the adjust parameters

    Returns:
        list,list,string: returns a list of the parameters, a list of the uncertainties and the name of the file 
    """
    nome = "{}" .format(dados[:-4])
    
    t,vel=readtabela(dados)
    values,pcov=curve_fit(v,t,vel,bounds=[0,lim])
    v0,l,a=values
    perr = np.sqrt(np.diag(pcov))
    dp_v0,dp_l,dp_a=perr
    param=[t,vel,v0,l,a]
    incert=[dp_v0,dp_l,dp_a]
     
    return param,incert,nome

def plot(param,incert,nome):
    """makes a graphic of the adjusted curve

    Args:
        param (list): list of the parameters
        incert (list): list of the uncertainties
        nome (string): name of the file
    """
    
    t=param[0]
    vel=param[1]
    v0=param[2]
    l=param[3]
    a=param[4]
    tempos=np.linspace(t[0],t[-1],1000)
    y=[]
    for i in tempos:
        y.append(v(i,v0,l,a))
    texto_graph=f"$v_0$={uncertainties.ufloat(v0,incert[0])}$m/s$\n $\u03BB$={uncertainties.ufloat(l,incert[1])}$s^{{-1}}$\n $a$={uncertainties.ufloat(a,incert[2])}$m/s^2$"
    
    
    fig1= plt.figure(1)
    plt.scatter(t,vel,color="green",marker="x")
    plt.plot(tempos,y,color="orange",marker=" ")
    plt.title("Ajuste aos dados para I={}".format(nome)) 
    plt.xlabel("Tempo(s)")
    plt.ylabel("Velocidade máxima (m/s)")
    plt.grid()
    plt.annotate(texto_graph, xy=(0.5, 0.77), xycoords='axes fraction', weight='bold',bbox=dict(boxstyle="square",fc="lightblue",ec="steelblue",lw=2))
    fig1.savefig("python {}.pdf".format(nome))    
    plt.show()
    plt.close()        
        

## For I=0,10A
lim=[0.9,0.02,0.08]
param,incert,nome=ajuste("I010A.txt",lim)
plot(param,incert,nome)


## For I=0,25A
lim=[0.9,0.09,0.09]
param,incert,nome=ajuste("I025A.txt",lim)
plot(param,incert,nome)

## For I=0,35A
lim=[0.9,0.3,0.09]
param,incert,nome=ajuste("I035A.txt",lim)
plot(param,incert,nome)


##For I=0,50A
lim=[0.9,0.33,0.0015]
param,incert,nome=ajuste("I050A.txt",lim)
lim=[0.9,0.32,0.0015]
param1,incert1,nome1=ajuste("I050A1.txt",lim)
lim=[0.9,0.33,0.0015]
param2,incert2,nome2=ajuste("I050A2.txt",lim)
lim=[0.9,0.33,0.0015]
param3,incert3,nome3=ajuste("I050A3.txt",lim)

for i in range(2,len(param)):
    param[i]=(param1[i]+param2[i]+param3[i])/3
    incert[i-2]=np.sqrt(incert1[i-2]**2+incert2[i-2]**2+incert3[i-2]**2)/3
    
plot(param,incert,nome)
