'''
Created on 15 Sep 2019

@author: julianporter
'''


from enum import Enum
from MIDI.base import MIDIParserError
import MIDI.timing
from .chunk import Chunk

class DivisionMode(Enum):
    Metrical = 0
    TimeCode = 1


class Division:

    def __init__(self,div):
        self.division=div
        if (div & (1<<15)) == 0:
            self.mode = DivisionMode.Metrical
            self.ticks = div & 0x7fff
            self.smtpe = None
        else:
            self.mode = DivisionMode.TimeCode
            self.ticks = div & 0xff
            self.smtpe = MIDI.timing.SMTPEType.make2s(div >> 8)

    @property
    def ticksPerCrotchet(self):
        if self.mode == DivisionMode.Metrical:
            return self.ticks
        else:
            raise MIDIParserError(message="SMTPE TimeCode not yet implemented")

    def __str__(self):
        if self.smtpe is None:
            return f'{self.mode.name} @ {self.ticks} ticks per crotchet  [raw : {self.division}]'
        else:
            return f'SMTPE {self.smtpe} @ {self.ticks} ticks per frame  [raw : {self.division}]'


class Header(Chunk):

    def __init__(self,data=b''):
        super().__init__(data)
        self.format = self.build(data[:2])
        self.nTracks = self.build(data[2:4])
        self.division = Division(self.build(data[4:]))

    def __str__(self):
        return f'Format {self.format} nTracks: {self.nTracks} Timing: {self.division}'