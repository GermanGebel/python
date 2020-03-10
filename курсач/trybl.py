import bluetooth
import os
target_name = "SmartHome"
addr = "ab:68:32:57:34:02"
target_address = addr
port = 1024
nearby_devices = bluetooth.discover_devices()
for address in nearby_devices:
    if target_name == bluetooth.lookup_name(address):
        target_address = address
        break
if target_address is not None:
    print("found target bluetooth device with address", target_address)
else:
    print("could not find target bluetooth device nearby")

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((addr, port))
#
# sock.connect((addr, port))
#
# sock.send("0000")
#
# sock.close()
