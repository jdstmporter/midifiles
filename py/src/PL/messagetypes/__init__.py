from .core import BaseMessage,BadMessage
from .int8messages import Int8Message
from .int16messages import Int16Message
from .int32messages import Int32Message
from .textmessages import TextMessage 

MessageTypes = [Int8Message,Int16Message,Int32Message,TextMessage]
PayloadLengths = [1,2,4,-1]

from PL.base import PLParserError

def payloadLength(idx):
    try:
        return PayloadLengths[idx//64]
    except:
        raise PLParserError(f'Received bad event index {idx}')

def messageType(idx):
    try:
        return MessageTypes[idx//64]
    except:
        raise PLParserError(f'Received bad event index {idx}')  
    
def isNumeric(idx):
    return payloadLength(idx)>0

def isText(idx):
    return payloadLength(idx)<0