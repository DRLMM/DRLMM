import os
import pandas as pd

# 用于从csv文件中读取信息
class DataHandler(object):

    def __init__(self,folder_path:str):
        self.folder_path:str = folder_path  #文件夹地址
        self.day = -1   #记录当前读到第几天
        self.day_data = None  #当日数据
        self.curr_bar_index:int = -1  #当日最后一条bar的下标
        self.curr_bar = None  #最后一条bar的数据
        self.history_bar:list = list()
        # 初始化数据
        self.read_next_day()

    def read_data(self,folder_path,day)->pd.DataFrame: 
        """
        用于读取数据的工具函数
        """
        dir_list = os.listdir(folder_path) #读取文件夹里的文件名
        dir_list.sort()
        return pd.read_csv(folder_path+dir_list[day])
        # dir_list = os.listdir('data/Ag(T+D)_SGE_TickData_202003/').sort()  #读取文件夹里的文件名
    
    def read_next_day(self):
        """
        读取下一天的数据
        """
        self.day += 1
        self.day_data = self.read_data(self.folder_path,self.day).sort_values(by='volume')

    def update_bar(self):
        """
        更新bar数据
        """
        self.curr_bar_index += 1  #bar下标加一
        if self.curr_bar_index >= len(self.day_data):  #如果当天的数据已读完则进入下一天
            self.read_next_day()  #读取下一天的内容
            self.curr_bar_index = 0  #将bar的下标归零
        self.curr_bar = self.day_data[self.curr_bar_index:self.curr_bar_index+1]  #将bar数据更新
        self.history_bar.append(self.curr_bar)
        return self.curr_bar
        
        