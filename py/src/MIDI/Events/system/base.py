'''
Created on 13 Nov 2022

@author: julianporter
'''

class SystemMessageBase:

    def __init__(self,data=b''):
        pass

    def __len__(self):
        return 0

    def __str__(self):
        return ""


class NullMessage(SystemMessageBase):

    def __init__(self,data=b''):
        pass
