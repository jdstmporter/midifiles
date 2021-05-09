'''
Created on 16 Sep 2019

@author: julianporter
'''


from .converters import ConversionEnum, Converter


def Pedals(data):
    x = data[0]
    onOff = 'OFF' if x<64 else 'ON'
    return f' {onOff} ({x})'


class ControlMessages(ConversionEnum):
    
    Data_Entry_MSB = 6
    Channel_Volume = 7
    Pan = 10
    Data_Entry_LSB = 38
    Damper_Pedal = (64,Pedals)
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
          
