'''
Created on 15 Sep 2019

@author: julianporter
'''

from collections import OrderedDict
from .event import Event
from MIDI.util import SafeEnum

class MetaEventKinds(SafeEnum):

    Sequence_Number = 0
    Text = 1
    Copyright_Notice = 2
    Track_Name = 3
    Instrument_Name = 4
    Lyric = 5
    Marker = 6
    Cue_Point = 7
    MIDI_Channel_Prefix = 0x20
    End_Of_Track = 0x2f
    Set_Tempo = 0x51
    SMTPE_Offset = 0x54
    Time_Signature = 0x58
    Key_Signature = 0x59
    Sequencer_Specific = 0x7f

    def key(self,n):
        if n>=0:
            return ['C','G','D','A','E','B','F#','C#'][n]
        else:
            return ['C','F','Bb','Eb','Ab','Db','Gb','Cb'][-n]



    def attributes(self,_bytes=b''):
        cls=self.__class__
        if self in [cls.Text,cls.Copyright_Notice,cls.Track_Name,cls.Instrument_Name,cls.Lyric,cls.Marker,cls.Cue_Point]:
            return OrderedDict(text = _bytes)
        elif self==cls.Sequence_Number:
            return OrderedDict(number = Event.build(_bytes[:2]))
        elif self==cls.MIDI_Channel_Prefix:
            return OrderedDict(channel = _bytes[0]&0x0f)
        elif self==cls.End_Of_Track:
            return OrderedDict()
        elif self==cls.Set_Tempo:
            microsecondsPerCrotchet=Event.build(_bytes[:3])
            crotchetsPerMinute=60000000/microsecondsPerCrotchet
            return OrderedDict(tempo = microsecondsPerCrotchet, bpm = crotchetsPerMinute)
        elif self==cls.SMTPE_Offset:
            return OrderedDict(hh=_bytes[0],mm=_bytes[1],ss=_bytes[2],frame=_bytes[3]+0.01*_bytes[4])
        elif self==cls.Time_Signature:
            return OrderedDict(numerator=_bytes[0],denominator=(1<<_bytes[1]),clocksPerTick=_bytes[2],demisemiquaverPer24Clocks=_bytes[3])
        elif self==cls.Key_Signature:
            mode = { 0 : 'major', 1 : 'minor' }[_bytes[1]]
            return OrderedDict(key=self.key(_bytes[0]),mode=mode)
        elif self==cls.Sequencer_Specific:
            return OrderedDict(data=_bytes)
        else:
            return OrderedDict()




class MetaEvent(Event):

    def __init__(self,time,buffer):
        super().__init__(time, buffer)
        self.type=self.getInt(1)
        length, n=self.getVarLengthInt()
        self.data=self.getChunk(length)
        self.length=length+n+2

        self.message = MetaEventKinds.make(self.type)
        if self.message:
            self.attributes = self.message.attributes(self.data)


    def __str__(self):
        if self.message:
            attrs = self.stringify([f'{k}={v}' for k,v in self.attributes.items()])
            return f'META@{self.time} {self.message} -> {attrs}'
        else:
            data = self.stringify(self.data)
            return f'META@{self.time} {self.type} -> {data}'


