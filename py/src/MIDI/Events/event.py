'''
Created on 15 Sep 2019

@author: julianporter
'''
from collections import OrderedDict
from MIDI.base import Base

class Event(Base):
    
    def __init__(self,time,buffer):
        super().__init__(buffer[1:])
        self.time=time
        self.header=buffer[0]
        self.length=0
        self.data=b''
        self.parameters=OrderedDict()
        
    def __len__(self):
        return self.length
    
    def __str__(self):
        return self.data
        
    def __getattr__(self,key):
        return self.parameters[key]
        
        
    
