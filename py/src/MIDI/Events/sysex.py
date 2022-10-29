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

        self.deviceID = self.data[1]
        self.isGlobal = self.deviceID == 0x7f

        id1 = None
        if len(self.data) > 2:
            id1 = self.data[2]
        id2 = None
        if len(self.data) > 3:
            id2 = self.data[3]
        self.subID1 = id1
        self.subID2 = id2

    def __str__(self):
        return f'SYSEX@{self.time} {self.type} {self.data} length = {self.length} [{self.deviceID}:{self.subID1}:{self.subID2}]'




