import time
import nfc
import requests
import uuid
import appsettings #you shouldnt need to edit this file
import usersettings #this is the file you might need to edit
import ndef

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import difflib

def find_uri_from_spotify(album, artist):
   print "Looking up album '%s' artist '%s'" % (album, artist)
   sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(usersettings.spotipy_client_id, usersettings.spotipy_client_secret))
   results = sp.search("album:%s artist:%s" % (album, artist), type="album")
   albums = results['albums']['items']
   items = {a['name']:a['uri'] for a in albums}
   elem = difflib.get_close_matches(album, items.keys(), 1)[0]
   uri = items[elem]
   return uri

def find_current_album():
   url = "/".join((usersettings.sonoshttpaddress, usersettings.sonosroom, "state"))
   response = requests.get(url)
   items = response.json()
   return items['currentTrack']['album'], items['currentTrack']['artist']

def write_current_album(tag):
   res = find_current_album()
   if not res:
      print "No album found"
      return False

   album, artist = res
   print "Current Album '%s' Artist '%s'" % (album, artist)
   uri = find_uri_from_spotify(album, artist)

   print "URI is %s" % uri

   print "Formatting tag"
   tag.format()

   print "Tag Formatted %s" % tag
   record = ndef.TextRecord(uri)
   tag.ndef.records = [record]
 
   print "Finished writing NDEF"  

   say_command = "Finished creating tag for artist %s and album %s" % (artist, album)
   url = "/".join((usersettings.sonoshttpaddress,usersettings.sonosroom, "say",say_command))
   requests.get(url)
   return True 

# this function gets called when a NFC tag is detected
def touched(tag):
    read_mode = tag.ndef and tag.ndef.records
    if read_mode:
        print "Received %d records"  % len(tag.ndef.records)
        for record in tag.ndef.records:
            receivedtext = record.text

            print("Read from NFC tag: "+ receivedtext)

            servicetype = ""

            if receivedtext.startswith ('spotify'):
                servicetype = "spotify"
                sonosinstruction = "spotify/now/" + receivedtext

            if receivedtext.startswith ('tunein'):
                servicetype = "tunein"
                sonosinstruction = receivedtext

            if receivedtext.startswith ('apple:'):
                servicetype = "applemusic"
                sonosinstruction = "applemusic/now/" + receivedtext[6:]

            if receivedtext.startswith ('applemusic:'):
                servicetype = "applemusic"
                sonosinstruction = "applemusic/now/" + receivedtext[11:]

            if receivedtext.startswith ('command'):
                servicetype = "command"
                sonosinstruction = receivedtext[8:]

            if servicetype == "":
                print ("Service type not recognised. Tag text should begin spotify, tunein, command or apple/applemusic (experimental). (Case matters: lower case please)")
                if usersettings.sendanonymoususagestatistics == "yes":
                    r = requests.post(appsettings.usagestatsurl, data = {'time': time.time(), 'value1': appsettings.appversion, 'value2': hex(uuid.getnode()), 'value3': 'invalid service type sent'})
                return True
            
            print ("Detected " + servicetype + " service request")

            #build the URL we want to request
            urltoget = usersettings.sonoshttpaddress + "/" + usersettings.sonosroom + "/" + sonosinstruction

            #clear the queue for every service request type except commands
            if servicetype <> "command":
                print ("Clearing Sonos queue")
                r = requests.get(usersettings.sonoshttpaddress + "/" + usersettings.sonosroom + "/clearqueue")

            #use the request function to get the URL built previously, triggering the sonos
            print ("Fetching URL via HTTP: "+ urltoget)
            r = requests.get(urltoget)
            print ("")

            #put together log data and send (if given permission)
            if usersettings.sendanonymoususagestatistics == "yes":
                logdata = {
                'time': time.time(),
                'value1': appsettings.appversion,
                'value2': hex(uuid.getnode()),
                'actiontype': 'nfcread',
                'value3': receivedtext,
                'servicetype': servicetype,
                'urltoget': urltoget
                }
                r = requests.post(appsettings.usagestatsurl, data = logdata)

    else:
        print ("Tag Blank - trying to format/write")
        write_current_album(tag) 

    return True

print("Setting up reader...")
reader = nfc.ContactlessFrontend('usb')
print(reader)
print("Ready!")
print("")

if usersettings.sendanonymoususagestatistics == "yes":
    r = requests.post(appsettings.usagestatsurl, data = {'time': time.time(), 'value1': appsettings.appversion, 'value2': hex(uuid.getnode()), 'value3': 'appstart'})

while True:
    response = reader.connect(rdwr={'on-connect': touched, 'beep-on-connect': False})
    if response:
        r = requests.get(usersettings.sonoshttpaddress + "/" + usersettings.sonosroom + "/playpause")
    else:
	break 
    time.sleep(0.1);
