import socket
import struct
from uuid import getnode as get_mac
from random import randint

class DHCPDiscover:
	def buildPacket(self):
		packet = b''
		packet += b'\x01'	#OP
		packet += b'\x01'	#HTYPE
		packet += b'\x06'	#HLEN
		packet += b'\x00'	#HOPS
		packet += b'\x39\x03\xF3\x26'	#XID
		packet += b'\x00\x00'	#SECS
		packet += b'\x00\x00'	#FLAGS
		packet += b'\x00\x00\x00\x00'	#CIADDR(Client IP address)
		packet += b'\x00\x00\x00\x00'	#YIADDR(Your IP address)
		packet += b'\x00\x00\x00\x00'	#SIADDR(Server IP address)
		packet += b'\x00\x00\x00\x00' 	#GIADDR(Gateway IP address)
		packet += b'\x00\x05\x3C\x04'	#CHADDR(Client hardware address)
		packet += b'\x8D\x59\x00\x00'
		packet += b'\x00\x00\x00\x00'	
		packet += b'\x00\x00\x00\x00'
		packet += b'\x00'*192	
		packet += b'\x63\x82\x53\x63'	#Magic cookie
		packet += b'\x35\x01\x01'	#Option:DHCP Discover
		return packet

class DHCPRequest:
	def buildPacket(self):
		packet = b''
		packet += b'\x01'	#Op
		packet += b'\x01'	#HTYPE
		packet += b'\x06'	#HLEN
		packet += b'\x00'	#HOPS
		packet += b'\x39\x03\xF3\x26'	#XID
		packet += b'\x00\x00'	#SECS
		packet += b'\x00\x00'	#FLAGS
		packet += b'\x00\x00\x00\x00'	#CIADDR(Client IP address)
		packet += b'\x00\x00\x00\x00'	#YIADDR(Your IP address)
		packet += b'\xC0\xA8\x01\x01'	#SIADDR(Server IP address)
		packet += b'\x00\x00\x00\x00'	#GIADDR(Gateway IP address)
		packet += b'\x00\x05\x3C\x04'	#CHADDR(Client hardware address)
		packet += b'\x8D\x59\x00\x00'	
		packet += b'\x00\x00\x00\x00'
		packet += b'\x00\x00\x00\x00'
		packet += b'\x00'*192
		packet += b'\x63\x82\x53\x63'	#Magic cookie
		packet += b'\x35\x01\x03'	#Option:DHCP Request
		return packet

class DHCPOffer:
	def buildPacket(self):
		packet = b''
		packet += b'\x02'	#OP
		packet += b'\x01'	#HTYPE
		packet += b'\x06'	#HLEN
		packet += b'\x00'	#HOPS
		packet += b'\x39\x03\xF3\x26'	#XID
		packet += b'\x00\x00'	#SECS
		packet += b'\x00\x00'	#FLAGS
		packet += b'\x00\x00\x00\x00'	#CIADDR
		packet += b'\xC0\xA8\x01\x64'	#YIADDR
		packet += b'\xC0\xA8\x01\x01'	#SIADDR
		packet += b'\x00\x00\x00\x00'	#GIADDR
		packet += b'\x00\x05\x3C\x04'	#CHADDR
		packet += b'\x8D\x59\x00\x00'	
		packet += b'\x00\x00\x00\x00'
		packet += b'\x00\x00\x00\x00'
		packet += b'\x00'*192
		packet += b'\x63\x82\x53\x63'	#Magic cookie
		packet += b'\x35\x01\x02'	#Option:DHCP Offer
		return packet
	
class DHCPAck:
	def buildPacket(self):
		packet = b''
		packet += b'\x02'	#OP
		packet += b'\x01'	#HTYPE
		packet += b'\x05'	#HLEN
		packet += b'\x00'	#HOPS
		packet += b'\x39\x03\xF3\x26'	#XID
		packet += b'\x00\x00'	#SECS
		packet += b'\x00\x00'	#FLAGS
		packet += b'\x00\x00\x00\x00'	#CIADDR
		packet += b'\xC0\xA8\x01\x64'	#YIADDR
		packet += b'\xC0\xA8\x01\x01' 	#SIADDR
		packet += b'\x00\x00\x00\x00'	#GIADDR
		packet += b'\x00\x05\x3C\x04'	#CHADDR
		packet += b'\x8D\x59\x00\x00'	
		packet += b'\x00\x00\x00\x00'	
		packet += b'\x00\x00\x00\x00'
		packet += b'\x00'*192
		packet += b'\x63\x82\x53\x63'	#Magic cookie
		packet += b'\x35\x01\x05'	#Option:DHCP Offer
		return packet

if __name__ == '__main__':

		dhcps_C = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		dhcps_C.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
		print("Discover begin!\n")	
		try:
			dhcps_C.bind(('',68))
		except Exception as e:
			print('Port 68 in use.')
			dhcps_C.close()
			input('Press any key to quit.')
			exit()

		dhcps_S =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		dhcps_S.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
		
		try:
			dhcps_S.bind(('',67))
		except Exception as e:
			print('Port 67 in use.')
			dhcps_S.close()
			input('Press any key to quit.')
			exit()
#--------------------------------------------------------------------------------------
		discoverPacket=DHCPDiscover()
		dhcps_C.sendto(discoverPacket.buildPacket(),('<broadcast>',67))

		print('Send DISCOVER message!\n')
		dhcps_C.settimeout(5)

		try:
			while True:
					data = dhcps_C.recv(1024)
					if data == '':
							print('False\n')
							break
					else:
							break
		except socket.timeout as e:
			print()
#--------------------------------------------------------------------------------------
		dhcps_S.settimeout(5)
		try:
			while True:
					data = dhcps_S.recv(1024)
					if data == '':
							print('False\n')
							break
					else:
							break
		except socket.timeout as e:
			print()
		
		offerPacket = DHCPOffer()
		dhcps_S.sendto(offerPacket.buildPacket(),('<broadcast>',68))
#---------------------------------------------------------------------------------------
		requestPackage = DHCPRequest()
		dhcps_C.sendto(requestPackage.buildPacket(),('<broadcast>',67))

		print('Send DHCPREQUEST message\n')
		dhcps_C.close()
#---------------------------------------------------------------------------------------
		dhcps_S.settimeout(5)
		try:
			while True:
					data = dhcps_S.recv(1024)
					if data == '':
							 print('False\n')
							 break
					else:
							 break
		except socket.timeout as e:
		 	print()
		
		ACK = DHCPAck()
		dhcps_S.sendto(ACK.buildPacket(),('<broadcast>',68))
		dhcps_S.close()
#----------------------------------------------------------------------------------------
		
		print('Network Program Design hw1 finish!\n')

		input('Press any key to exit.')
		exit()




