import numpy as np
import matplotlib.pyplot as plt 
from math import sqrt

from Crowd.Worlds import * 
from Crowd.Peoples import * 
from Crowd.AllocationSolver import *

import matplotlib.animation as animation

###########################################################################

#
#   Création de trois monde et évacuation de ceux-ci
#   Ces trois mondes ont leur sortie en différentes positions, 
#   l'une au centre, l'une en coin et la dernière sur un bord au milieu
#


def generate_data(W, pos_out):
    N = range(5, 100)
    K = 10
    
    for n in N:
        print(n)
        if n not in W: W[n] = [] # Initialisation
        
        for k in range(K):
            w = World2D(20, pos_out = pos_out)
            w.add_random_people(n)
            w.simulate()
            W[n].append(w)
            
    return W

W_center = generate_data({}, [0,0])
W_side_center = generate_data({}, [19,0])
W_coin = generate_data({}, [19,19])




###########################################################################

def plot(W, get_value, label, color = "red"):
    N = W.keys()
    T = np.zeros(len(N))
    V = np.zeros(len(N))
    
    for i, n in enumerate(N):
        print(n)
        K = len(W[n])
        
        T_n = np.zeros(K)
        for k, w in enumerate(W[n]):
            T_n[k] = get_value(w)
            
        V[i] = np.std(T_n)*1.96/sqrt(K)
        T[i] = np.mean(T_n)
        
    plt.plot(N, T, color = color, label = label)
    plt.fill_between(N, T-V, T+V, alpha = 0.5, color = color)


def plot_all_W(get_value, title, ylabel):
    global W_center, W_side_center, W_coin
    plt.figure()
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Nombre de personne")
    plt.grid(True)
    
    plot(W_center, get_value, label="center", color="red")
    plot(W_side_center, get_value, label="side_center", color="blue")
    plot(W_coin, get_value, label="coin", color="green")
    plt.legend()
    

    
###########################################################################

get_value = lambda w : w.elapsed_time
plot_all_W(get_value, "Temps d'execution", "Temps")
    
get_value = lambda w : w.round
plot_all_W(get_value, "Temps d'évacuation", "Temps")
    
    
def get_value_angry(w):
    angry = []
    for p in w.peoples_out :
        angry.append(p.angryness)
    return np.mean(angry)
plot_all_W(get_value_angry, "Niveau de colère des personnes", "Niveau de colère")

#########################################################################
    
w = World2D(20, pos_out = [0,19])
w.add_random_people(100)
w.simulate()

w.plot_paths()
    
###########################################################################



