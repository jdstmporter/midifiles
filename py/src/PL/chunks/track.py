'''
Created on 15 Sep 2019

@author: julianporter
'''

from .chunk import Chunk
from .event import Event
import traceback
           

class Track(Chunk):
    
    def __init__(self,data):
        super().__init__(data)
        self.events=[]
           
    def parse(self):
        self.buffer=self.data
        #self.buffer=self.buffer[8:]
        try:
            while len(self.buffer)>0 :
                #print(f'Parsing {len(self.buffer)} bytes')
                #print(f'Time is {time} length {n}')
                #eventType=self.buffer[0]
                #print(f'Next event type {eventType}')
                event=Event(self.buffer)
                #if eventType <192 :     
                #    event = NumericEvent(self.buffer)
                #else: # 
                #    event = TextEvent(self.buffer)
                length = len(event)
                #print(f"Event type {hex(eventType)} is of kind {event.code}")
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
        
