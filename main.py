# -*- coding: utf-8 -*-

from RL.DQN import DeepQNetwork
from RL.environment.environment import MarketMaking
from RL.environment.config import config
import matplotlib.pyplot as plt
import numpy as np


T = 1000
account_list = list()
position_list =list()
 
def run(env,RL):
    step = 0
    for episode in range(1):
        # initial observation
        observation = env.reset()
        time = 0
        while True:
            time += 1
            # fresh env
            env.render()
            # RL choose action based on observation
            action = RL.choose_action(observation)
            #print("action",action)
            # RL take action and get next observation and reward
            observation_, reward, done = env.step(observation,action)
            account_list.append(env.Ag_exchange.account)
            position_list.append(env.Ag_exchange.position)
            #print(observation)
            print(reward)
            RL.store_transition(observation, action, reward, observation_)
 
            if (step > 200) and (step % 5 == 0):
                RL.learn()
            # swap observation
            observation = observation_
            # break while loop when end of this episode
            if time == T:
                break
            step += 1
    # end of game
    print('game over')
    return account_list,position_list

 
 
if __name__ == "__main__":
    
    config_file = "config.ini"
    cf = config().getconf(config_file)
    n_features = int(cf['state']['state_size'])
    n_actions = int(cf['learning']['action_size'])
    env =  MarketMaking(cf)
    RL = DeepQNetwork(n_actions, n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    init_price = 4043
    account_list,position_list = run(env,RL)
    accounts = np.array(account_list)
    positions = np.array(position_list)*4043 #4043是最开始的单价
    total = np.sum([accounts,positions],axis=0)
    RL.plot_cost()
    plt.plot(np.arange(T),total)
    plt.ylabel('Account')
    plt.xlabel('time')
    plt.show()