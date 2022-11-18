'''
Created on 15 Sep 2019

@author: julianporter
'''
from MIDI.util import SafeEnum
from MIDI.timing import SMTPEType

class SysExBase:

    def __init__(self,enumKlass,data=b''):
        self.id2 = data[0]
        self.data = data[1:]

        self.kind = enumKlass.make(self.id2)
        self.str = str(self.data)

    def __len__(self):
        return len(self.data)

    def __str__(self):
        if self.kind is not None:
            return f'{self.kind} {self.str}'
        else:
            return f'{self.id2} {self.data}'

class MIDITimeCodeInstructions(SafeEnum):
    Full_Message=1
    User_Bits=2

class MIDITimeCode(SysExBase):

    def __init__(self,data=b''):
        super.__init__(MIDITimeCodeInstructions,data)

        if self.kind == MIDITimeCodeInstructions.Full_Message:
            self.smtpe = SMTPEType((self.data[0]>>5)&0x03)
            self.hours = self.data[0] & 0x1f
            self.minutes = self.data[1]
            self.seconds = self.data[2]
            self.frames = self.data[3]
            self.str = f'{str(self.smtpe)} @ {self.hours}:{self.minutes}:{self.seconds} + {self.frames} frames'


class MIDITuningStandardInstructions(SafeEnum):
    Note_Change = 2


class MIDITuningStandard(SysExBase):

    def __init__(self,data='b'):
        super.__init__(MIDITuningStandardInstructions,data)

class MIDINotationInstructions(SafeEnum):
    Bar_Number=1
    Time_Signature=2
    Time_Signature_Delayed=0x42

class MIDINotation(SysExBase):
    def __init__(self,data='b'):
        super.__init__(MIDINotationInstructions,data)

class DeviceControlInstructions(SafeEnum):
    Master_Volume=1
    Master_Balance=2

class DeviceControl(SysExBase):
    def __init__(self,data='b'):
        super.__init__(DeviceControlInstructions,data)

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

    def instance(self,data=b''):
        makers = {
            RTSysExKinds.MIDI_Time_Code: MIDITimeCode,
            RTSysExKinds.Notation_Information: MIDINotation,
            RTSysExKinds.Device_Control: DeviceControl,
            RTSysExKinds.MIDI_Tuning_Standard: MIDITuningStandard
            }
        klass = makers.get(self,SysExBase)
        return klass(data)

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

    def instance(self,data=b''):
        makers = {
            NonRTSysExKinds.Sample_Dump_Extensions: SampleDumpExtensions,
            NonRTSysExKinds.General_Information: GeneralInformation,
            NonRTSysExKinds.File_Dump: FileDump,
            NonRTSysExKinds.MIDI_Tuning_Standard: NRTMIDITuningStandard,
            NonRTSysExKinds.General_MIDI: GeneralMIDI
        }
        klass = makers.get(self,SysExBase)
        return klass(data)

class GeneralMIDIInstructions(SafeEnum):
    General_MIDI_Systems_On = 1
    General_MIDI_Systems_Off = 2

class GeneralMIDI(SysExBase):

    def __init__(self,data='b'):
        super.__init__(GeneralMIDIInstructions,data)

class GeneralInformationInstructions(SafeEnum):
    Identity_Request = 1
    Identity_Reply = 2

class GeneralInformation(SysExBase):

    def __init__(self,data='b'):
        super.__init__(GeneralInformationInstructions,data)

class NRTMIDITuningStandardInstructions(SafeEnum):
    Bulk_Dump_Request = 0
    Bulk_Dump_Reply_Reply = 1

class NRTMIDITuningStandard(SysExBase):

    def __init__(self,data='b'):
        super.__init__(NRTMIDITuningStandardInstructions,data)

class FileDumpInstructions(SafeEnum):
    Header = 1
    Data_Packet = 2
    Request = 3

class SampleDumpExtensionsInstructions(SafeEnum):
    Multiple_Loop_Points = 1
    Loop_Points_Request = 2

class SampleDumpExtensions(SysExBase):

    def __init__(self,data='b'):
        super.__init__(SampleDumpExtensionsInstructions,data)

class FileDump(SysExBase):

    def __init__(self,data='b'):
        super.__init__(FileDumpInstructions,data)


class RTSysEx:

    def __init__(self,data=b''):
        self.id1 = data[0]
        self.data=data[1:]
        self.kind = RTSysExKinds.make(self.id1)
        if self.kind is not None:
            self.message=self.kind.instance(self.data)
        else:
            self.message=self.data

    def __str__(self):
        return self.message

    def __len__(self):
        return len(self.message)

class NonRTSysEx:

    def __init__(self,data=b''):
        self.id1 = data[0]
        self.data=data[1:]
        self.kind = NonRTSysExKinds.make(self.id1)
        if self.kind is not None:
            self.message=self.kind.instance(self.data)
        else:
            self.message=self.data

    def __str__(self):
        return self.message

    def __len__(self):
        return len(self.message)

class SysExKind(SafeEnum):
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

class SysEx:

    def __init__(self,data=b''):

        self.kind = SysExKind.make(data[0] & 0x7f)
        self.deviceID = data[1] & 0x7f
        self.data=data[2:]

        if self.kind == SysExKind.RT_SysEx:
            self.content = RTSysEx(self.data)
        elif self.kind == SysExKind.Non_RT_SysEx:
            self.content = NonRTSysEx(self.data)
        else:
            self.content = self.data

    def __len__(self):
        return len(self.message)

    def __str__(self):
        kind = str(self.kind) if self.kind is not None else "-"
        message = str(self.content) if self.message is not None else str(self.data)
        return f'Device {self.deviceID} of kind {kind} : {message}'








