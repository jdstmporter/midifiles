'''
Created on 16 Sep 2019

@author: julianporter
'''


from MIDI.Events.system import NullMessage, QuarterFrameMessage, SongPositionPointer, SongSelect, SysEx

from MIDI.util import SafeEnum


class SystemKind(SafeEnum):

    Exclusive = 0
    Time_Code_Quarter_Frame = 1
    Song_Position_Pointer = 2
    Song_Select = 3
    Tune_Request = 6
    End_Of_Exclusive = 7
    RT_Timing_Clock = 8
    RT_Start = 10
    RT_Continue = 11
    RT_Stop = 12
    RT_Active_Sensing = 14
    RT_Reset = 15

    @property
    def isExclusive(self):
        return self == SystemKind.Exclusive

    @property
    def isRT(self):
        return self.value >= 8

    def instance(self,data = []):
        lookup = {
            SystemKind.Exclusive : SysEx,
            SystemKind.Time_Code_Quarter_Frame : QuarterFrameMessage,
            SystemKind.Song_Position_Pointer : SongPositionPointer,
            SystemKind.Song_Select : SongSelect
        }
        klass = lookup.get(self,NullMessage)
        return klass(data)




class SystemMessage:

    def __init__(self,data=b''):

        command=SystemKind.make(data[0]&15)
        if command:
            self.command=command
            self.data=command(data[1:])
            self.message = self.command.instance(self.data)
            self.length=len(self.message) or 0
        else:
            self.command=data[0]
            self.value=data[1:]
            self.messsage=None
            self.length=len(data)-1

    def __len__(self):
        return self.length

    def __str__(self):
        if self.message is not None:
            return f'{str(self.command.name)} := {self.message}'
        else:
            return str(self.command)




