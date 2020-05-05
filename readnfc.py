from time import sleep
import nfc
import requests
import sonossettings #this is a settings file stored in the directory

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

    else:
        print ("Tag Misread - Sorry")

    return True

print("Setting up reader...")
reader = nfc.ContactlessFrontend('usb')
print(reader)
print("Ready!")
print("")

while True:
    reader.connect(rdwr={'on-connect': touched})
    sleep(0.1);
