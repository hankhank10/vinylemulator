import requests

print ("")
print ("Do you want to register to receive email updates on new versions?")
print ("(Y)es or (N)o")
want_to_register = raw_input("> ")

if want_to_register.lower() == "y":
    print ("")
    print ("Please type your email address below:")
    email = raw_input("> ")

    r = requests.get("https://version.hankapi.com/vinylemulator-register?email="+email)
    print ("")
    print (r.text)