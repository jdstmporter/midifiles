'''
Created on 30 Oct 2022

@author: julianporter
'''
from MIDI.util import SafeEnum

class TimeCodeMessages(SafeEnum):

    Frame_Number_LSB = 0x00
    Frame_Number_MSB = 0x10
    Second_LSB = 0x20
    Second_MSB = 0x30
    Minute_LSB = 0x40
    Minute_MSB = 0x50
    Hour_LSB = 0x60
    Rate_And_Hour_MSB = 0x70

class SMTPEType(SafeEnum):
    FPS24 = 0
    FPS25 = 1
    FPS30Drop = 2
    FPS30 = 3

    @property
    def fps(self):
        c = SMTPEType
        return { c.FPS24 : 24, c.FPS25 : 25, c.FPS30Drop : 29, c.FPS30 : 30 }.get(self,30)

    @classmethod
    def make2s(cls,value):
        fps = value if value<128 else -(value&0xff)
        matches = [x for x in SMTPEType if x.fps==fps]
        if len(matches)==0: return None
        return matches[0]



    @classmethod
    def make(cls,value):
        return SMTPEType((value>>5)&3)

class SMTPEInfo:

    def __init__(self,data):
        self.data = data[0]
        self.value = self.data & 0x1f
        self.kind = TimeCodeMessages(self.data&0x70)
        if self.kind == TimeCodeMessages.Rate_And_Hour_MSB:
            self.smtpe = SMTPEType.make(self.data)
        else:
            self.smtpe = None


    def __str__(self):
        if self.smtpe is not None:
            return f'Type: {str(self.kind)} value: {self.value} SMTPE : {str(self.smtpe)}'
        else:
            return f'Type: {str(self.kind)} value: {self.value}'