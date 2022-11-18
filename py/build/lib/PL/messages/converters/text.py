'''
Created on 13 May 2021

@author: julianporter
'''

from .base import Converter


class String8Converter(Converter):
    
    def __init__(self):
        super().__init__(separator='')
        
    def process(self,d):
        return chr(d) if d>30 and 3<128 else '.'

'''
class String16Converter(String8Converter):
    
    def __init__(self):
        super().__init__()
        
        
        
    def __call__(self,data):
        s=super().__call__(data)
        if len(s)>0: return s[0:-1:2]
        return ''
'''    
    
class String16Converter(Converter):
    
    def __init__(self):
        super().__init__()
        
        
        
    def __call__(self,data):
        return data.decode('utf16')


    