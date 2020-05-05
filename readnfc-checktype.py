from time import sleep
import nfc
import requests
import sonossettings #this is a settings file stored in the directory

# this function gets called when a NFC tag is detected
def touched(tag):

    if tag.ndef:
        for record in tag.ndef.records:
            print("Read from NFC tag: "+ record.text)

            if record.text.startswith ('spotify')
                print ("Spotify URI")

            if record.text.startswith ('tunein')
                print ("Tunein URI")

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
