import numpy as np 
import time
import matplotlib.pyplot as plt 

from Crowd.AllocationSolver import AllocationSolver
from Crowd.Peoples import People


class World1D(object):
    """
        Put limits, collect all variables and make them interact 
    """
    def __init__(self, l, allocator = None, pos_out = None):
        self.l = l                       # Définir la taille du monde 
        self.peoples = []                # Tableau dans lequel on stockera tout les individus qui évoluent dans le monde 
        self.peoples_out = []            # Tableau dans lequel on stockera tout les individus qui sont sortis du monde 
        self.pos_out = [l-1] if pos_out is None else pos_out   # Position de la sortie 
        
        self.allocator = AllocationSolver() if allocator is None else allocator
        
        # Stats
        self.elapsed_time = None
        self.round = 0
        
        
    def add_people(self, p):
        """
            Add peoples to the list of peoples that are in the World
        """
        self.peoples.append(p)
 

#
# Main function 
#
    
    def live_round(self):
        """
            Give its new position to every individuals, put out individual that take the exit 
        """
        
        # Alloue les nouvelles positions 
        wills, now = self.allocator.solve(self.peoples)
        
        # Donne à chaque individus sa nouvelle position 
        for i, p in enumerate(self.peoples):
            p.set_pos(now[i])
        
        # Sort celui qui est sur la porte (ou ceux au premier tour) 
        self.expulse()
        
        self.round += 1 
        
        
        
    def expulse(self):
        """
            Under the pos_in condition, put someone out of the world by deleting him from people and pu
        """
        for i, p in enumerate(self.peoples):
            if p.pos == self.pos_out:
                self.peoples_out.append(p)
                del self.peoples[i]
                  
    
    def pos_in(self, pos):
        """
            Check that the position is inside the World 
        """
        if pos == self.pos_out :
            return True 
        else :
            return pos[0] < self.l and 0 <= pos[0] 
              
    
    
#
# Running and diplaying    
#
    
    def show(self):
        """
            Handle the displaying in 1D, ____X___ where X is the logo of a people
        """
        res = ["_"] * self.l #chaîne caractère, ie liste de caractère séparées 
        for p in self.peoples:
            res[int(p.pos[0])] = p.logo
        print("".join(res), end="\r") # join permet de coller les caractères 
        

    
    def animate(self, T):
        """
            Display in 1D, makes all run 
        """
        self.show()
        for t in range(T):
            time.sleep(0.1)
            self.live_round()
            self.show()
            
            
    def simulate(self):
        """
            Run everything without diplaying 
        """
        start_time = time.time()
        while len(self.peoples) != 0 :
            self.live_round()
        self.elapsed_time = time.time() - start_time
        return self.elapsed_time

            
  
    
#
# Passage en 2D 
#
 
    
class World2D(World1D):
    """ 
        Transition towards multiple dimension
    """
    
    def __init__(self, l, allocator = None, pos_out=[0,0]):
        super(World2D, self).__init__(l, allocator, pos_out)
            
            
    def pos_in(self, pos):
        return (np.absolute(pos) < self.l).all() and pos != self.pos_out
    
        
    def add_random_people(self, n):
        for i in range(n):
            pos_lim = self.l - 1
            pos_random = np.random.randint(-pos_lim, pos_lim, (1,2))[0]
            People(pos = list(pos_random), world = self, speed = 1)
        
        
    def plot_paths(self):
        plt.figure()
        plt.title("Chemins parcourus")
        plt.grid(True)
        plt.xticks(range(-self.l, self.l))
        plt.yticks(range(-self.l, self.l))
        plt.xlim(-self.l, self.l)
        plt.ylim(-self.l, self.l)
        plt.scatter(self.pos_out[0], self.pos_out[1], marker="*", s=200)
        
        for p in self.peoples_out:
            X= np.array(p.path)
            plt.plot(X[:,0], X[:,1])

            
    
    