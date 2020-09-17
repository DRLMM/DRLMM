# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 16:17:12 2020

@author: huyue
"""
import numpy as np
class State():
    
    
    def __init__(self,config):
        
        self.seq = ['pos','a_dist','b_dist','spd','mpm','imb','vol','rsi']
        self.state_dict = dict.fromkeys(self.seq,0)
        self.volatility = list()
        self.vlt_lookback = int(config['state']['vlt_lookback'])
        self.rsi_lookback = int(config['state']['vlt_lookback'])
        
        self.return_ups = list()
        self.return_downs = list()
        
        self.n_actions = int(config['learning']['action_size'])
        self.ORDER_SISE = 1

        self.is_terminal = False
        
    def initialise(self):
        self.state_dict = dict.fromkeys(self.seq,0)
        return self.state_dict.values()
        
    
    def get_state(self,is_terminal = False):
        self.is_terminal = is_terminal
        return self.state_dict.values()
    
    def get_pos(self,inventory):
        """
        仓位
        """
        self.state_dict['pos'] = inventory / self.ORDER_SISE
        return self.state_dict['pos']
        
    def get_mpm(self,midprice,last_midprice):
        """
        中间价移动量
        """
        self.state_dict['mpm'] = midprice - last_midprice
        return self.state_dict['mpm']
       
    def get_spd(self,ask_price,bid_price):
        """
        价差
        """
        self.state_dict['spd'] = (ask_price - bid_price) / 2
        return self.state_dict['spd']
        
    
    def get_imb(self,total_ask_volume,total_bid_volume):
        """
        total_ask_volume： a1-a5的volume,
        total_bid_volume:  b1-b5的volume
        一般来说，就数据而言，买单比卖单多
        """
        v_a = total_ask_volume
        v_b = total_bid_volume
        
        if ((v_a + v_b) > 0):
            imb= 5* (v_b - v_a) /(v_b + v_a)  # 算得上归一化嘛？
            
        else:
            imb = 0
        
        self.state_dict['imb'] =  imb
        
    def get_a_dist(self,ask_quote,ask_price):
        """
        所挂卖单与市场中卖单的价差，一般为与挂的卖一与市场中卖一的距离
        """
        self.state_dict['a_dist'] = ask_quote - ask_price
        
    def get_b_dist(self,bid_quote,bid_price):
        """
        所挂买单与市场中买单的价差，一般为与挂的买一与市场中买一的距离
        """
        self.state_dict['a_dist'] = bid_price - bid_quote
    
    
    
    def get_vol(self,ask_price,bid_price):
        """
        中间价序列，波动率
        """
        midprice = (ask_price + bid_price) / 2
        
        if (len(self.volatility) >= self.vlt_lookback):
            self.volatility.pop(0)
        
        self.volatility.append(midprice)
        
        volatility = np.std(self.volatility)
        
        self.state_dict['vol'] = 5.0 * volatility
        return self.state_dict['vol']
    
    def get_rsi(self,midprice,last_midprice):
        """
        相对强弱指标,RSI＝[上升平均数÷(上升平均数＋下跌平均数)]×100
        """
        if (len(self.return_ups) >= self.rsi_lookback):
            self.return_ups.pop(0)
            
        if (len(self.return_downs) >= self.rsi_lookback):
            self.return_downs.pop(0)
        
        midprice_move = midprice - last_midprice
      
        self.return_ups.append(np.max([0,midprice_move]))
        self.return_downs.append(abs(np.min([0,midprice_move])))
        
        u = np.mean(self.return_ups)
        d = np.mean(self.return_downs)
        
        if ((u+d) != 0):
            rsi = 100 * u / (u + d)
            
        else:
            rsi = 0
            
        self.state_dict['rsi'] = rsi
        return self.state_dict['rsi']
    
    def print_state(self):
        
        print(str(self.state_dict))