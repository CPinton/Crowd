import numpy as np
import matplotlib.pyplot as plt 

from Crowd.Worlds import * 
from Crowd.Peoples import * 
from Crowd.AllocationSolver import *

import matplotlib.animation as animation

w = World2D(20)
w.add_random_people(200)


#
# Affichage 2D 
#

    
fig, ax = plt.subplots()
def animate(i):
    w.live_round()
    ax.clear()
    plt.grid(True)
    plt.xticks(range(-w.l, w.l))
    plt.yticks(range(-w.l, w.l))
    plt.xlim(-w.l, w.l)
    plt.ylim(-w.l, w.l)
    ax.scatter(w.pos_out[0], w.pos_out[1], marker="*", s=200)
    for p in w.peoples:
        ax.scatter(p.pos[0], p.pos[1], marker="x", s = 100)

ani = animation.FuncAnimation(fig, animate, [0,1], interval=500)
plt.show()