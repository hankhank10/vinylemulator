#set the address for node-sonos-http-api
#if this is running on the local Raspberry Pi then localhost will work
#if not, then set an IP address
#eg  sonoshttpaddress="http://192.168.4.102:5005"
sonoshttpaddress="http://localhost:5005"

#set the name of the Sonos room you want to play the music in
sonosroom="Garden"

#send anonymous usage statistics
sendanonymoususagestatistics="yes"

#if you are getting erros saying your nfc reader can not be found do the following:
#type lsusb into a terminal on your raspberry pi and enter
#in the output, find your nfc reader and copy the hex code next to it
#(for example, the ACR122U it is 072f:2200)
#then replace "usb" with "usb:072f:2200"
#(or whatever lsusb outputted for your nfc reader)
nfc_reader_path="usb"
