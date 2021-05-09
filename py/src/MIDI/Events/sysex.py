'''
Created on 15 Sep 2019

@author: julianporter
'''
from .event import Event

class SysExEvent(Event):
    
    def __init__(self,time,buffer):
        super().__init__(time, buffer)
        self.type=self.header & 0x0f
        
        length, n=self.getVarLengthInt()
        self.data=self.buffer[:length]
        self.length=length+n+1
        
    def __str__(self):
        return f'SYSEX@{self.time} {self.type} {self.data} length = {self.length}'
        
    