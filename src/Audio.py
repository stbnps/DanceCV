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

import pygame
import sys


# Audioo class

class Audio():
    def __init__(self):
        pass

    def pre_open(self, frequency=44100, bits=16, stereo=True, bufferSize=1024):
        pygame.mixer.pre_init(frequency, -bits, stereo and 2 or 1, bufferSize)
        return True

    def open(self, frequency=44100, bits=16, stereo=True, bufferSize=1024):
        try:
            pygame.mixer.quit()
        except:
            pass

        try:
            pygame.mixer.init(frequency, -bits, stereo and 2 or 1, bufferSize)
        except:
            pygame.mixer.init()

        return True

    def getChannelCount(self):
        return pygame.mixer.get_num_channels()

    def getChannel(self, n):
        return Channel(n)

    def close(self):
        pygame.mixer.quit()

    def pause(self):
        pygame.mixer.pause()

    def unpause(self):
        pygame.mixer.unpause()

class Music():
    def __init__(self, fileName):
        pygame.mixer.music.load(fileName)

    @staticmethod
    def setEndEvent(event):
        pygame.mixer.music.set_endevent(event)

    def play(self, loops= -1, pos=0.0):
        pygame.mixer.music.play(loops, pos)

    def stop(self):
        pygame.mixer.music.stop()

    def rewind(self):
        pygame.mixer.music.rewind()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def setVolume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def fadeout(self, time):
        pygame.mixer.music.fadeout(time)

    def isPlaying(self):
        return pygame.mixer.music.get_busy()

    def getPosition(self):
        return pygame.mixer.music.get_pos()

class Channel(object):
    def __init__(self, id):
        self.channel = pygame.mixer.Channel(id)

    def play(self, sound):
        self.channel.play(sound.sound)

    def stop(self):
        self.channel.stop()

    def setVolume(self, volume):
        self.channel.set_volume(volume)

    def fadeout(self, time):
        self.channel.fadeout(time)

class Sound(object):
    def __init__(self, fileName):
        self.sound = pygame.mixer.Sound(fileName)

    def play(self, loops=0):
        self.sound.play(loops)

    def stop(self):
        self.sound.stop()

    def setVolume(self, volume):
        self.sound.set_volume(volume)

    def fadeout(self, time):
        self.sound.fadeout(time)
        
        

class StreamingSound(Sound):
    def __init__(self, engine, channel, fileName):
        Sound.__init__(self, fileName)

