'''
Created on 15 Sep 2019

@author: julianporter
'''

from .chunk import Chunk
from .event import Event
import traceback
           

class FLPTrack(Chunk):
    
    def __init__(self,data):
        super().__init__(data)
        self.events=[]
           
    def parse(self):
        self.buffer=self.data
        try:
            while len(self.buffer)>0 :
                event=Event(self.buffer)
                length = len(event)
                self.events.append(event)
                self.buffer=self.buffer[length:]
        except Exception as e:
            print(f'Error : {e}')
            traceback.print_exc()
            pass
    
    def __iter__(self):
        return iter(self.events)
        
    def __len__(self):
        return len(self.events)
        
    def __getitem__(self,index):
        return self.events[index]
    
    def __str__(self):
        return self.stringify(self.events, '\n')
        
