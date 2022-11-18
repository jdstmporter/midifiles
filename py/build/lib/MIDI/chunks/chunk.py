'''
Created on 15 Sep 2019

@author: julianporter
'''
from MIDI.base import Base

class Chunk(Base):
    
    def __init__(self,data=b''):
        super().__init__()
        self.data=data
        
    def __len__(self):
        return len(self.data)
    
    def __str__(self):
        return self.stringify(self.data)
