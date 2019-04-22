#!/usr/bin/python
import pcap
import sys
import socket
import os
import signal
import pcapy 
from Sniffer import Sniffer
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




	def capture_file(self):
		flow_log = {}
		count = 0
		#flowGen = new FlowGenerator(true,120000000L, 5000000L);
		flowGen = FlowGenerator(True,self.__flow_timeout, self.__activity_timeout, self.__output_file_object)
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
			flowGen.addPacket(packetInfo)
	
		print ('Printing our list!')
		flowGen.listBasic()
		print('Total packets:' + str(count))

	def capture_live(self):
		flow_log = {}
		count = 0
		#flowGen = new FlowGenerator(true,120000000L, 5000000L);
		flowGen = FlowGenerator(True,self.__flow_timeout, self.__activity_timeout, self.__output_file_object)
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
	
			flowGen.addPacket(packetInfo)
			print("Count:{}".format(count))
			if count == 100:
				flowGen.listBasic()
				break
	
		print ('Printing our list!')
		flowGen.listBasic()
		print('Total packets:' + str(count))


def main():
	arg_err_main = 'Invalid argument\nLive Capture: python FlowMeter.py -l <interface> <output-r>\n File Capture:python FlowMeter.py -p <input-dir> <output-dir>\n'
	arg_err_live = 'Invalid argument for live capture\nLive Capture: python FlowMeter.py -l <interface> <output-dir>\n'
	arg_err_offline = 'Invalid argument for file capture\nFile Capture:python FlowMeter.py -p <input-dir> <output-dir>\n'
	print('Input length:')
	print(len(sys.argv))
	print(sys.argv[0])
	if(len(sys.argv)) <= 1:
		print(arg_err_main)
	else:
		if sys.argv[1] == '-l':
			print('Live capture mode!')
			if len(sys.argv) != 4:
				print(arg_err_live)
			else: 
				if 1 != 1:
					print('directory does not exist')
				else:
					try:

						os.makedirs(sys.argv[3])
						print('starting online capture:')
						print('[{}] interface to be processed:'.format(sys.argv[2]))
						outputfile = os.path.join(sys.argv[3], "live.csv")
						try:
							output_file_object= open(outputfile,"w")
							flowmeter = FlowMeter(sys.argv[2],output_file_object, 120000000,5000000 )
							flowmeter.capture_live()
							output_file_object.close()
						except IOError:
							print('Could not open file:[{}]'.format(outputfile));

				

					except FileExistsError:
						print('Error: output directory [{}] already exists.'.format(sys.argv[3]))
						pass

		elif sys.argv[1] == '-p':
			if len(sys.argv) != 4:
				print(arg_err_offline)
			else: 
				if not os.path.exists(sys.argv[2]):
					print('directory does not exist')
				else:
					try:

						os.makedirs(sys.argv[3])
						files = []
						#makes list of all files in input directory! 
						for r, d, f in os.walk(sys.argv[2]):
							for file in f:
								if '.pcap' in file:
									files.append(file)

						print('starting offline capture:')
						print('[{}] pcap files to be processed:'.format(len(files)))
						for file in files:
							print(file)

						#loop to iterate all input files inside the input directory!
						for file in files:
							inputfile = os.path.join(sys.argv[2], file)
							csv_file = os.path.splitext(file)[0] + ".csv"
							outputfile = os.path.join(sys.argv[3], csv_file)
							try:
								output_file_object= open(outputfile,"w")
								flowmeter = FlowMeter(inputfile,output_file_object, 120000000,5000000 )
								flowmeter.capture_file()
								output_file_object.close()
							except IOError:
								print('Could not open file:[{}]'.format(outputfile));

				

					except FileExistsError:
						print('Error: output directory [{}] already exists.'.format(sys.argv[3]))
						pass



		else:
			print(arg_err_main)






	

main()
#flowmeter = FlowMeter()
#flowmeter.capture_file()