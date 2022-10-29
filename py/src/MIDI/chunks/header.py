'''
Created on 15 Sep 2019

@author: julianporter
'''

from .chunk import Chunk
#from enum import Enum
#from MIDI.base import MIDIParserError

'''
class DivisionMode(Enum):
    Metrical = 0
    TimeCode = 1

class SMTPEFormat(Enum):
    FPS24 = -24
    FPS25 = -25
    FPS30Drop = -29
    FPS30 = -30

    @classmethod
    def byValue(cls,value):
        return [x for x in cls if x.value==value][0]

    @property
    def fps(self):
        return -self.mode.value

def twosComplement(coded):
    x = coded & 0xff
    return x if x<128 else x-256

class SMTPE:

    def __init__(self,slug):
        slug =slug | 0x8000
        self.mode = SMTPEFormat.byValue(twosComplement(slug>>8))
        self.resolution = slug & 0xff



class Division:



    def __init__(self,div):
        self.division=div
        if (div & (1<<15)) == 0:
            self.mode = DivisionMode.Metrical
            self.ticks = div & 0x7fff
            self.smtpeFormat
        else:
            self.mode = DivisionMode.TimeCode
            self.ticks = div & 0xff
            self.smtpe = (div >> 8) & 0x7f

    @property
    def ticksPerCrotchet(self):
        if self.mode == DivisionMode.Metrical:
            return self.ticks
        else:
            raise MIDIParserError(message="SMTPE TimeCode not yet implemented")

    def __str__(self):
        return f'{self.mode.name} ticks = {self.ticks}  [raw : {self.division}]'

'''
class Header(Chunk):

    def __init__(self,data=b''):
        super().__init__(data)
        self.format = self.build(data[:2])
        self.nTracks = self.build(data[2:4])
        self.division = self.build(data[4:])

    def __str__(self):
        return f'Format {self.format} nTracks {self.nTracks} division {self.division}'


