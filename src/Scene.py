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

from Song import Song, Note, loadSong
from Input import Input
import pygame
from pyhiero.pygamefont import PyGameHieroFont
import Constants
import math


class Scene():
    def __init__(self, resource, song, screen, input, beatsPerBoard = 2):
        self.input = input
        self.song = song
        self.screen = screen
        self.downLeft = pygame.image.load(resource.fileName("images", "DownLeft.png"))
        self.downRight = pygame.image.load(resource.fileName("images", "DownRight.png"))
        self.upLeft = pygame.image.load(resource.fileName("images", "UpLeft.png"))
        self.upRight = pygame.image.load(resource.fileName("images", "UpRight.png"))
        
        self.downLeftActive = pygame.image.load(resource.fileName("images", "DownLeftActive.png"))
        self.downRightActive = pygame.image.load(resource.fileName("images", "DownRightActive.png"))
        self.upLeftActive = pygame.image.load(resource.fileName("images", "UpLeftActive.png"))
        self.upRightActive = pygame.image.load(resource.fileName("images", "UpRightActive.png"))
        
        self.center = pygame.image.load(resource.fileName("images", "Center.png"))    
        self.glow = pygame.image.load(resource.fileName("images", "Glow.png")) 
        
        # ALL IMAGES HAVE SAME HEIGHT AND WIDTH
        Constants.SPRITE_SIZE = self.glow.get_width()
        self.beatsPerBoard = beatsPerBoard
        self.backgroundColor = (0,0,0)
        self.score = 0
        self.font = PyGameHieroFont(resource.fileName("font", "font.fnt"))
        
        self.opacityGlow = []
        for i in range(0,4):
            self.opacityGlow.append(0)
        
        self.calculateCenterTargetsDistance()
        
        Constants.SQRT_2 = math.sqrt(2)
        
        self.targetsHypotenuse = math.sqrt(2*(self.centerTargetsDistance-Constants.SPRITE_SIZE)*(self.centerTargetsDistance-Constants.SPRITE_SIZE))
        self.arrowTimeRelation = self.beatsPerBoard/self.targetsHypotenuse
        
        self.sceneClock = pygame.time.Clock()
        
    
        self.song.play()

    def blitAlpha(self, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(self.screen, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        self.screen.blit(temp, location)         
    
    def handleNotes(self):
        pos = self.song.getPosition()
        track = self.song.track
        period = self.song.period
        delay = self.song.delay
            
        for time, event in track.getUnplayedNotes(pos - delay - self.screenDelay - period * 2 , pos - delay - self.screenDelay + period * self.beatsPerBoard):
           
            delta = time - pos + delay + self.screenDelay
            delta = delta / period
            self.renderNote(event.number, delta)

    def renderNote(self, number, delta):
        d = delta/self.arrowTimeRelation
        d2 = d/Constants.SQRT_2
        if number == 0:
            self.screen.blit(self.upLeft, (d2,d2))
        elif number == 1:
            self.screen.blit(self.upRight, (Constants.SCREEN_WIDTH-d2-Constants.SPRITE_SIZE,d2))
        elif number == 2:
            self.screen.blit(self.downLeft, (d2,Constants.SCREEN_HEIGHT-d2-Constants.SPRITE_SIZE))
        elif number == 3:
            self.screen.blit(self.downRight, (Constants.SCREEN_WIDTH-d2-Constants.SPRITE_SIZE,Constants.SCREEN_HEIGHT-d2-Constants.SPRITE_SIZE))
    
    def calculateCenterTargetsDistance(self):
        if Constants.SCREEN_HEIGHT/2 > Constants.SCREEN_WIDTH/2:
            self.centerTargetsDistance = Constants.SCREEN_WIDTH/2
        else:
            self.centerTargetsDistance = Constants.SCREEN_HEIGHT/2
    
    def renderCenterTargets(self):
        self.screen.blit(self.center, (self.centerTargetsDistance - Constants.SPRITE_SIZE, self.centerTargetsDistance - Constants.SPRITE_SIZE))
        self.screen.blit(self.center, (Constants.SCREEN_WIDTH - self.centerTargetsDistance, self.centerTargetsDistance - Constants.SPRITE_SIZE))
        self.screen.blit(self.center, (self.centerTargetsDistance - Constants.SPRITE_SIZE,Constants.SCREEN_HEIGHT - self.centerTargetsDistance))
        self.screen.blit(self.center, (Constants.SCREEN_WIDTH- self.centerTargetsDistance,Constants.SCREEN_HEIGHT- self.centerTargetsDistance))
        
    def renderCornerTargets(self):

        if self.input.isActive(0):
            self.screen.blit(self.upLeftActive, (0,0))
        else:
            self.screen.blit(self.upLeft, (0,0))
            
        if self.input.isActive(1):
            self.screen.blit(self.upRightActive, (Constants.SCREEN_WIDTH-Constants.SPRITE_SIZE,0))
        else:
            self.screen.blit(self.upRight, (Constants.SCREEN_WIDTH-Constants.SPRITE_SIZE,0))
            
        if self.input.isActive(2):
            self.screen.blit(self.downLeftActive, (0,Constants.SCREEN_HEIGHT-Constants.SPRITE_SIZE))
        else:
            self.screen.blit(self.downLeft, (0,Constants.SCREEN_HEIGHT-Constants.SPRITE_SIZE))
            
        if self.input.isActive(3):
            self.screen.blit(self.downRightActive, (Constants.SCREEN_WIDTH-Constants.SPRITE_SIZE,Constants.SCREEN_HEIGHT-Constants.SPRITE_SIZE))
        else:
            self.screen.blit(self.downRight, (Constants.SCREEN_WIDTH-Constants.SPRITE_SIZE,Constants.SCREEN_HEIGHT-Constants.SPRITE_SIZE))
     
    
    def renderWebCam(self):
        frame = self.input.getCurrentFrameAsImage()
        self.screen.blit(frame, (0,0))
    
    def render(self):
        self.renderWebCam()
        self.renderCornerTargets()
        self.handleNotes()
        self.renderCenterTargets()   
        self.renderGlow()
        self.fadeGlow()
        self.renderScore()
        
    def renderGlow(self):
        self.blitAlpha(self.glow, (0,0), self.opacityGlow[0])
        self.blitAlpha(self.glow, (Constants.SCREEN_WIDTH-Constants.SPRITE_SIZE,0), self.opacityGlow[1])
        self.blitAlpha(self.glow, (0,Constants.SCREEN_HEIGHT-Constants.SPRITE_SIZE), self.opacityGlow[2])
        self.blitAlpha(self.glow, (Constants.SCREEN_WIDTH-Constants.SPRITE_SIZE,Constants.SCREEN_HEIGHT-Constants.SPRITE_SIZE), self.opacityGlow[3])
        
        
    def fadeGlow(self):
        for i in range(0,4):
            if self.opacityGlow[i] > 0:
                self.opacityGlow[i] -= Constants.GLOW_FADE
            
        
        
    
    def handleRequiredNotes(self, notes):
        arrows = [False, False, False, False]   
        for time, note in notes:
            if self.input.toggled(note.number):   
                if arrows[note.number] == False:
                    self.score += 50
                    note.played = True
                    arrows[note.number] = True
                    self.opacityGlow[note.number] = 255
                
                
                     
    def renderScore(self):
        scoreImage = self.font.render(str(self.score))
        self.screen.blit(scoreImage, 
                         (Constants.SCREEN_WIDTH/2 - scoreImage.get_width()/2, 0))
    
    
    def updateScore(self):
        pos = self.song.getPosition()
        track = self.song.track
        period = self.song.period
        delay = self.song.delay
        margin = period * 0.5      

        requiredNotes = track.getNotes(pos - delay - self.screenDelay - margin, pos - delay - self.screenDelay + margin)           
        update = [True, True, True, True]
        for time, event in requiredNotes:
            update[event.number] = False
        self.input.adapt(update)
        requiredNotes = track.getUnplayedNotes(pos - delay - self.screenDelay - margin, pos - delay - self.screenDelay + margin)                   
        self.handleRequiredNotes(requiredNotes)
        
    
    
    
    def run(self):
        self.screenDelay = self.sceneClock.tick()
        self.screen.fill(self.backgroundColor)
        self.updateScore()
        self.render()
        pygame.display.flip()
    
    
