# -*- coding: utf-8 -*-

import numpy as np
from RL.policy import epsilon_greedy
from simulator.exchange import Exchange
from RL.action import action
from RL.state import state

ASK = "ASK"
BID = "BID"

class environment(object):
    
    def __init__(self,config):
        
        self.n_actions = 10
        self.config = config
        self.ORDER_SIZE = 1
        self.Ag_exchange = Exchange('../data/')
        
        self.Ag_exchange.init_exchange()
        self.Ag_exchange.init_agent(10000,0)
        
    def initialise(self):
        
        self.state = state(self.config)
        self.action = np.random.randint(0,10)
        
        return self.state,self.action
    
    # execute the action
    def step(self,state,action_id,is_terminal = False):

        is_terminal = is_terminal
        reward = 0
        
        act = action(action_id)
        ask_quote,bid_quote = act.get_order_quote()
        ask_volume,bid_volume = self.ORDER_SIZE
        
        self.Ag_exchange.send_action(ASK,ask_quote,ask_volume)
        self.Ag_exchange.send_action(BID,bid_quote,bid_volume)
        
        next_state = state()
        next_state.get_state()
        
        return next_state,reward,is_terminal