'''
Created on 16 Sep 2019

@author: julianporter
'''
from MIDI.util import SafeEnum
from .converters import ConversionEnum, Converter

class SMTPEType(SafeEnum):
    FPS24 = 0
    FPS25 = 1
    FPS30Drop = 2
    FPS30 = 3

    @property
    def fps(self):
        c = SMTPEType
        return { c.FPS24 : 24, c.FPS25 : 25, c.FPS30Drop : 30, c.FPS30 : 30 }.get(self,30)


class TimeCodeMessages(SafeEnum):

    Frame_Number_LSB = 0x00
    Frame_Number_MSB = 0x10
    Second_LSB = 0x20
    Second_MSB = 0x30
    Minute_LSB = 0x40
    Minute_MSB = 0x50
    Hour_LSB = 0x60
    Rate_And_Hour_MSB = 0x70

def TimeCode(data):
    x = data[0]
    value = x & 0x1f
    kind = TimeCodeMessages(x&0x70)
    if kind == TimeCodeMessages.Rate_And_Hour_MSB:
        smtpe = SMTPEType((x>>5)&3)
        return f'Type: Hour_MSB value: {value} SMTPE : {str(smtpe)}'
    else:
        return f'Type: {str(kind)} value: {value}'





class SystemMessages(ConversionEnum):

    Exclusive = 0
    Time_Code_Quarter_Frame = (1,TimeCode)
    Song_Position_Pointer = (2,Converter.Int16)
    Song_Select = 3
    Tune_Request = (6,Converter.Null)
    End_Of_Exclusive = (7,Converter.Null)
    RT_Timing_Clock = (8,Converter.Null)
    RT_Start = (10,Converter.Null)
    RT_Continue = (11,Converter.Null)
    RT_Stop = (12,Converter.Null)
    RT_Active_Sensing = (14,Converter.Null)
    RT_Reset = (15,Converter.Null)

    def length(self):
        cls=self.__class__
        if self == cls.Exclusive:
            return None
        elif self in [cls.Time_Code_Quarter_Frame,cls.Song_Select]:
            return 1
        elif self == cls.Song_Position_Pointer:
            return 2
        else:
            return 0

class SystemMessage(object):

    def __init__(self,data=b''):

        command=SystemMessages.make(data[0]&15)
        if command:
            self.command=command
            self.value=command(data[1:])
            self.length=command.length or 0
        else:
            self.command=data[0]
            self.value=data[1:]
            self.length=len(data)-1

    def __len__(self):
        return self.length

    def __str__(self):
        if self.value is not None:
            return f'{str(self.command)} := {self.value}'
        else:
            return str(self.command)

