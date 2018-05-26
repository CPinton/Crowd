import numpy as np 

from Crowd.Peoples import * 

class People(object):
    def __init__(self, pos, world, logo = "X", speed = 1):
        """
            Création of individuals with them caractéristics
        """
        self.pos = pos
        self.logo = logo
        self.speed = speed
        self.world = world
        world.add_people(self)
        
        # Stats
        self.angryness = 0
        self.path = [self.pos]
                 
            
    def get_will(self): # L'individu demande à prendre sa position suivante, le monde va gérer qui gagne les combats
        if self.pos == self.world.pos_out:
            return self.world.pos_out
        
        direction = np.array(self.world.pos_out) - np.array(self.pos)
        pas_pur = np.linalg.norm(direction)
        fac = min(self.speed,pas_pur)
        pas = (direction/pas_pur) * fac
        return list(np.round(np.array(self.pos) + pas))
    
    
    def set_pos(self, pos):
        if self.pos == pos:
            self.angryness += 1
        self.pos = pos
        self.path.append(pos) # on ajoute au tableau data, la nouvelle position de l'individu