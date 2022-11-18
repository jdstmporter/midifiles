'''
Created on 15 Sep 2019

@author: julianporter
'''

from .chunk import Chunk
from MIDI.Events import MetaEvent, MIDIEvent
import traceback


class Track(Chunk):

    def __init__(self,data,containsTiming = True):
        super().__init__(data)
        self.events=[]
        self.containsTiming = containsTiming

    def parse(self):
        self.buffer=self.data
        time=0 if self.containsTiming else None
        self.buffer=self.buffer[8:]
        try:
            while len(self.buffer)>0 :
                #print(f'Parsing {len(self.buffer)} bytes')
                if self.containsTiming:
                    delta, _=self.getVarLengthInt()
                    time+=delta
                #print(f'Time is {time} length {n}')
                eventType=self.buffer[0]
                #print(f'Event type is {eventType}')
                if eventType == 0xff:     # Meta event
                    event = MetaEvent(time,self.buffer)
                else:
                    event = MIDIEvent(time,self.buffer)
                length = len(event)
                self.events.append(event)
                self.buffer=self.buffer[length:]
        except Exception:
            #print(f'Error : {e}')
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

