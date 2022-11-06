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

    def __str__(self):
        ns = [f'{self.fps} FPS']
        if self == SMTPEType.FPS30Drop:
            ns.append('drop frame')
        return ' '.join(ns)

class QuarterFrameMessage:

    def __init__(self,data):
        self.data = data[0]
        self.kind = TimeCodeMessages(self.data&0x70)
        if self.kind == TimeCodeMessages.Rate_And_Hour_MSB:
            self.smtpe = SMTPEType((self.data>>1) & 0x03)
            self.value = self.data & 0x01
        else:
            self.smtpe = None
            self.value = self.data & 0x0f


    def __str__(self):
        if self.smtpe is not None:
            return f'Type: {str(self.kind)} value: {self.value} SMTPE : {str(self.smtpe)}'
        else:
            return f'Type: {str(self.kind)} value: {self.value}'

class FullTimingMessage:

    def __init__(self,data):        # F0 7F 7F 01 01 <hr> <mn> <sc> <fr> F7
        self.data=data[:4]
        self.smtpe = SMTPEType((data[0]>>5)&0x03)
        self.hours = data[0] & 0x1f
        self.minutes = data[1]
        self.seconds = data[2]
        self.frames = data[3]

    def __str__(self):
        return f'Type: {str(self.smtpe)} @ {self.hours}:{self.minutes}:{self.seconds} + {self.frames} frames'
