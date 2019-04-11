import socket
import struct
import textwrap

class Sniffer():
	def __init__(self, timelimit):
		self.__timelimit = timelimit

	def ethernet_frame(self,data):
		#get 14 starting bytes and unpack it
		dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[0:14])
		return self.get_mac_addr(dest_mac), self.get_mac_addr(src_mac), socket.htons(proto), data[14:]
	
	def get_mac_addr(self,bytes_addr):
		#takes one bytes and break into two 
		bytes_str = map('{:02x}'.format, bytes_addr)
		#joins the array into string seperated by :
		return ':'.join(bytes_str).upper()

	def ipv4_packet(self, data):
		#version and header length are combined in IP packets
		version_header_length = data[0]
		version = version_header_length >> 4

		#compares two bytes and get result when both bytes are one
		#header length is important as where header ends data begins!
		header_length = (version_header_length & 15)

		#IPv4 headers are always 20 bytes 
		ttl, proto, src,dest = struct.unpack('! 8x B B 2x 4s 4s',data[:20])
		#ipv4 can have options so we use header length!
		return version, header_length, ttl, proto, self.get_ipv4(src), self.get_ipv4(dest), data[header_length:]

	def get_ipv4(self,addr):	
		return '.'.join(map(str,addr))


	def icmp_packet(self, data):
		icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
		return icmp_type, code, checksum, data[4:]

	def tcp_segmet(self,data):
		src_port, dest_port, seq, ack, offset_reserved_flag = struct.unpack('! H H L L H', data[:14])
		offset = (offset_reserved_flag >> 12)*4

		flag_urg = (offset_reserved_flag & 32) >>  5
		flag_ack = (offset_reserved_flag & 16) >>  5
		flag_psh = (offset_reserved_flag & 8)  >>  5
		flag_rst = (offset_reserved_flag & 4)  >>  5
		flag_syn = (offset_reserved_flag & 2)  >>  5
		flag_fin = (offset_reserved_flag & 1)  >>  5

		return src_port, dest_port, seq, ack, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]

	def udp_segment(self,data):
		src_port,dest_port, size = struct.unpack('! H H 2x H', data[:8])
		return src_port,dest_port, size, data[8:]



	def main(self):

		conn = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.ntohs(3))

		while True:
			raw_data, addr = conn.recvfrom(65536)
			#data is ethernet payload
			dest_mac, src_mac, eth_proto, eth_data = self.ethernet_frame(raw_data)
			print('\nEthernet Frame:')
			print('\t Destination:{}, Source:{}, Protocol:{}'.format(dest_mac, src_mac, eth_proto))
			
			if eth_proto == 8:
				version, header_length, ttl, ip_proto, src_ip, dest_ip, ip_data = self.ipv4_packet(eth_data)
				print('\t ipv4 packet:')
				print('\t\t Source:{}, Destination:{}, Network Protocol:{}'.format(src_ip, dest_ip,ip_proto))

				if ip_proto == 1: 
					icmp_type, code, checksum, data = self.icmp_packet(ip_data)







