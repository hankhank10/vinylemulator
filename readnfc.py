import time
import nfc
import requests
import uuid
import appsettings #you shouldnt need to edit this file
import usersettings #this is the file you might need to edit

# this function gets called when a NFC tag is detected
def touched(tag):

    if tag.ndef:
        for record in tag.ndef.records:
            receivedtext = record.text

            print("Read from NFC tag: "+ receivedtext)

            if receivedtext.startswith ('spotify'):
                servicetype = "spotify"
                sonosinstruction = "spotify/now/" + record.text

            if receivedtext.startswith ('tunein'):
                servicetype = "tunein"
                sonosinstruction = record.text

            if receivedtext.startswith ('command'):
                servicetype = "command"
                sonosinstruction = record.text[8:]

            print ("Detected " + servicetype + " service request")

            #build the URL we want to request
            urltoget =usersettings.sonoshttpaddress + "/" + usersettings.sonosroom + "/" + sonosinstruction

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
        print ("Tag Misread - Sorry")
        if usersettings.sendanonymoususagestatistics == "yes":
            r = requests.post(appsettings.usagestatsurl, data = {'timestamp': time.time(), 'appversion': appsettings.appversion, 'uuid': hex(uuid.getnode()), 'event': 'nfcreaderror'})

    return True

print("Setting up reader...")
reader = nfc.ContactlessFrontend('usb')
print(reader)
print("Ready!")
print("")

if usersettings.sendanonymoususagestatistics == "yes":
    r = requests.post(appsettings.usagestatsurl, data = {'timestamp': time.time(), 'appversion': appsettings.appversion, 'uuid': hex(uuid.getnode()), 'event': 'appstart'})

while True:
    reader.connect(rdwr={'on-connect': touched})
    time.sleep(0.1);
