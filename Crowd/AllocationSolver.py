import numpy as np
import time 


def pos_to_id(pos):
    """
        Transfrom a position to a unique key for a dictionary
    """
    res = ""
    for x in pos:
        res += '_' + str(x)
    return(res)    


def fight_method_default(id_perss, perss):
    """
        This is the default method of fighting
        Just pick a random person from the fighters.
        This does not use any characteristec (so no use of perss)
        Later the aim would be to use special characteristic to select the winner
    """
    i = np.random.randint(0,len(id_perss))
    return id_perss[i]


def fight_method_angry(id_perss, perss):
    """
        This is an advanced fight method
        This use the angryness atribut of people to determine which one will win
    """
    max_level = None
    for id_pers in id_perss:
        p_level = perss[id_pers].angryness # Level of angryness of "id_pers"
        
        if max_level is None or max_level < p_level: #Strictly better
            max_level, angry_peoples = p_level, [id_pers]
        elif max_level == p_level: #Same level
            angry_peoples.append(id_pers)
            
    # Picking a random one from the most angry
    i = np.random.randint(0,len(angry_peoples))
    return angry_peoples[i]
            
        
    

    
class AllocationSolver:
    """
        Manage all the allocation and find the one matching all requirement.
    """

    def __init__(self, fight_method = None):
        """
            Init method to store parameters
        """
        
        # Function of selection for a position
        self.fight_method =  fight_method_default if fight_method is None else fight_method
        
        
#
#  Interface function
#
    def solve(self, perss):
        """
            Solve the alocation problem for all person (class People) in "perss" 
        """
        self.perss = perss # People to allocate
        
        self.set_param() # Initiate the variable "wills" and "now"
        
        self.war() # Handle conflict of wills

        # Move everyone if possible (handles cycle)
        for pos in self.now:
            self.move(pos) # Recursive function
            
        return self.wills, self.now # Solution of the problem

    
#
#  Solving function
#   

    def set_param(self):
        """
            Recupere tous les voeux et les positions actuels.
            Chaque individu est identifié par son index dans ce tableau (qui est unique)
        """
        self.now, self.wills = [], []
        for p in self.perss:
            self.now.append(p.pos)
            self.wills.append(p.get_will())  
        return self
    
    
    def war(self):
        """
            Réalise tout les combats et répertorie qui a droit de changer de place ou nom
        """
        # Store all the conflict
        fights = self.get_same_wills() 
        
        # Solve each conflict one by one with the method "fight_method"
        for id_pos, id_perss in fights.items():
            
            # On execute le combat et on récupère l'id du gagnant
            one = self.fight_method(id_perss, self.perss)
            
            # On met tous les voeux des refusés à None ce qui revient à refuser son voeu
            for id_pers in id_perss:
                if id_pers != one: self.wills[id_pers] = None
                    
        return self


    def move(self, pos, moving = None):
        """
            Move regarde si la place ou la personne veut aller est libre
                et sinon si la personne qui y est veut bouger. 
            Comme les combats ont été gérés on sait qu'il n'y a
                plus de combats pour prendre la place. 
            Si la personne peut prendre la place, move répond True et modifie now.         
        """
        now, wills = self.now, self.wills #Shortcut
        pos = list(pos)
        
        moving = [] if moving is None else moving # Handle issue with pointer if "moving = []"
        if pos in now:
            p_id = now.index(pos) # Personne sur la case
            will = wills[p_id] # Voeux de la personne

            if will == pos or will is None: # Il souhaite ne pas bouger
                return False

            if p_id in moving: # Gère le cas de la boucle 
                now[p_id] = will
                return True

            else: # Il veut aller quelque part
                moving.append(p_id)
                is_empty = self.move(will, moving) # On essaie de vider la case voulue
                if (is_empty):
                    now[p_id] = will
                    return True
                else:
                    return False

        else:     # Il n'y a personne et la position est dans le monde 
            return True
    
    
    
#
#  Utilities
#
       
    def get_same_wills(self):
        """
            Répertorie dans un dictionnaire toutes les positions demandees et qui les demande
        """
        d = {}
        
        for id_pers, pos in enumerate(self.wills):
            # On transforme la position en une clé pour le dictionnaire
            id_pos = pos_to_id(pos)
            
            if id_pos in d:
                # Ajoute la personne à la liste des personnes ayant le voeu "will" dont la clé est "id_pos"
                d[id_pos].append(id_pers)
           
            else:
                # Pour une position nouvelle, crée la nouvelle clé dans le dictionnaire d 
                d[id_pos] = [id_pers] 
        
        return d