'''
Created on 8 May 2021

@author: julianporter
'''
from .chunk import Chunk 

class Header(Chunk):

    def __init__(self,data=b''):
        super().__init__(data)
        try:
            self.format = Chunk.getInt16(self.data[0:2])
            self.nTracks = Chunk.getInt16(self.data[2:4])
            self.division = Chunk.getInt16(self.data[4:6])
        except:
            self.format = 0
            self.nTracks = 0
            self.division=0
 
    def __str__(self):
        return f'Format {hex(self.format)} nTracks {hex(self.nTracks)} division {hex(self.division)}'
  
   
