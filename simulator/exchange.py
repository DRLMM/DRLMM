from data import DataHandler
import datetime

# 用于模拟交易所
class Exchange(object):

    def __init__(self,folder_path:str):
        self.dataHandler = DataHandler(folder_path)
        self.timestamp:datetime.datetime = None     #时间戳

        # 交易所数据
        self.ticker:float = 0       #成交价
        self.bids:list = list()     #买单列表
        self.asks:list = list()     #卖单列表
        self.open:float = 0     #开盘价
        self.high:float = 0     #最高价
        self.low:float = 0      #最低价
        self.close:float = 0    #收盘价
        self.spread:float = 0   #价差

        # agent数据
        self.account:float = 0        #账户余额
        self.position:float = 0       #仓位
        self.bid_orders:list = list()   #买单列表 [(price1,volume1),(price2,volume2),...]
        self.ask_orders:list = list()   #卖单列表 [(price1,volume1),(price2,volume2),...]

    def init_agent(self,account:float,position:float)
        self.account = account
        self.position = position

    def update_market(self):
        """
        更新交易所状态
        """
        last_bar = dataHandler.update_bar()
        print(last_bar)
        pass

    def update_agent_state(self,update_function):
        """
        更新agent状态
        """
        pass

    def next_state(self):
        self.update_market()
        self.update_agent_state()

    def send_action(self):
        """
        发起动作
        """
        pass



