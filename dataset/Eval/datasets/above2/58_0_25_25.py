# -*- coding: utf-8 -*-




class ImageComparer():


    def __init__(self):
        self.reset()
        

    def reset(self):
        self.hash = None

    def checksum(self,msg):
        v = 21
        for c in msg:
            v ^= c
        return v

#         hash = self.checksum(msg)

    def check(self,msg):

        result = (self.hash == hash)
        self.hash = hash
        return result