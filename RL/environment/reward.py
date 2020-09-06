# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 16:06:15 2020

@author: huyue
"""
"""
需要的数据：t-1时刻双边报价的价格和数量，t时刻的存货数量，t时刻中间价格，t-1时刻中间价格
"""
import numpy as np

class Reward(object):
    
    def __init__(self,config):
        
        self.reward_measure = config['reward']['reward_measure']
        self.damping_factor = float(config['reward']['damping_factor'])
        self.reward = 0
        
    def get_reward(self,ask_quote_price,ask_volume,bid_quote_price,bid_volume,inventory,midprice,last_midprice):
        self.ask_quote_price = ask_quote_price
        self.bid_quote_price = bid_quote_price
        self.ask_volume = ask_volume
        self.bid_volume = bid_volume
        self.midprice = midprice
        self.midprice_move =  midprice - last_midprice
        
        self.momentum_pnl_step = inventory * self.midprice_move
        
        if (self.reward_measure == "pnl"):
            reward = self.get_pnl() 
            
        elif(self.reward_measure == "pnl_sdamped"):
            reward = self.get_sym_damped_pnl()
        
        elif(self.reward_measure == "pnl_adamped"):
            reward = self.get_asym_damped_pnl()
            
        return reward
    
    def get_pnl(self):
        
        r = self.ask_volume * (self.ask_quote_price - self.midprice) + self.bid_volume * (self.midprice - self.bid_quote_price)
        
        r = r + self.momentum_pnl_step
        return r
    
    
    def get_sym_damped_pnl(self):
        
          
        pnl_step = self.get_pnl()
        r = pnl_step -self.damping_factor * self.momentum_pnl_step
        return r
    
    def get_asym_damped_pnl(self):
        
        pnl_step = self.get_pnl()
        r = pnl_step -self.damping_factor * np.max([0, self.momentum_pnl_step])    
        return r
    
    
#%% 

