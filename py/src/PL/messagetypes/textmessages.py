'''
Created on 9 May 2021

@author: julianporter
'''
from .core import BaseMessage

class TextMessage(BaseMessage):
    ChanName      =192    # name for the current channel
    PatName       =192+1    # name for the current pattern
    Title         =192+2    # title of the loop
    Comment       =192+3    # old comments in text format. Not used anymore
    SampleFileName    =192+4    # filename for the sample in the current channel, stored as relative path
    URL           =192+5
    CommentRTF    =192+6      # new comments in Rich Text format
    Version            =192+7
    PluginName    =192+9    # plugin file name (without path)
    
    MIDICtrls          =192+16
    Delay              =192+17
    TS404Params        =192+18
    DelayLine          =192+19
    NewPlugin          =192+20
    PluginParams       =192+21
    ChanParams        =192+23     # block of various channel params (can grow)
    
    @classmethod
    def payloadLength(cls):
        return -1