# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 20:36:11 2020

@author: huyue
"""
import random
import numpy as np
import keras
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from RL.environment.policy import epsilon_greedy

class DQNAgent:
    
    def __init__(self,config):
        
        self.state_size = int(config['state']['state_size'])
        self.n_actions = int(config['learning']['action_size'])
        self.memory_size = int(config['learning']['memory_size'])
        self.episodes = int(config['learning']['episodes'])
        self.memory = [None] * self.memory_size
        self.gamma = float(config['learning']['gamma'])
        self.epsilon = float(config['learning']['epsilon'])
        self.epsilon_min = float(config['learning']['epsilon_min'])
        self.train_interval = int(config['learning']['train_interval'])
        self.episode_length = int(config['learning']['episode_length'])
        self.epsilon_decrement = (self.epsilon - self.epsilon_min) \
            * self.train_interval / (self.episodes * self.episode_length)
            
        self.learning_rate = float(config['learning']['learning_rate'])
        self.batch_size = int(config['learning']['batch_size'])
        self.model = self._build_model()
        self.i = 0
        
        
    def _build_model(self):
        
        """Build the agent's brain
        """
        brain = Sequential()
        neurons_per_layer = 24
        activation = "relu"
        brain.add(Dense(neurons_per_layer,
                        input_dim=self.state_size,
                        activation=activation))
        brain.add(Dense(neurons_per_layer, activation=activation))
        brain.add(Dense(self.n_actions, activation='linear'))
        brain.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return brain


    def act(self,state):
        print("act state",state)
        
        state = state.reshape(1,self.state_size)
        qs = self.model.predict(state)
        n_actions = self.n_actions
        eps = self.epsilon
        floor = self.epsilon_min
        T = self.train_interval
        seed = 45
        
        epsilon_greedy_action = epsilon_greedy(n_actions,eps,floor,T,seed).sample(qs)
        
        return epsilon_greedy_action
    
    
    def observe(self,state,action,reward,next_state,done,warming_up = False):
        """Memory Management and training of the agent
        """  
        self.i = (self.i + 1) % self.memory_size
        self.memory[self.i] = (state,action,reward,next_state,done)
        
        if (not warming_up):
            
            if self.epsilon > self.epsilon_min:
                
                self.epsilon -= self.epsilon_decrement
            state, action, reward, next_state, done = self._get_batches()
            
            reward += (self.gamma
                       * np.logical_not(done)
                       * np.amax(self.brain.predict(next_state),
                                 axis = 1))
            q_target = self.brain.predict(state)
            
            q_target[action] = reward
                
            return self.brain.fit(state,q_target,batch_size = self.batch_size,epochs=1,verbose = False)
            
         
    def _get_batches(self):
        
        """Selecting a batch of memory
           Split it into categorical subbatches
           Process action_batch into a position vector
        """
        
        batch = np.array(random.sample(self.memory, self.batch_size))
        state_batch = np.concatenate(batch[:, 0])\
            .reshape(self.batch_size, self.state_size)
        action_batch = np.concatenate(batch[:, 1])\
            .reshape(self.batch_size, self.action_size)
        reward_batch = batch[:, 2]
        next_state_batch = np.concatenate(batch[:, 3])\
            .reshape(self.batch_size, self.state_size)
        done_batch = batch[:, 4]
  
        return state_batch, action_batch, reward_batch, next_state_batch, done_batch
        
        

#%%
from RL.environment.environment import MarketMaking
from RL.environment.config import config


config_file = "../config.ini"
cf = config().getconf(config_file)
memory_size = int(cf['learning']['memory_size'])
env =  MarketMaking(cf)
state, _ = env.initialise()

agent = DQNAgent(cf)

# Warming up the agent
#%%
next_state = state
for _ in range(5):
    action = agent.act(next_state)
    print("action",action)
    
    next_state,reward,done= env.step(state,action)
    print("reward",reward)
    agent.observe(state,action,reward,next_state,done,warming_up = True)
  
#Training the agent
#%%
# =============================================================================
# episodes = 10
# episode_length = 40
# 
# rews = []
# losses =[]
# epsilons =[]
# 
# for ep in range(episodes):
#     
#     state,_ = env.initialise()
#     rew = 0
#     for _ in range(episode_length):
#         action = agent.act(state)
#         
#         next_state, reward,done= env.step(state,action)
#         print(next_state, reward,done)
#         loss = agent.observe(state,action,reward,next_state,done)
#         state = next_state
#         rew += reward
#         
#     print("Ep:" + str(ep)
#            + "| rew:" + str(round(rew, 2))
#            + "| eps:" + str(round(agent.epsilon, 2))
#            + "| loss:" + str(round(loss.history["loss"][0], 4)))
#     
#     rews.append(rew)
#     epsilons.append(agent.epsilon)
#     losses.append(loss.history['loss'][0])
# =============================================================================
