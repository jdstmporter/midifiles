'''
Created on 9 May 2021

@author: julianporter
'''

from enum import Enum


    


class BaseMessage(Enum):
    
    @classmethod
    def all(cls):
        return list(cls.__members__.values())
    
    @classmethod
    def names(cls):
        return list(cls.__members__.keys())
    
    @classmethod
    def byName(cls,name):
        return cls.__members__[name]
    
    @classmethod
    def payloadLength(cls):
        return None
    
    
 
    
class BadMessage(BaseMessage):
    
    BadMessage = 0
    



    

