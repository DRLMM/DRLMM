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
from RL.policy import epsilon_greedy

class DQNAgent:
    
    def __init__(self,config):
        
        self.state_size = config['state_size']
        self.action_size = config['action_size']
        self.memory_size = config['memory_size']
        
        self.memory = [None] * self.memory_size
        self.gamma = config['gamma']
        self.epsilon = config['epsilon']
        self.epsilon_min = config['epsilon_min']
        self.train_interval = config['train_interval']
        self.episode_length = config['episode_length']
        self.epsilon_decrement = (self.epsilon - self.epsilon_min) \
            * self.train_interval / (self.episodes * self.episode_length)
            
        self.learning_rate = config['learning_rate']
        self.batch_size = config['batch_size']
        self.brain = self._build_model()
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
        brain.add(Dense(self.action_size, activation='linear'))
        brain.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return brain


    def act(self,state):

        state = state.reshape(1,self.state_size)
        qs = self.brain.predict(state)
        n_actions = self.action_size
        eps = self.epsilon
        floor = self.epsilon_min
        T = self.train_interval
        seed = 45
        
        epsilon_greedy_action = epsilon_greedy(n_actions,eps,floor,T,seed).sample(qs)
        
        return epsilon_greedy_action
    
    
    def observe(self,state,action,reward,next_state,done):
        """Memory Management and training of the agent
        """  
        self.i = (self.i + 1) % self.memory_size
        self.memory[self.i] = (state,action,reward,next_state,done)
        
    
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
from RL.MarketMaking import environment
from config import config


config_file = "./config.ini"
cf = config().getconf(config_file)
memory_size = cf['memory_size']
env =  environment(cf)
state, _ = env.initialise()

agent = DQNAgent(cf)

# Warming up the agent
#%%
for _ in range(memory_size):
    action = agent.act(state)
    
    next_state,reward,done, _ = env.step(state,action)
    agent.observe(state,action,reward,next_state,done)
  
#Training the agent
#%%
episodes = 100
episode_length = 400

rews = []
losses =[]
epsilons =[]

for ep in range(episodes):
    
    state = env.initialise()
    rew = 0
    for _ in range(episode_length):
        action = agent.act(state)
        
        next_state, reward,done, _ = env.step(state,action)
        
        loss = agent.observe(state,action,reward,next_state,done)
        state = next_state
        rew += reward
        
    print("Ep:" + str(ep)
           + "| rew:" + str(round(rew, 2))
           + "| eps:" + str(round(agent.epsilon, 2))
           + "| loss:" + str(round(loss.history["loss"][0], 4)))
    
    rews.append(rew)
    epsilons.append(agent.epsilon)
    losses.append(loss.history['loss'][0])