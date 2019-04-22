#!/usr/bin/python
import pcap
import sys
import socket
import os
import signal
import pcapy 
from BasicPacketInfo import BasicPacketInfo
from BasicFlow import BasicFlow
from FlowGenerator import FlowGenerator
from FlowProcessor import FlowProcessor

from struct import *


class FlowMeter():

	def __init__(self, input_file,output_file_object,flowTimeout, activityTimeout):
		self.__input_file= input_file
		self.__output_file_object = output_file_object
		self.__flow_timeout = flowTimeout
		self.__activity_timeout = activityTimeout
		self.__flowGen = None


	def flush_flows(self):
		self.__flowGen.flush_flows()

	def flow_timeout(self):
		self.__flowGen.flow_timeout()



	def capture_file(self):
		flow_log = {}
		count = 0
		#flowGen = new FlowGenerator(true,120000000L, 5000000L);
		self.__flowGen = FlowGenerator(True,self.__flow_timeout, self.__activity_timeout, self.__output_file_object)
		flowProc = FlowProcessor()
		packetInfo = None
		header = 0 
		sniffer = pcap.pcap(name=self.__input_file, promisc=True, immediate=True,timeout_ms=12000000000)

	# initialises address structure helps in printing
		addr = lambda pkt, offset: ':'.join(str(ord(pkt[i])) for i in
                                    range(offset, offset + 4))
		print ('Sniffer built successfully..')

	# loop that process packet as soon as they are caught by sniffer
		for (ts, pkt) in sniffer:
			ts = ts * 1000000
			count = count + 1
			pkt = pkt[sniffer.dloff:]  # remove link layer data
		
			ip_hdr = pkt[0:20]
			iph = unpack('!BBHHHBBH4s4s', ip_hdr)
		
			version_ihl = iph[0]
			version = version_ihl >> 4
		
			packetInfo = None

			if version == 4:
				packetInfo = flowProc.getIpv4Info(ts, pkt)

			elif version == 6:
				packetInfo = flowProc.getIpv6Info(ts, pkt)
			self.__flowGen.addPacket(packetInfo)
	
		self.flush_flows()
		print('Total packets:' + str(count))

	def capture_live(self):
		flow_log = {}
		count = 0
		#flowGen = new FlowGenerator(true,120000000L, 5000000L);
		self.__flowGen = FlowGenerator(True,self.__flow_timeout, self.__activity_timeout, self.__output_file_object)
		flowProc = FlowProcessor()
		packetInfo = None
		header = 0 
		sniffer = pcapy.open_live(self.__input_file, 65536,1,0)
		

	# initialises address structure helps in printing
		addr = lambda pkt, offset: ':'.join(str(ord(pkt[i])) for i in
                                    range(offset, offset + 4))
		print ('Sniffer built successfully..')

	# loop that process packet as soon as they are caught by sniffer
		while True:
			(header, payload) = sniffer.next()
			(seconds, micros) = header.getts()
			pkt = payload[14:]
			ts = seconds
			print("Time:{}".format(ts))
			ts = ts * 1000000

			count = count + 1
			#pkt = pkt[sniffer.dloff:]  # remove link layer data
			
			#pkt = pkt.get_raw_packet()
			ip_hdr = pkt[0:20]
			iph = unpack('!BBHHHBBH4s4s', ip_hdr)
		
			version_ihl = iph[0]
			version = version_ihl >> 4
		
			packetInfo = None

			if version == 4:
				packetInfo = flowProc.getIpv4Info(ts, pkt)
			elif version == 6:
				packetInfo = flowProc.getIpv6Info(ts, pkt)
			else:
				weirdcount = weirdcount + 1
	
			self.__flowGen.addPacket(packetInfo)
			print("Count:{}".format(count))
			if count == 100:
				self.flush_flows()
				break
	
	
		self.flush_flows()
		print('Total packets:' + str(count))


