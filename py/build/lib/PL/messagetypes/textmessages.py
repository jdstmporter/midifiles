'''
Created on 9 May 2021

@author: julianporter
'''
from .core import BaseMessage
from enum import Enum
from PL.messages.converters import HEXConv,STR8Conv,STR16Conv

class Display(Enum):
    
    CSTRING = 1
    STRING16 = 2
    HEX = 3
    RAW = 4
    RTF = 5
    
    
displays = {
        Display.HEX: [208,209,212,219,221,226,227,229,237],
        Display.CSTRING: [199],
        Display.STRING16 : [194,195,197,200,201,202,203,204,205,206,207,230,231,239]
    }

converters = {
        Display.HEX: HEXConv,
        Display.CSTRING: STR8Conv,
        Display.STRING16 : STR16Conv
    }

class VAR(BaseMessage):
    
    ChanName            = 192    # name for the current channel
    PatName             = 193    # name for the current pattern
    Title               = 194    # title of the loop
    Comment             = 195    # old comments in text format. Not used anymore
    SampleFileName      = 196    # filename for the sample in the current channel, stored as relative path
    URL                 = 197
    CommentRTF          = 198      # new comments in Rich Text format
    Version             = 199
    RegName             = 200
    DefPluginName       = 201   # plugin file name (without path)
    ProjDataPath        = 202
    PluginName          = 203 # plugin's name
    FXName              = 204
    TimeMarker          = 205 # time marker name
    Genre               = 206
    Author              = 207
    MIDICtrls           = 208
    Delay               = 209
    TS404Params         = 210
    DelayLine           = 211
    NewPlugin           = 212
    PluginParams        = 213
    Reserved2           = 214 # used once for testing
    ChanParams          = 215     # block of various channel params (can grow)
    CtrlRecChan         = 216 # automated controller events
    PLSel               = 217 # selection in playlist
    Envelope            = 218
    BasicChanParams     = 219
    OldFilterParams     = 220
    ChanPoly            = 221
    NoteEvents          = 222
    AutomationData      = 223
    PatternNotes        = 224
    InitCtrlRecChan     = 225 # init values for automated events
    RemoteCtrl_MIDI     = 226 # remote control entry (MIDI)
    RemoteCtrl_Int      = 227 # remote control entry (internal)
    Tracking            = 228 # vol/kb tracking
    ChanOfsLevels       = 229 # levels offset
    RemoteCtrlFormula   = 230 # remote control entry formula
    ChanGroupName       = 231
    RegBlackList        = 232 # black list of reg codes
    PlayListItems       = 233
    ChanAC              = 234 # channel articulator
    FXRouting           = 235
    FXParams            = 236
    ProjectTime         = 237
    PLTrackInfo         = 238
    PLTrackName         = 239
    
    
    
    
    def getConverter(self):
        display=Display.RAW
        for k, v in displays.items():
            if self.value in v: display=k
        return converters.get(display,STR8Conv)
    
       
    
    @classmethod
    def allObsolete(cls):
        return [VAR.ChanName,
                VAR.DelayLine,
                VAR.OldFilterParams] 
        
       

    
    @classmethod
    def payloadLength(cls):
        return -1
    
    
    def asString(self,value):
        converter = self.getConverter()
        return converter(value)
    
