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

import midi
import Audio
from ConfigParser import ConfigParser
import os

DEFAULT_LIBRARY         = "songs"

class SongInfo():
    def __init__(self, infoFileName):
        self.songName      = os.path.basename(os.path.dirname(infoFileName))
        self.fileName      = infoFileName
        self.info          = ConfigParser()

        try:
            self.info.read(infoFileName)
        except:
            pass

    def _set(self, attr, value):
        if not self.info.has_section("song"):
            self.info.add_section("song")
        value = str(value)
        self.info.set("song", attr, value)
    
    def _get(self, attr, type = None, default = ""):
        try:
            v = self.info.get("song", attr)
        except:
            v = default
        if v is not None and type:
            v = type(v)
        return v

    def getName(self):
        return self._get("name")

    def setName(self, value):
        self._set("name", value)

    def getArtist(self):
        return self._get("artist")
  
    def setArtist(self, value):
        self._set("artist", value)
    
    def getDelay(self):
        return self._get("delay", int, 0)
    
    def setDelay(self, value):
        return self._set("delay", value)
    
    def getBPM(self):
        return self._get("bpm", int, 0)

    name          = property(getName, setName)
    artist        = property(getArtist, setArtist)
    delay         = property(getDelay, setDelay)

class Event:
    def __init__(self, length):
        self.length = length

class Note(Event):
    def __init__(self, number, length, special = False, tappable = False):
        Event.__init__(self, length)
        self.number   = number
        self.played   = False
        self.special  = special
        self.tappable = tappable
    
    def __repr__(self):
        return "<#%d>" % self.number

class Tempo(Event):
    def __init__(self, bpm):
        Event.__init__(self, 0)
        self.bpm = bpm
    
    def __repr__(self):
        return "<%d bpm>" % self.bpm

class TextEvent(Event):
    def __init__(self, text, length):
        Event.__init__(self, length)
        self.text = text

    def __repr__(self):
        return "<%s>" % self.text

class PictureEvent(Event):
    def __init__(self, fileName, length):
        Event.__init__(self, length)
        self.fileName = fileName
    
class Track:  
    def __init__(self):
        self.events = []
        self.allEvents = []

    def addEvent(self, time, event):
        self.events.append((time, event))
        self.allEvents.append((time, event))

    def getEvents(self, startTime, endTime):
        events = set()
        for time, event in self.events:
            if time > startTime and time < endTime:
                events.add((time, event))
        return events

    def getUnplayedNotes(self, startTime, endTime):
        events = set()
        for time, event in self.events:
            if time > startTime and time < endTime:
                if isinstance(event, Note):
                    if not event.played:
                        events.add((time, event))
        return events
    
    def getNotes(self, startTime, endTime):
        events = set()
        for time, event in self.events:
            if time > startTime and time < endTime:
                if isinstance(event, Note):
                    events.add((time, event))
        return events
    
    def getAllEvents(self):
        return self.allEvents

    def reset(self):
        for eventList in self.events:
            for time, event in eventList:
                if isinstance(event, Note):
                    event.played = False

class Song(object):
    def __init__(self, infoFileName, songTrackName, noteFileName):
        self.info          = SongInfo(infoFileName)
        #self.track         = Track()
        self._playing      = False
        self.start         = 0.0
        self.noteFileName  = noteFileName
        self.bpm           = None
        self.period        = 0
        self.delay         = self.info.getDelay()

        # load the tracks
        if songTrackName:
            self.music       = Audio.Music(songTrackName)

        # load the notes
        if noteFileName:
            midiIn = midi.MidiInFile(MidiReader(self), noteFileName)
            midiIn.read()
  
    def setBpm(self, bpm):
        self.bpm    = bpm
        self.period = 60000.0 / self.bpm

    def play(self, start = 0.0):
        self.start = start
        self.music.play(0, start / 1000.0)
        self._playing = True

    def pause(self):
        self.music.pause()
        self.engine.audio.pause()

    def unpause(self):
        self.music.unpause()
        self.engine.audio.unpause()
  
    def setBackgroundVolume(self, volume):
        self.music.setVolume(volume)
  
    def stop(self):
        self.track.reset()
          
        self.music.stop()
        self.music.rewind()
        if self.guitarTrack:
            self.guitarTrack.stop()
        if self.rhythmTrack:
            self.rhythmTrack.stop()
        self._playing = False

    def fadeout(self, time):
        self.track.reset()
          
        self.music.fadeout(time)
        if self.guitarTrack:
            self.guitarTrack.fadeout(time)
        if self.rhythmTrack:
            self.rhythmTrack.fadeout(time)
        self._playing = False

    def getPosition(self):
        if not self._playing:
            pos = 0.0
        else:
            pos = self.music.getPosition()
        if pos < 0.0:
            pos = 0.0
        return pos + self.start

    def isPlaying(self):
        return self._playing and self.music.isPlaying()

    def getBeat(self):
        return self.getPosition() / self.period

    def update(self, ticks):
        pass

    def getTrack(self):
        return self.track

    track = Track() #fproperty(getTrack)

class MidiReader(midi.MidiOutStream):
    def __init__(self, song):
        midi.MidiOutStream.__init__(self)
        self.song = song
        self.heldNotes = {}
        self.velocity  = {}
        self.ticksPerBeat = 480
        self.tempoMarkers = []

    def addEvent(self, track, event, time = None):
        if time is None:
            time = self.abs_time()
        assert time >= 0
        if track is None:
            self.song.track.addEvent(time, event)


    def abs_time(self):
        def ticksToBeats(ticks, bpm):
            return (60000.0 * ticks) / (bpm * self.ticksPerBeat)
          
        if self.song.bpm:
            currentTime = midi.MidiOutStream.abs_time(self)
            #return currentTime
            # Find out the current scaled time.
            # Yeah, this is reeally slow, but fast enough :)
            scaledTime      = 0.0
            tempoMarkerTime = 0.0
            currentBpm      = self.song.bpm
            for i, marker in enumerate(self.tempoMarkers):
                time, bpm = marker
                if time > currentTime:
                    break
                scaledTime += ticksToBeats(time - tempoMarkerTime, currentBpm)
                tempoMarkerTime, currentBpm = time, bpm
            return scaledTime + ticksToBeats(currentTime - tempoMarkerTime, currentBpm)
        return midi.MidiOutStream.abs_time(self)

    def header(self, format, nTracks, division):
        self.ticksPerBeat = division
    
    def tempo(self, value):
        bpm = 60.0 * 10.0**6 / value
        self.tempoMarkers.append((midi.MidiOutStream.abs_time(self), bpm))
        if not self.song.bpm:
            self.song.setBpm(bpm)
        self.addEvent(None, Tempo(bpm))

    def note_on(self, channel, note, velocity):
        if self.get_current_track() > 1: return
        self.velocity[note] = velocity
        self.heldNotes[(self.get_current_track(), channel, note)] = self.abs_time()
        self.addEvent(None, Note(note, 1, special = self.velocity[note] == 127))
        
    def sysex_event(self, data):
        pass
  
  
def loadSong(resource, name, library = DEFAULT_LIBRARY,):
    songFile   = resource.fileName(library, name, "song.mp3")
    noteFile   = resource.fileName(library, name, "notes.mid", writable = True)
    infoFile   = resource.fileName(library, name, "song.ini", writable = True)
  
    song       = Song(infoFile, songFile, noteFile)
    return song

def loadSongInfo(engine, name, library = DEFAULT_LIBRARY):
    infoFile   = engine.resource.fileName(library, name, "song.ini", writable = True)
    return SongInfo(infoFile)
