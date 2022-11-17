'''
Created on 16 Sep 2019

@author: julianporter
'''
from MIDI.util import Converter

class SimpleMessage(object):

    def compute(self,data):
        return data[0]


    def __init__(self,name,data=b''):
        self.name=name
        self.value=self.compute(data)

    def __str__(self):
        return f'{self.name} := {self.value}'

    def __len__(self):
        return 1


class ProgramMessage(SimpleMessage):

    def __init__(self,data=b''):
        super().__init__('Program',data)

class ChannelPressureMessage(SimpleMessage):

    def __init__(self,data=b''):
        super().__init__('Pressure',data)

class PitchBendMessage(SimpleMessage):

    def compute(self, data):
        return Converter.Int16(data)-8192

    def __init__(self,data=b''):
        super().__init__('Bend',data)

    def __len__(self):
        return 2

