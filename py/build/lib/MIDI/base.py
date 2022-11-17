'''
Created on 15 Sep 2019

@author: julianporter
'''

class MIDIParserError(Exception):
    
    def __init__(self,*args,**kwargs):
        self.extras=kwargs
        if 'message' not in self.extras:
            if len(args)>0:
                self.extras['message']=str(args[0])
            else:
                self.extras['message']=''
        if 'exception' not in self.extras:
            self.extras['exception']=None
        
    def __getattr__(self,key):
        return self.extras.get(key)
    
    def __getitem__(self,key):
        return self.extras[key]
    
    def __len__(self):
        return len(self.extras)
    
    def __iter__(self):
        return iter(self.extras)
    
    def __str__(self):
        return self.message
    
        

class Base(object):
    
    @classmethod
    def stringify(cls,array=[],separator=' '):
        return separator.join([str(x) for x in array])
    
    @classmethod
    def build(cls,buffer,nBits=8):
        mask=(1<<nBits)-1
        out=0
        for b in buffer:
            out = (out<<nBits) | (b&mask)
        return out
    
    def __init__(self,buffer=b''):
        self.buffer=buffer
    
    def getChunk(self,n=4):
        tmp=self.buffer[:n]
        self.buffer=self.buffer[n:]
        return tmp
    
    def getInt(self,n=4):
        tmp=self.getChunk(n)
        return self.build(tmp)
    
    def getVarLengthChunk(self):
        length = len(self.buffer)
        count=0
        while count<length and self.buffer[count]>=128:
            count+=1
        if count==length:
            raise Exception('Ran off end of file looking for variable length quantity')
        return self.getChunk(count+1)
    
    def getVarLengthInt(self):
        chunk=self.getVarLengthChunk()
        return self.build(chunk,nBits=7), len(chunk)
    
