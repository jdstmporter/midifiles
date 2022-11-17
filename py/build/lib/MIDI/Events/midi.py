'''
Created on 15 Sep 2019

@author: julianporter
'''

from .event import Event
from .messages import NoteMessage, PressureMessage, ControlMessage, ProgramMessage, ChannelPressureMessage, PitchBendMessage, SystemMessage

class MIDIEvent(Event):
    
    commands = {
        0x80: 'NOTE_OFF',
        0x90: 'NOTE_ON',
        0xa0: 'PRESSURE',
        0xb0: 'CONTROL_CHANGE',
        0xc0: 'PROGRAM_CHANGE',
        0xd0: 'CHANNEL_PRESSURE',
        0xe0: 'PITCH_BEND'
    }
  
    def __init__(self,time,buffer):
        super().__init__(time, buffer)
        self.channel=self.header & 0x0f
        self.command=self.header & 0xf0
        
        if self.command in [0x80,0x90]:
            self.message=NoteMessage(self.command==0x90,self.buffer)
        elif self.command==0xa0:
            self.message=PressureMessage(self.buffer)
        elif self.command==0xb0:
            self.message=ControlMessage(self.buffer)
        elif self.command==0xc0:
            self.message=ProgramMessage(self.buffer)
        elif self.command==0xd0:
            self.message=ChannelPressureMessage(self.buffer)
        elif self.command==0xe0:
            self.message=PitchBendMessage(self.buffer)
        elif self.command==0xf0:
            self.message=SystemMessage(self.buffer)
        else:
            self.message=''
        length = len(self.message) if self.message else 0
        self.data=self.buffer[:length]
        self.length=length+1
        
    def __str__(self):
        command = self.commands.get(self.command, None)
        if command:
            return f'MIDI@{self.time} {command}[{self.channel}] {self.message}'
        else:
            data = self.stringify(self.data)
            return f'MIDI@{self.time} {self.command}[{self.channel}] {data}'
