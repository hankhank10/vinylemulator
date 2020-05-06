import time
import nfc
import requests
import sonossettings #this is a settings file stored in the directory
import uuid

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
            urltoget = sonossettings.sonoshttpaddress + "/" + sonossettings.sonosroom + "/" + sonosinstruction

            #clear the queue for every service request type except commands
            if servicetype <> "command":
                print ("Clearing Sonos queue")
                r = requests.get(sonossettings.sonoshttpaddress + "/" + sonossettings.sonosroom + "/clearqueue")

            #use the request function to get the URL built previously, triggering the sonos
            print ("Fetching URL via HTTP: "+ urltoget)
            r = requests.get(urltoget)
            print ("")

            #put together log data and send (if given permission)
            if sonossettings.sendanonymoususagestatistics == "yes":
                logdata = {
                'timestamp': time.time(),
                'uuid': hex(uuid.getnode()),
                'event': 'nfcread',
                'nfcpayload': receivedtext,
                'servicetype': servicetype,
                'urlfetched': urltoget
                }
                r = requests.post("https://en23qqgaymyen.x.pipedream.net/", data = logdata)

    else:
        print ("Tag Misread - Sorry")
        if sonossettings.sendanonymoususagestatistics == "yes":
            r = requests.post("https://en23qqgaymyen.x.pipedream.net/", data = {'timestamp': time.time(), 'uuid': hex(uuid.getnode()), 'event': 'nfcreaderror'})

    return True

print("Setting up reader...")
reader = nfc.ContactlessFrontend('usb')
print(reader)
print("Ready!")
print("")

if sonossettings.sendanonymoususagestatistics == "yes":
    r = requests.post("https://en23qqgaymyen.x.pipedream.net/", data = {'timestamp': time.time(), 'uuid': hex(uuid.getnode()), 'event': 'appstart'})

while True:
    reader.connect(rdwr={'on-connect': touched})
    time.sleep(0.1);
