# -*- coding: utf-8 -*-

from RL.DQN import DeepQNetwork
from RL.environment.environment import MarketMaking
from RL.environment.config import config
import numpy as np
import matplotlib.pyplot as plt


T = 2000 #步数
episode_set = 20
 
def run():
    step = 0
    for episode in range(episode_set):
        print(episode)
        # initial observation
        if step == 0:
            observation = env.reset()
        time = 0
        init_price = env.Ag_exchange.ticker #初始单价
        print(init_price)
 
        while True:
            time += 1
            # fresh env
            env.render()
            # RL choose action based on observation
            action = RL.choose_action(observation)
            #print("action",action)
            # RL take action and get next observation and reward
            observation_, reward, done = env.step(observation,action)

            if done:
                print("No more data")
                return None
            #print(observation)
            # print(reward)
            RL.store_transition(observation, action, reward, observation_)
            account_list.append(env.Ag_exchange.account)
            position_list.append(env.Ag_exchange.position)
            ticker_list.append(env.Ag_exchange.ticker)
 
            if (step > 200) and (step % 5 == 0):
                RL.learn()
                # print(env.Ag_exchange.account,env.Ag_exchange.position,env.Ag_exchange.account+env.Ag_exchange.position*4043)
            # swap observation
            observation = observation_
            # break while loop when end of this episode
            if time == T:
                break
            step += 1

    # end of game
    print('game over')

 
if __name__ == "__main__":
    account_list = list()
    position_list =list()  
    ticker_list = list()
    
    config_file = "config.ini"
    cf = config().getconf(config_file)
    n_features = int(cf['state']['state_size'])
    n_actions = int(cf['learning']['action_size'])
    env =  MarketMaking(cf,'data/Ag(T+D)_SGE_TickData_202003/',{'account':1000000,'position':50})
    
    RL = DeepQNetwork(n_actions, n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    run()
    RL.plot_cost()

    bid_count = env.Ag_exchange.bid_count
    ask_count = env.Ag_exchange.ask_count
    clear_count = env.Ag_exchange.clear_count
    # 画图
    accounts = np.array(account_list)
    positions = np.array(position_list)*np.array(ticker_list) #4043是最开始的单价
    total = np.sum([accounts,positions],axis=0)

    # 总资产
    plt.plot(np.arange(len(total)),total)
    plt.ylabel('total')
    plt.xlabel('step')
    plt.show()

    # 余额
    plt.plot(np.arange(len(account_list)),account_list)
    plt.ylabel('account')
    plt.xlabel('step')
    plt.show()

    # 库存
    plt.plot(np.arange(len(position_list)),position_list)
    plt.ylabel('position')
    plt.xlabel('step')
    plt.show()

    p = np.array(position_list)
    print(p.min())
    print(p.max())
    print(p.std())
    print(p.sum()/len(p))
    
    print(accounts.min())
    print(accounts.max())
    print(accounts[-1])

