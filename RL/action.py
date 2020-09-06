# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:16:09 2020

@author: huyue
"""
import numpy as np


# 对action进行设置
class action(object):
    
    def __init__(self,act_id):
        
        self.act_id = act_id
        self.ORDER_SIZE = 1 # 默认为1

        """
        下单数量
        ask_level,bid_level 报价与当前订单簿的最优报价的距离
        """
        
        if (self.act_id == 0):
            self.ask_level = 1
            self.bid_level = 1
        
        elif(self.act_id == 1):    
            self.ask_level = 2
            self.bid_level = 2
            
        elif(self.act_id == 2):
            self.ask_level = 3
            self.bid_level = 3
        
        elif(self.act_id == 3):
            self.ask_level = 4
            self.bid_level = 4
            
        elif(self.act_id == 4):
            self.ask_level = 5
            self.bid_level = 5
            
        elif(self.act_id == 5):
            self.ask_level = 1
            self.bid_level = 3
            
        elif(self.act_id == 6):
            self.ask_level = 3
            self.bid_level = 1
        
        elif(self.act_id == 7):
            self.ask_level = 2
            self.bid_level = 5
            
        elif(self.act_id == 8):
            self.ask_level = 5
            self.bid_level = 2
            
         # 市价单清空所有的库存
        elif(self.act_id == 9):
            self.ask_level = 0
            self.bid_level = 0
                
            
    def get_order_quote(self,ask_price,bid_price):
        """
        报价
        """
        al = self.ask_level
        bl = self.bid_level
        ask_quote = 0.0
        bid_quote = 0.0
        
        if (self.act_id < 9): 
            spread = ask_price - bid_price
            half_spread = max(0,spread / 2.0)
            midprice = (ask_price + bid_price) / 2
            
            ask_quote = midprice + al * half_spread
            bid_quote = midprice - bl * half_spread
            
        
        elif (self.act_id == 9): #市价单清空库存
            a1 = 0 # 买1
            b1 = 0 # 卖1
            ask_quote = a1 + al
            bid_quote = b1 - bl
            
        return ask_quote,bid_quote  


# =============================================================================
# # 测试
# if __name__ == '__main__':
#     
#     act_id = 2
#     ask_quote,bid_qutote = action(act_id).get_order_quote()
#     print(ask_quote,bid_qutote)
#     
#     print(action(act_id).ORDER_SIZE)
# =============================================================================
    
 