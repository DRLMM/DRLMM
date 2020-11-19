# -*- coding: utf-8 -*-

from RL.DQN import DeepQNetwork
from RL.environment.environment import MarketMaking
from RL.environment.config import config
import numpy as np
import matplotlib.pyplot as plt


T = 200 #步数
episode_set = 1
 
def run(env,RL):
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
            # action = RL.choose_action_random()
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

    acc_list = []
    pos_list = []
    total_list = []

    config_file = "config.ini"
    cf = config().getconf(config_file)
    n_features = int(cf['state']['state_size'])
    n_actions = int(cf['learning']['action_size'])
    
    for i in [0.5]:
        account_list = list()
        position_list =list()  
        ticker_list = list()
        env =  MarketMaking(cf,'data/Ag(T+D)_SGE_TickData_202003/',{'account':1000000,'position':50},damping_factor=i)
        
        RL = DeepQNetwork(n_actions, n_features,
                        learning_rate=0.01,
                        reward_decay=0.9,
                        e_greedy=0.9,
                        replace_target_iter=200,
                        memory_size=2000,
                        # output_graph=True
                        )
        run(env,RL)
        RL.plot_cost()

        bid_count = env.Ag_exchange.bid_count
        ask_count = env.Ag_exchange.ask_count
        clear_count = env.Ag_exchange.clear_count

        # 画图
        accounts = np.array(account_list)
        positions = np.array(position_list)*np.array(ticker_list)
        total = np.sum([accounts,positions],axis=0)
        p = np.array(position_list)

        # # 总资产
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

        # print(p.min())
        # print(p.max())
        # print(p.std())
        # print(p.sum()/len(p))
        # print(p[-1])
        
        # print(accounts.min())
        # print(accounts.max())
        # print(accounts.std())
        # print(accounts.sum()/len(accounts))
        # print(accounts[-1])

        # print(total.min())
        # print(total.max())
        # print(total.std())
        # print(total.sum()/len(total))
        # print(total[-1])

        acc_list.append(accounts)
        pos_list.append(p)
        total_list.append(total)

    acc_std_list = [x.std() for x in acc_list]
    print('acc_std_list=',acc_std_list)
    acc_ave_list = [x.sum()/len(x) for x in acc_list]
    print('acc_ave_list=',acc_ave_list)

    pos_std_list = [x.std() for x in pos_list]
    print('pos_std_list=',pos_std_list)
    pos_ave_list = [x.sum()/len(x) for x in pos_list]
    print('pos_ave_list=',pos_ave_list)
    total_max_list = [x.max() for x in total_list]
    print('total_max_list=',total_max_list)
    total_min_list = [x.min() for x in total_list]
    print('total_min_list=',total_min_list)
    pos_max_list = [x.max() for x in pos_list]
    pos_min_list = [x.min() for x in pos_list]
    print('pos_max_list=',pos_max_list)
    print('pos_min_list=',pos_min_list)
    acc_max_list = [x.max() for x in acc_list]
    print('acc_max_list=',acc_max_list)
    acc_min_list = [x.min() for x in acc_list]
    print('acc_min_list=',acc_max_list)
    total_end_list = [x[-1] for x in total_list]
    print('total_end_list=',total_end_list)