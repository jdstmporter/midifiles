'''
Created on 30 Oct 2022

@author: julianporter
'''
from MIDI.util import SafeEnum



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

class FullTimingMessageKind(SafeEnum):
    Full_Message = 1
    User_Bits = 2

    @classmethod
    def make(cls,value):
        hits = [x for x in cls if x.value==value]
        hits.append(None)
        return hits[0]

class FullTimingMessage:

    def __init__(self,data):        # F0 7F 7F 01 01 <hr> <mn> <sc> <fr> F7
        self.kind = FullTimingMessageKind.make(data[0])
        self.data=data[1:]
        if self.kind == FullTimingMessageKind.Full_Message:
            self.smtpe = SMTPEType((data[0]>>5)&0x03)
            self.hours = data[0] & 0x1f
            self.minutes = data[1]
            self.seconds = data[2]
            self.frames = data[3]

    def __str__(self):
        if self.kind == FullTimingMessageKind.Full_Message:
            return f'Full message: {str(self.smtpe)} @ {self.hours}:{self.minutes}:{self.seconds} + {self.frames} frames'
        elif self.kind == FullTimingMessageKind.User_Bits:
            return f'User bits: {self.data}'
        else:
            return 'Unknown timing message type'
