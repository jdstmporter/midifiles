'''
Created on 15 Sep 2019

@author: julianporter
'''
from MIDI.util import SafeEnum
import MIDI.timing
from enum import Enum
from .systemCommon import SystemMessageBase, NullMessage


class SysExKind(Enum):
    Commercial_ID = 0
    Non_Commercial_ID = 1
    Non_RT_SysEx = 2
    RT_SysEx = 3

    @classmethod
    def make(cls,value=0x7f):
        value = value & 0x7f
        if value == 0x7f:
            return cls.RT_SysEx
        elif value == 0x7e:
            return cls.Non_RT_SysEx
        elif value == 0x7d:
            return cls.Non_Commercial_ID
        else:
            return cls.Commercial_ID



class NonRTSysExKinds(SafeEnum):
    Unused = 0
    Sample_Dump_Header = 1
    Sample_Data_Packet = 2
    Sample_Dump_Request = 3
    MIDI_Time_Code = 4
    Sample_Dump_Extensions = 5
    General_Information = 6
    File_Dump = 7
    MIDI_Tuning_Standard = 8
    General_MIDI = 9
    End_Of_File = 0x7b
    Wait = 0x7c
    Cancel = 0x7d
    NAK = 0x7e
    ACK = 0x7f

class RTSysExKinds(SafeEnum):
    Unused = 0
    MIDI_Time_Code = 1
    MIDI_Show_Control = 2
    Notation_Information = 3
    Device_Control = 4
    RT_MTC_Cueing = 5
    MIDI_Machine_Control_Commands = 6
    MIDI_Machine_Control_Responses = 7
    MIDI_Tuning_Standard = 8

class MIDITuningStandard:

    def __init__(self,data=b''):
        self.id = data[0]
        self.data=data[1:]

    def __len__(self):
        return len(self.data)

    def __str__(self):
        part = 'Note change' if self.id==2 else f'{self.id}'
        return f'{part} : {self.data}'

class MIDIMachineControl:

    def __init__(self,data=b''):
        self.command = data[0]
        self.data=data[1:]

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return f'{self.command} : {self.data}'


class SysEx:

    def __init__(self,data=b''):

        self.kind = SysExKind.make(data[0] & 0x7f)
        self.deviceID = data[1] & 0x7f

        id1=None
        if len(data) > 2:
            id1 = data[2]
        id2 = None
        if len(data) > 3:
            id2 = data[3]
        self.subID1 = id1
        self.subID2 = id2
        self.data = data[2:]



        super().__init__(time, buffer)
        self.type=self.header & 0x0f

        length, n=self.getVarLengthInt()
        self.data=self.buffer[:length]
        self.length=length+n+1

        self.deviceID = self.data[1]
        self.isGlobal = self.deviceID == 0x7f

        id1 = None
        if len(self.data) > 2:
            id1 = self.data[2]
        id2 = None
        if len(self.data) > 3:
            id2 = self.data[3]
        self.subID1 = id1
        self.subID2 = id2

        if self.subID1 == 1:
            self.attributes["SysExId"] = "MIDI Time Code"
            if self.subID2 == 1:
                self.attributes["SysExId2"] = "Full Time Code Message"
                self.attributes["SMTPE type"] = MIDI.timing.SMTPEType.make(self.data[4])
                self.attributes["Hours"] = self.data[4] & 0x1f
                self.attributes["Minutes"] = self.data[5]
                self.attributes["Seconds"] = self.data[6]
                self.attributes["Frames"] = self.data[7]
            elif self.subID2 == 2:
                self.attributes["SysExId2"] = "User Bits Message"



    def __str__(self):
        return f'SYSEX@{self.time} {self.type} {self.data} length = {self.length} [{self.deviceID}:{self.subID1}:{self.subID2}]'




