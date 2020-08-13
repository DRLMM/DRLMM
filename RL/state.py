# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 16:17:12 2020

@author: huyue
"""


class state():
    
    def __init__(self,config,is_terminal = False):
        
        self.n_actions = config['learning']['n_actions']
        self.is_terminal = is_terminal
    
    def new_state(self,env):
        pass
    
    def populate_features(self):
        pass
    
    def print_state(self):
        
    
class action():
    pass


class 