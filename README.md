# vinylemulator

Emulate the tactile experience of a vinyl collection through your Sonos system, but with a back end run by Spotify.

There is a step-by-step tutorial on how to set this up from first principles on a Raspberry Pi here: https://www.instructables.com/id/Sonos-Spotify-Vinyl-Emulator-SSVE/

<b>Description</b>

Start playing a Spotify album or playlist through Sonos when you place a physical object on an NFC reader connected to a Raspberry Pi.

You can attach these tiny NFC tags to any physical object you want: I like polaroid-style prints of album covers and tape cassettes for playlists/mixtapes, but you do you; send me a photo if you're baller enough to print album art on 12-inch square aluminium plates and tag it to that.

<b>Usage</b>

Originally fork from musicbox project https://github.com/pucbaldwin/musicbox which was itself a fork from songblocks project https://github.com/shawnrk/songblocks. I have rewritten and simplified this a lot, however, so this version looks very different to those two.

All the actual back end work of this is done by the node-sonos-http-api https://github.com/jishi/node-sonos-http-api/ which will need to be installed and setup in order to work.

This is not the first project to link NFC to Sonos / Spotify, but I couldn't find one that did both in the way I wanted. Unlike other projects of this type - which take a NFC tag id and cross reference that against a database on the Raspberry Pi to find the music URI - this project actually stores the album details directly on the NFC tag. This has a few advantages:

First, you can have a very large collection which will continue to exist independent of digital storage on the Raspberry Pi. Even if you manage to wipe the database on your Pi, your collection will live forever (just like real vinyl);

Second, these NFC tags aren't tied to the particular Raspberry Pi. This means that the tags are portable to other Raspberry Pis running the same scripts. So take your favourite jazz album from your city pad up to the country house to listen to in the study when it's Laphroig time, or take a rare deep cut you've stumbled across to a friend's house for a listening party. Other use cases are available for those who aren't millionaires.

It also means that other applications can read the tags - I am working on an implementation for Android phones which don't rely on Pi for the NFC, for instance.

It's all coded in Python. Kind of.

<b>Setup instructions</b>

I made a full tutorial, starting from absolute first principles, here:
https://www.instructables.com/id/Sonos-Spotify-Vinyl-Emulator-SSVE/
