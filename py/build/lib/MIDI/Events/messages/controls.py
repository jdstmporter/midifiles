'''
Created on 16 Sep 2019

@author: julianporter
'''


from MIDI.util.converters import ConversionEnum, Converter


def Pedals(data):
    x = data[0]
    onOff = 'OFF' if x<64 else 'ON'
    return f' {onOff} ({x})'

def LongString(data):
    return f'{data}'

def TruncatedString(data):
    l=len(data)
    if l<32:
        return f'{data}'
    else:
        return f'{data[:32]}... [{l-32} more]'

def TruncatedStringHex(data):
    return ' '.join([f'{d:02x}' for d in data[:48]])

class ControlMessages(ConversionEnum):
    Bank_Select = 0
    Mod_Wheel = 1
    Breath_Controller = 2
    Foot_Controller = 4
    Portameno_Time = 5
    Data_Entry_MSB = 6
    Channel_Volume = 7
    Balance = 8
    Pan = 10
    Data_Entry_LSB = 38
    Damper_Pedal = (64,Pedals)
    Portamento_Pedal = (65,Pedals)
    Sostenuto_Pedal = (66,Pedals)
    Soft_Pedal = (67,Pedals)
    Legato_Footswitch = (68,Pedals)
    Effects_1_Depth = (91,TruncatedString)
    Effects_2_Depth = (92,TruncatedString)
    Effects_3_Depth = (93,TruncatedString)
    Effects_4_Depth = (94,TruncatedString)
    Effects_5_Depth = (95,TruncatedString)
    RPN_LSB = 100
    RPN_MSB = 101
    All_Sound_Off = (120,Converter.Null)
    Reset_All_Controllers = (121,Converter.Null)
    Local_Control = (122,Converter.OnOff127)
    All_Notes_Off = (123,Converter.Null)
    Omni_Mode_Off = (124,Converter.Null)
    Omni_Mode_On = (125,Converter.Null)
    Mono_Mode_On = 126
    Poly_Mode_On = (127,Converter.Null)




class ControlMessage(object):

    def __init__(self,data=b''):

        command=ControlMessages.make(data[0])
        if command:
            self.command=command
            self.value=command(data[1:])
        else:
            self.command=data[0]
            self.value=data[1:]

    def __str__(self):
        if self.value is not None:
            return f'{str(self.command)} := {self.value}'
        else:
            return str(self.command)

    def __len__(self):
        return 2

