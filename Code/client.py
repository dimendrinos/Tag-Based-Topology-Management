from socket import *
from pox.lib.packet import ethernet,ipv6
from pox.lib.addresses import IPAddr6,EthAddr
# Developed by: Mendrinos Dimitrios Fotiou Nikos

'''

ethernet_packet = [0x52, 0x54, 0x00, 0x12, 0x35, 0x02, 0xfe, 0xed, 0xfa,
                         0xce, 0xbe, 0xef, 0x08, 0x00]

# src=10.0.2.15, dst=195.88.54.16 (vg.no), checksum, etc.
ipv4_header = [0x45, 0x00, 0x00, 0x54, 0x05, 0x9f, 0x40, 0x00, 0x40, 0x01,
             0x2f, 0x93, 0x0a, 0x00, 0x02, 0x0f, 0xc3, 0x58, 0x36, 0x10]
             

payload_packet = b"".join(map(chr, ipv4_header))
ethernet_packet_b = b"".join(map(chr, ethernet_packet))
'''

'''
This is a Client. Can be an IoT Device and use CoAP communication. 
We just send an IP packet without actually knowing IPv6 with 
just a tag in the IP packet payload.

'''

#Create an IP packet
ipv6_packet = ipv6()
ipv6_packet.srcip = IPAddr6("::0")

#Random IP destination address
ipv6_packet.dstip = IPAddr6("::7")
ipv6_packet.next_header_type = 0xFD

# Set a tag in IP payload. e.g color = red
ipv6_packet.payload = "[color='red']"
ether = ethernet()
ether.type = 0x86DD

# Because we don't know the destination mac address we set :00 as mac
ether.dst = EthAddr(b"\x00\x00\x00\x00\x00\x00")
ether.src = EthAddr(b"\x08\x00\x27\xc8\x18\xa5")
ether.payload = ipv6_packet

# Open a socket and send the packet through it
s = socket(AF_PACKET, SOCK_RAW)
s.bind(('h1-eth0', 0))
s.send(ether.pack())
