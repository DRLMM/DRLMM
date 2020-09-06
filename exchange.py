from MM.data import DataHandler
import datetime

PRICE = 0
VOLUME = 1
HEAD = 2


# 用于模拟交易所
class Exchange(object):

    def __init__(self, folder_path: str, update_function=None):
        self.dataHandler = DataHandler(folder_path)
        self.timestamp: datetime.datetime = None  # 时间戳
        self.count = -1
        self.update_function = update_function

        # 交易所数据
        self.ticker: float = 0  # 成交价
        self.bids: list = list()  # 买单列表 [(price1,volume1),(price2,volume2),...]
        self.asks: list = list()  # 卖单列表 [(price1,volume1),(price2,volume2),...]
        self.open: float = 0  # 开盘价
        self.high: float = 0  # 最高价
        self.low: float = 0  # 最低价
        self.close: float = 0  # 收盘价
        self.spread: float = 0  # 价差
        self.volume: int = 0 # 累计成交量
        self.last_volume: int = 0
        self.volume_diff: int = 0 #成交量

        # agent数据
        self.account: float = 0  # 账户余额
        self.position: float = 0  # 仓位
        self.bid_orders: list = list()  # 买单列表 [(price1,volume1,q_ahead1),(price2,volume2,q_ahead2),...]
        self.ask_orders: list = list()  # 卖单列表 [(price1,volume1,q_ahead1),(price2,volume2,q_ahead2),...]
        self.cancel_num: int = 0

    def init_exchange(self):
        """
        初始化交易所状态
        """
        self.update_market()

    def init_agent(self, account: float, position: float):
        self.account = account
        self.position = position

    def update_market(self):
        """
        更新交易所状态
        """
        self.count += 1
        curr_bar = self.dataHandler.update_bar()  # 更新bar
        self.ticker = float(curr_bar['LastPrice'])
        self.open = float(curr_bar['open'])
        self.high = float(curr_bar['high'])
        self.low = float(curr_bar['low'])
        self.close = float(curr_bar['close'])
        self.last_volume = self.volume
        self.volume = int(curr_bar['vlume'])
        self.volume_diff = self.volume - self.last_volume

        # 买单
        self.bids = []
        for i in range(1, 6):
            price = float(curr_bar[f'BidPrice{i}'])
            volume = float(curr_bar[f'BidVolume{i}'])
            self.bids.append(tuple([price, volume]))
        # 卖单
        self.asks = []
        for i in range(1, 6):
            price = float(curr_bar[f'AskPrice{i}'])
            volume = float(curr_bar[f'AskVolume{i}'])
            self.asks.append(tuple([price, volume]))
        self.spread = self.asks[0][PRICE] - self.bids[0][PRICE]
        # print(curr_bar)
        return curr_bar

    def update_agent_state(self, update_function, clear=True):
        """
        更新agent状态,默认撤掉没成交的单
        """
        self.account, self.position, self.bid_orders, self.ask_orders = update_function()
        if clear:
            self.cancel_num += (len(self.bid_orders) + len(self.ask_orders))
            self.bid_orders, self.ask_orders = [], []

    def breakdown(self):
        """
        击穿逻辑
        """
        account = self.account
        position = self.position
        bid_orders = self.bid_orders
        ask_orders = self.ask_orders
        for bid_order in bid_orders:
            if bid_order[PRICE] >= self.ticker:  # 现价击穿买单价
                account -= bid_order[PRICE] * bid_order[VOLUME]
                position += bid_order[VOLUME]

        for ask_order in ask_orders:
            if ask_order[PRICE] <= self.ticker:  # 现价击穿卖单价
                account += ask_order[PRICE] * ask_order[VOLUME]
                position -= ask_order[VOLUME]
        # 将已成交的单移除
        bid_orders = [x for x in bid_orders if x[PRICE] < self.ticker]
        ask_orders = [x for x in ask_orders if x[PRICE] > self.ticker]
        return account, position, bid_orders, ask_orders

    def update_state(self):
        """
        更新状态
        """
        self.update_market()
        self.update_agent_state(self.breakdown)

    def send_action(self, action: str, level: int = 0, volume: float = 0):
        """
        发起动作
        """
        # 挂买单
        if action == "BID":
            price = self.bids[level][PRICE]
            if self.account >= price * volume:
                self.bid_orders.append(tuple([price, volume,self.bids[level][VOLUME],0]))
            else:
                print('you need more monny')
        # 挂卖单
        elif action == "ASK":
            price = self.asks[level][PRICE]
            if self.position >= volume:
                self.ask_orders.append(tuple([price, volume,self.asks[level][VOLUME],0]))
            else:
                print('you need more position')
        # 清库存
        elif action == "CLEAR" and volume and volume <= self.position:
            self.account += volume * self.ticker
            self.position -= volume
        # 平仓
        elif action == "SELLALL":
            self.account += self.position * self.ticker
            self.position = 0

    def update_function(self):
        account = self.account
        position = self.position
        bid_orders = self.bid_orders
        ask_orders = self.ask_orders
        bids = self.bids
        asks = self.asks
        volume_diff = self.volume_diff
        remaining_volume = volume_diff #成交量剩余量
        for i in range(len(bids)):#从买一开始
            if remaining_volume <= 0: break
            if bids[i][PRICE] >= self.ticker: #买单价格高于成交价
                if remaining_volume > bids[i][VOLUME]:#击穿
                    remaining_volume -= bids[i][VOLUME]
                    account -= bid_orders[i][PRICE] * bid_orders[i][VOLUME]
                    position += bid_orders[i][VOLUME]
                else:
                    diff = remaining_volume - bid_orders[i][HEAD]
                    if diff > 0:
                        if bid_orders[i][VOLUME] <= diff:#totally executed
                            account -= bid_orders[i][PRICE] * bid_orders[i][VOLUME]
                            position += bid_orders[i][VOLUME]
                        else:#patially
                            account -= bid_orders[i][PRICE] * diff
                            position += diff
                    else: #如果没成交就撤单，这步可去掉
                        self.bid_orders[i][HEAD] -= remaining_volume
        for i in range(len(asks)):
            if remaining_volume <= 0: break
            if asks[i][PRICE] <= self.ticker:
                if remaining_volume > asks[i][VOLUME]:
                    remaining_volume -= asks[i][VOLUME]
                    account += ask_orders[i][PRICE] * ask_orders[i][VOLUME]
                    position -= ask_orders[i][VOLUME]
                else:
                    diff = remaining_volume - ask_orders[i][HEAD]
                    if diff > 0:
                        if ask_orders[i][VOLUME] <= diff:#totally executed
                            account -= ask_orders[i][PRICE] * ask_orders[i][VOLUME]
                            position += ask_orders[i][VOLUME]
                        else:#patially
                            account -= ask_orders[i][PRICE] * diff
                            position += diff
                    else: #如果没成交就撤单，这步可去掉
                        self.ask_orders[i][HEAD] -= remaining_volume
        # 将已成交的单移除
        bid_orders = [x for x in bid_orders if x[PRICE] < self.ticker]
        ask_orders = [x for x in ask_orders if x[PRICE] > self.ticker]
        return account, position, bid_orders, ask_orders







Ag_exchange = Exchange('data/Ag(T+D)_SGE_TickData_202003/')