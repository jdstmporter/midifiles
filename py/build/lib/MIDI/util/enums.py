'''
Created on 16 Sep 2019

@author: julianporter
'''
import enum

class SafeEnum(enum.Enum):
    
    def __str__(self):
        return self.name.replace('_',' ')
    
    @classmethod
    def make(cls,n):
        try:
            return cls(n)
        except:
            return None