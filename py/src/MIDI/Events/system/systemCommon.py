'''
Created on 12 Nov 2022

@author: julianporter
'''

from .base import SystemMessageBase
from MIDI.timing import SMTPEType
from MIDI.util import SafeEnum, Converter


class SongPositionPointer(SystemMessageBase):

    def __init__(self,data=b''):
        self.data=data[:2]
        self.value=Converter.Int16(self.data)
        self.clocks = 6*self.value

    def __len__(self):
        return 2

    def __str__(self):
        return f'{self.clocks} clocks'

class SongSelect(SystemMessageBase):

    def __init__(self,data=b''):
        self.data=data[0]
        self.song=self.data & 0x7f

    def __len__(self):
        return 1

    def __str__(self):
        return f'{self.song}'

class TimeCodeMessages(SafeEnum):

    Frame_Number_LSB = 0x00
    Frame_Number_MSB = 0x10
    Second_LSB = 0x20
    Second_MSB = 0x30
    Minute_LSB = 0x40
    Minute_MSB = 0x50
    Hour_LSB = 0x60
    Rate_And_Hour_MSB = 0x70

class QuarterFrameMessage(SystemMessageBase):

    def __init__(self,data):
        self.data = data[0]
        self.kind = TimeCodeMessages(self.data&0x70)
        if self.kind == TimeCodeMessages.Rate_And_Hour_MSB:
            self.smtpe = SMTPEType((self.data>>1) & 0x03)
            self.value = self.data & 0x01
        else:
            self.smtpe = None
            self.value = self.data & 0x0f

    def __len__(self):
        return 1

    def __str__(self):
        if self.smtpe is not None:
            return f'Type: {str(self.kind)} value: {self.value} SMTPE : {str(self.smtpe)}'
        else:
            return f'Type: {str(self.kind)} value: {self.value}'