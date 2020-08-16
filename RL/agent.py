# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 10:57:54 2020

@author: huyue
"""


# 强化学习 加油！！！ 我可以的！
from policy import greedy_policy
import numpy as np
from traces import traces

class agent():
    
    def __init__(self,policy,config):
        
        self.N_ACTIONS = config['learning']['n_actions']
        self.theta
        self.alpha
        self.omega
        self.gamma
        self.lambda_
        self.alpha_floor
        self.alpha_start
        self.policy = policy
        self._agg_delta = 0
        self._update_counter = 0
        
        self.traces = traces()
        
    def action(self,s):
        qs = []
        for a in range(0,self.N_ACTIONS):
            qs[a] = self.getQ(s,a)
        
        return self.policy.sample(qs)
            
    def go_greedy(self):
        
        self.policy = greedy_policy(self.N_ACTIONS, seed = 0)
            
    def handle_transition(self,from_state,action,reward,to_state):
        
        self.update_traces(from_state,action)  
        
        delta  = self.update_weights(from_state,action,reward,to_state)
        
        self._agg_delta += np.abs(delta)
        
        
    def handle_terminal(self,episode):
        
        self.traces.decay(0,0)
        self.alpha = np.max([self.alpha_floor,self.alpha_start * np.power(self.omega,episode)])
        
        self.policy.handle_terminal(episode)
        
    def update_traces(self,from_state,action):
         
        self.traces.decay(self.gamma * self.lambda_)
        self.traces.update(from_state,action)
     
    def epsilon_greedy(self,state):
        pass
     
    def updateQ(self,update):
        pass
    
    def getQ(self,state,action):
        
        pass
        
        
        
    def argmaxQ(self,state):
        
        index = 0
        n_ties = 1
        
        currMaxQ = self.getQ(state,index)
        
        for a in range(1,self.N_ACTIONS):
            
            val = self.getQ(state,a)
            
            if (val >= currMaxQ):
                if(val > currMaxQ):
                    currMaxQ = val
                    index = a
                else:
                    n_ties += 1
                    
                    if ((np.random.randint(5 * n_ties) % n_ties) == 0):
                        currMaxQ = val
                        index = a
        return index
    
    def maxQ(self,state):
        
        return self.getQ(state,self.argmaxQ(state))
    
    def write_theta(self,filename):
        pass
    
class QLearn(agent):
    
    def __init__(self,policy,config):
        agent. __init__(self,policy,config)
    
    def update_traces(self,from_state,action):
        amax = self.argmaxQ(from_state)
        
        if(action != amax):
            self.traces.decay(0)
        else:
            self.traces.decay(self.gamma * self.lambda_)
        
        self.traces.update(from_state,action)
    
    def update_weights(self,from_state,action,reward,to_state):
        pass
# =============================================================================
#         Q = self.getQ(from_state,action)
#         F_term = self.gamma * self.to_state.getPotential()
# =============================================================================
        
        
    
class SARSA(agent):
    
    def __init__(self,policy,config):
        agent. __init__(self,policy,config)
    
    
    def updateWeights(self,from_state,action,reward,to_state):
        pass 