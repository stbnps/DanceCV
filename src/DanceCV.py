#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (c) 2014, Esteban Pardo Sánchez
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from Resource import Resource
from Audio import Audio
from Scene import Scene
from Song import Song, Note, loadSong
from Input import Input
import pygame
from pygame.locals import *
import sys
import getopt
import Constants
#import cProfile as profile

class DanceCV():
    def __init__(self, song, speed):

        self.input = Input()
        self.resource = Resource()
        self.audio = Audio()
        self.audio.pre_open()
        pygame.init()
        self.audio.open()
        if song != None:
            self.song = loadSong(self.resource, song)
        else:
            self.song = loadSong(self.resource, "gangnam")
        self.clock = pygame.time.Clock()
        pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        pygame.display.set_caption("DanceCV")
        screen = pygame.display.get_surface()
        if speed != None:
            self.scene = Scene(self.resource, self.song, screen, self.input, speed)
        else:
            self.scene = Scene(self.resource, self.song, screen, self.input, 2)

        
        
    def run(self):
        while True:
            for events in pygame.event.get():
                if events.type == QUIT:
                    sys.exit(0)
            self.input.run()
            self.scene.run()
            pygame.display.update()
            self.clock.tick(30)
    
    
    
if __name__ == "__main__":
    song = None
    speed = None
    options, remainder = getopt.getopt(sys.argv[1:], 's:x:')
    for opt, arg in options:
        
        if opt in ('-s'):
            song = arg
        elif opt in ('-x'):
            speed = float(arg)
    game = DanceCV(song, speed)
    game.run()
    
