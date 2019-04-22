import pcap
import sys
import socket
import os
import signal
import pcapy 
import time
from Sniffer import Sniffer
from BasicPacketInfo import BasicPacketInfo
from BasicFlow import BasicFlow
from FlowGenerator import FlowGenerator
from FlowProcessor import FlowProcessor
from FlowMeter import FlowMeter

from struct import *


flowmeter = None
output_file_object = None
original_sigint = None
def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    global original_sigint
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)


def set_signals():
    global original_sigint
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGALRM, exit_gracefully)
    signal.signal(signal.SIGHUP, signal.SIG_IGN)




def alarm_handler(sig, frame):
        print('You pressed Ctrl+C!')
        if flowmeter == None:
        	print('No flow created!')
        else:
        	print('got flow')
        sys.exit(0)
def main():
	flowmeter = None
	arg_err_main = 'Invalid argument\nLive Capture: python FlowMeter.py -l <interface> <output-r>\n File Capture:python FlowMeter.py -p <input-dir> <output-dir>\n'
	arg_err_live = 'Invalid argument for live capture\nLive Capture: python FlowMeter.py -l <interface> <output-dir>\n'
	arg_err_offline = 'Invalid argument for file capture\nFile Capture:python FlowMeter.py -p <input-dir> <output-dir>\n'
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
								
								
							except IOError:
								print('Could not open file:[{}]'.format(outputfile));

				

					except FileExistsError:
						print('Error: output directory [{}] already exists.'.format(sys.argv[3]))
						pass



		else:
			print(arg_err_main)

	print('calling flowfeature')

	if flowmeter != None:
		flowmeter.flow_timeout()
		flowmeter.flush_flows()
		output_file_object.close()

if __name__ == '__main__':
    # store the original SIGINT handler
    set_signals()
    main()



