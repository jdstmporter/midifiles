'''
Created on 16 Sep 2019

@author: julianporter
'''
from MIDI.util import SafeEnum

class Converter(object):
    @staticmethod
    def Null(_):
        return None
 
    @staticmethod       
    def OnOff127(data):
        x = data[0]
        return {0: 'OFF', 127: 'ON'}.get(x,'???')

    @staticmethod        
    def Id1(x):
        return x[0]

    @staticmethod
    def Int16(data):
        return (data[0]&0x7f) + (data[1]&0x7f)*128


    
  
class ConversionEnum(SafeEnum):
    
    def __init__(self,*args):
        self.code=args[0]
        self.converter=args[1] if len(args)>1 else Converter.Id1
        
    @classmethod
    def make(cls, n):
        for obj in cls:
            if obj.code==n: return obj
        return None
    
    def __call__(self,value):
        return self.converter(value)
    