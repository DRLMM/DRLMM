# -*- coding: utf-8 -*-

import numpy as np

from simulator.exchange import Exchange
from RL.environment.state import state
from RL.environment.state import state
from RL.environment.action import action
from RL.environment.reward import Reward




ASK = "ASK"
BID = "BID"

class MarketMaking(object):
    
    def __init__(self,config):
        
        self.n_actions = 10
        self.ORDER_SIZE = 1
        self.Ag_exchange = Exchange('../data/')
        
        self.Ag_exchange.init_exchange()
        self.Ag_exchange.init_agent(10000,0)
        self.state_dict = state(config)
        self.rewards = Reward(config)
        
    def reset(self):
        
        init_state = np.array(list(self.state_dict.initialise()))
        #init_action = np.random.randint(0,10)
        
        return init_state
    
    # execute the action
    def step(self,state,action_id):
        
    
        last_midprice = self.Ag_exchange.get_mid_price()
        reward = 0
        
        act = action(action_id)
        ask_price,bid_price =  self.Ag_exchange.get_price()
        ask_quote,bid_quote = act.get_order_quote(ask_price,bid_price)
        ask_volume = self.ORDER_SIZE
        bid_volume = self.ORDER_SIZE
        
        self.Ag_exchange.send_action(ASK,ask_quote,ask_volume)
        self.Ag_exchange.send_action(BID,bid_quote,bid_volume)
        
        self.Ag_exchange.update_state()
        inventory =  self.Ag_exchange.position
        total_ask_volume,total_bid_volume =  self.Ag_exchange.get_total_volume()
        midprice = self.Ag_exchange.get_mid_price()
        ask_price,bid_price =  self.Ag_exchange.get_price()
        
        #calculate the reward
        reward = self.rewards.get_reward(ask_quote,ask_volume,bid_quote,bid_volume,inventory,midprice,last_midprice)
        
        
        # new state
        self.state_dict.get_pos(inventory)
        self.state_dict.get_mpm(midprice,last_midprice)
        self.state_dict.get_spd(ask_price,bid_price)
        self.state_dict.get_imb(total_ask_volume,total_bid_volume)
        self.state_dict.get_a_dist(ask_quote,ask_price)
        self.state_dict.get_b_dist(bid_quote,bid_price)
        self.state_dict.get_vol(ask_price,bid_price)
        self.state_dict.get_rsi(midprice,last_midprice)
        
        next_state = np.array(list(self.state_dict.get_state()))
        
        is_terminal = False
   
        return next_state,reward,is_terminal
    
    def is_done(self):
        pass
    
    def render(self):
        return 0