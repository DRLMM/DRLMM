# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 17:32:23 2020

@author: huyue
"""
import configparser

class config():
        
    def getconf(self,file_path):
        
        config = configparser.ConfigParser()
        config.read(file_path)
        
        return config
    
    