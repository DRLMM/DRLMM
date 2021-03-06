# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 09:37:34 2020

@author: huyue
"""
import numpy as np

class policy(object):
    
    def __init__(self,n_actions,seed):
        self.N_ACTIONS = n_actions
        self.seed = seed
        #np.random.seed(self.seed)
    
    def handle_terminal(self,episode):
        pass
    
    
class random_policy(policy):
    
    def __init__(self,n_actions,seed):
       policy.__init__(self,n_actions,seed)
    
    def sample(self,qs):
        return np.random.randint(0,self.N_ACTIONS-1)
    
class greedy_policy(policy):
    """
    选择价值函数最大的动作，如果出现一样大的，就ramdom
    """
    def __init__(self,n_actions,seed):
        policy.__init__(self,n_actions,seed)
    
    def sample(self,qs):
        
        
        argmax = 0
        n_ties = 1
        
        for a in range(1,self.N_ACTIONS):
           # np.random.seed(self.seed)
            if(qs[a]> qs[argmax]):
                argmax = a
                
            elif(qs[a]>= qs[argmax]):
                n_ties += 1
                
                if ((np.random.randint(1,n_ties * 5) % n_ties) == 0):
                    argmax = a
                    
        return argmax
    
class epsilon_greedy(greedy_policy):
    """
    epsilon greedy算法
    """
    
    def __init__(self,n_actions,eps,floor,T,seed):
        self.eps = eps
        self.eps_T = T
        self.eps_init = eps
        self.eps_floor = floor
        
        greedy_policy.__init__(self,n_actions,seed)
        
    
    def sample(self,qs):
        print("qs",qs)
        #np.random.seed(self.seed)
        random_number = np.random.rand()
        if( random_number < self.eps):
            #np.random.seed(self.seed)
            return np.random.randint(0,self.N_ACTIONS-1)
        else:
            return greedy_policy.sample(self,qs)
    
    def descr(self):
        return self.eps
    
    def handle_terminal(self,episode):
        self.eps = self.eps_init * np.power(self.eps_floor/ self.eps_init, episode / self.eps_T)
        
        
# =============================================================================
# # 测试
# if __name__ == '__main__':
#     
#     qs = [13.684795,26.555346,-8.383726,-29.709715,30.46716,22.772629,-38.131424,9.355559,40.934956,31.808802]
#     n_actions = 10
#     eps = 0.1
#     seed = 1056
#     T = 2
#     floor = 0.05
#     
#     greedy_action = greedy_policy(n_actions,seed).sample(qs)
#     print(greedy_action)
#     
#     epsilon_greedy_action = epsilon_greedy(n_actions,eps,floor,T,seed).sample(qs)
#     print(epsilon_greedy_action)
#     
# =============================================================================
