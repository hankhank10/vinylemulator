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
                print ("Spotify URI detected")
                sonosinstruction = "spotify/now/" + record.text

            if receivedtext.startswith ('tunein'):
                print ("Tunein URI detected")
                sonosinstruction = record.text

            urltoget = sonossettings.sonoshttpaddress + "/" + sonossettings.sonosroom + "/" + sonosinstruction
            print ("Fetching via HTTP: "+ urltoget)


            #clear the queue (you can delete this next line if you prefer not to have a clear queue)
            r = requests.get(sonossettings.sonoshttpaddress + "/" + sonossettings.sonosroom + "/clearqueue")

            #request the URL built previously
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
#    print("Tag released")
#    print ("---")
#    print ("")
    sleep(0.1);
