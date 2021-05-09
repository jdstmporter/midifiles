'''
Created on 15 Sep 2019

@author: julianporter
'''

from .chunk import Chunk

class Header(Chunk):

    def __init__(self,data=b''):
        super().__init__(data)
        self.format = self.build(data[:2])
        self.nTracks = self.build(data[2:4])
        self.division = self.build(data[4:])
 
    def __str__(self):
        return f'Format {self.format} nTracks {self.nTracks} division {self.division}'
  
   
