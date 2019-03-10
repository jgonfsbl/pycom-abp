""" LoRaWAN ABP Node """

from network import LoRa
import socket
import binascii
import struct
import time

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# Create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('26011AC2'))[0]
nwk_swkey = binascii.unhexlify('2188BC4ED0335345334637664A01C0AD3')
app_swkey = binascii.unhexlify('8AC7B9A90E78678767692C10B6D825418')

# Remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# Set the 3 default LoRa channels to the same frequency for Single Channel gateways
lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=868100000, dr_min=0, dr_max=5)

# Join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# Make the socket non-blocking
s.setblocking(False)

""" Your own code can be written below! """

while True:
    for i in range(254):
        print("Sending PKT # %s" % bytes([i]))
        s.send(b'PKT #' + bytes([i]))
        time.sleep(10)
        rx = s.recv(256)
        if rx:
            print("Received data: %s" % rx)
            print('Received: {}, on port: {}'.format(rx, port))
            time.sleep(10)
    i=0
