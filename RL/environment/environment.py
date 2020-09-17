# -*- coding: utf-8 -*-

import numpy as np

from simulator.exchange import Exchange,PRICE,VOLUME
from RL.environment.state import State
from RL.environment.action import Action
from RL.environment.reward import Reward




ASK = "ASK"
BID = "BID"

class MarketMaking(object):
    
    def __init__(self,config):
        
        self.n_actions = 10
        self.ORDER_SIZE = 1
        self.Ag_exchange = Exchange('data/Ag(T+D)_SGE_TickData_202003/')
        
        self.Ag_exchange.init_exchange()
        self.Ag_exchange.init_agent(500000,100)
        self.state = State(config)
        self.rewards = Reward(config)
        
    def reset(self):
        
        init_state = np.array(list(self.state.initialise()))
        #init_action = np.random.randint(0,10)
        
        return init_state
    
    def step(self,state,action_id):
        """
        excute the action
        """
    
        last_midprice = self.Ag_exchange.get_mid_price()
        reward = 0
        
        # choose action
        act = Action(action_id)

        ask_price,bid_price =  self.Ag_exchange.get_first_price()
        ask_quote,bid_quote = act.get_order_quote(ask_price,bid_price)
        ask_volume = self.ORDER_SIZE
        bid_volume = self.ORDER_SIZE
        
        self.Ag_exchange.send_action(ASK,ask_quote,ask_volume)
        self.Ag_exchange.send_action(BID,bid_quote,bid_volume)
        
        bids_execution,asks_execution = self.Ag_exchange.update_state()
        inventory =  self.Ag_exchange.position
        total_ask_volume,total_bid_volume =  self.Ag_exchange.get_total_volume()
        midprice = self.Ag_exchange.get_mid_price()
        ask_price,bid_price = self.Ag_exchange.get_first_price()
        
        #calculate the reward
        bid_exec_volume = bids_execution[0][VOLUME] if bids_execution else 0
        ask_exec_volume = asks_execution[0][VOLUME] if asks_execution else 0
        reward = self.rewards.get_reward(ask_quote,ask_exec_volume,bid_quote,bid_exec_volume,inventory,midprice,last_midprice)
        
        # new state
        self.state.get_pos(inventory)
        self.state.get_mpm(midprice,last_midprice)
        self.state.get_spd(ask_price,bid_price)
        self.state.get_imb(total_ask_volume,total_bid_volume)
        self.state.get_a_dist(ask_quote,ask_price)
        self.state.get_b_dist(bid_quote,bid_price)
        self.state.get_vol(ask_price,bid_price)
        self.state.get_rsi(midprice,last_midprice)
        
        next_state = np.array(list(self.state.get_state()))
        
        is_terminal = False
   
        return next_state,reward,is_terminal
    
    def is_done(self):
        pass
    
    def render(self):
        return 0