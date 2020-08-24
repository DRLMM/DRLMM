# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 16:17:12 2020

@author: huyue
"""


class state():
    
    
    def __init__(self):
        
        # 自身状态
        self.pos = 0
        self.a_dist = 0
        self.b_dist = 0
        self.spd = 0  # 0-20之间
        
        
        #市场状态
        self.mpm = 0
        self.imb = 0
        self.svl = 0
        self.vol = 0 # 0-10之间
        self.rsi = 0
        
    
    def get_state(self,config,is_terminal = False):
        
        self.n_actions = config['learning']['n_actions']
        self.ORDER_SISE = 1
        
        self.pos = self.get_pos() # 风险暴露
        self.spread = self.get_spread()
        self.midprice_move = self.get_mpm()
        self.imbalance = self.get_imb(5,6)
        self.svl = self.get_svl()
        self.vol = self.get_vol()
        self.rsi = self.get_rsi()
        self.a_dist = 0
        self.b_dist = 0
        self.last_action = 5
        self.is_terminal = is_terminal
    
    def new_state(self,env):
        pass
    
    def populate_features(self):
        pass
    
    def print_state(self):
        print()
    
    def get_spread(self):
        a1 = 1
        b1= 1
        return a1 - b1
        
    def get_pos(self):
        exposure = 2
        
        return exposure / self.ORDER_SISE
    
    def get_imb(self,ask_volume,bid_volume):
        
        v_a = ask_volume
        v_b = bid_volume
        
        if ((v_a + v_b) > 0):
            imb= 5* (v_b - v_a) /(v_b + v_a)
            
        else:
            imb = 0
        
        return imb
    
    def get_mpm(self):
        max_midprice = 2
        min_midprice = 1
        return max_midprice - min_midprice
    
    def get_svl(self):
        q_a = 5
        q_b = 2
        
        if ((q_a + q_b ) > 0):
            svl = 5 * (q_b - q_a) /(q_a + q_b)
            
        else:  
            svl = 0
            
        return svl
    
    def get_vol(self):
        
        volatility = 0.05
        
        return 5.0 * volatility
    
    def get_rsi(self):
        
        u = 1
        d = 0.5
        
        if ((u+d) != 0):
            rsi = 5.0 * (u-d) / (u + d)
            
        else:
            rsi = 0
            
        return rsi