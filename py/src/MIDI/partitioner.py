'''
Created on 14 Sep 2019

@author: julianporter
'''

import MIDI.chunks
from MIDI.base import Base

class MIDIFile(object):

    def __init__(self,filename):
        with open(filename,mode='rb') as file:
            self.bytes=file.read()
        self.header=None
        self.tracks=[]

    def readHeader(self):
        if len(self.bytes)<14:
            return False
        buffer=self.bytes[0:14]
        header=buffer[0:4].decode()
        length=Base.build(buffer[4:8])
        if header=='MThd' : # header
            if length != 6:
                return False
            self.header = MIDI.chunks.Header(buffer[8:8+length])
            return True
        return False


    def parse(self):
        buffer=self.bytes
        while len(buffer)>8:

            header=buffer[0:4].decode()
            length=Base.build(buffer[4:8])
            if header=='MThd' : # header
                if length != 6:
                    raise Exception('Header chunk must have length 6')
                self.header = MIDI.chunks.Header(buffer[8:8+length])

            elif header=='MTrk' : # track
                self.tracks.append(MIDI.chunks.Track(buffer[8:8+length]))
            else:
                print(f'Unknown chunk type {header} - skipping')
            buffer = buffer[8+length:]

    def __str__(self):
        out=[]
        if self.header:
            out.append("Header:")
            out.append(str(self.header))
        else:
            out.append('No header!')
        for idx, track in enumerate(self):
            out.append(f'\tTrack {idx} of length {len(track)}')
        return '\n'.join(out)

    def __iter__(self):
        return iter(self.tracks)

    def __len__(self):
        return len(self.tracks)

    def __getitem__(self,index):
        return self.tracks[index]

    @property
    def format(self):
        return self.header.format

    @property
    def division(self):
        return self.header.division









