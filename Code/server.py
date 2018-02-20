from socket import *
from pox.lib.packet import ethernet,ipv6
from pox.lib.addresses import IPAddr6,EthAddr 


'''
This is a Server  binding an interface and waiting
to receive a packet from the client and print it. (e.g icmp)
'''

#Open a Socket
s = socket(AF_PACKET, SOCK_RAW, htons(0x0003) )
#bind an interface
s.bind(('h2-eth0', 0))
#parse packet payload and print it
ether = ethernet()
data = s.recv(2048)
ether.parse(data)
ipv6 = ether.payload

print ipv6.payload
