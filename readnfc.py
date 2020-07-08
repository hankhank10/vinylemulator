import time
import nfc
import requests
import uuid
import appsettings #you shouldnt need to edit this file
import usersettings #this is the file you might need to edit

# this function gets called when a NFC tag is detected
def touched(tag):
    global sonosroom_local

    if tag.ndef:
        for record in tag.ndef.records:
            receivedtext = record.text
            receivedtext_lower = receivedtext.lower()

            print("Read from NFC tag: "+ receivedtext)

            servicetype = ""

            if receivedtext_lower.startswith ('spotify'):
                servicetype = "spotify"
                sonosinstruction = "spotify/now/" + receivedtext

            if receivedtext_lower.startswith ('tunein'):
                servicetype = "tunein"
                sonosinstruction = receivedtext

            if receivedtext_lower.startswith ('apple:'):
                servicetype = "applemusic"
                sonosinstruction = "applemusic/now/" + receivedtext[6:]

            if receivedtext_lower.startswith ('applemusic:'):
                servicetype = "applemusic"
                sonosinstruction = "applemusic/now/" + receivedtext[11:]

            if receivedtext_lower.startswith ('command'):
                servicetype = "command"
                sonosinstruction = receivedtext[8:]
            
            if receivedtext_lower.startswith ('room'):
                servicetype = "room"
                sonosroom_local = receivedtext[5:]
                print ("Sonos room changed to " + sonosroom_local)
                return True

            if servicetype == "":
                print ("Service type not recognised. Tag text should begin spotify, tunein, command, room or apple/applemusic.")
                if usersettings.sendanonymoususagestatistics == "yes":
                    r = requests.post(appsettings.usagestatsurl, data = {'time': time.time(), 'value1': appsettings.appversion, 'value2': hex(uuid.getnode()), 'value3': 'invalid service type sent'})
                return True
            
            print ("Detected " + servicetype + " service request")

            #build the URL we want to request
            urltoget = usersettings.sonoshttpaddress + "/" + sonosroom_local + "/" + sonosinstruction

            #clear the queue for every service request type except commands
            if servicetype != "command":
                print ("Clearing Sonos queue")
                r = requests.get(usersettings.sonoshttpaddress + "/" + sonosroom_local + "/clearqueue")

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
        print ("NFC reader could not read tag. This is usually because (a) the tag is encoded (b) you are trying to use a mifare classic card, which is not supported or (c) you have tried to add data to the card which is not in text format. Please check the data on the card using NFC Tools on Windows or Mac.")
        if usersettings.sendanonymoususagestatistics == "yes":
            r = requests.post(appsettings.usagestatsurl, data = {'time': time.time(), 'value1': appsettings.appversion, 'value2': hex(uuid.getnode()), 'value3': 'nfcreaderror'})

    return True

print("Setting up reader...")
reader = nfc.ContactlessFrontend('usb')
print(reader)

sonosroom_local = usersettings.sonosroom
print ("Sonos room set to " + sonosroom_local)

print("Ready!")
print("")

if usersettings.sendanonymoususagestatistics == "yes":
    r = requests.post(appsettings.usagestatsurl, data = {'time': time.time(), 'value1': appsettings.appversion, 'value2': hex(uuid.getnode()), 'value3': 'appstart'})

while True:
    reader.connect(rdwr={'on-connect': touched, 'beep-on-connect': False})
    time.sleep(0.1);
