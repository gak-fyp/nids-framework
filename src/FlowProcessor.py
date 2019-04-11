#!/usr/bin/python
# -*- coding: utf-8 -*-
import pcap
import sys
import socket
from BasicPacketInfo import BasicPacketInfo
from struct import *

class FlowProcessor:
    def getIpv4Info(self,ts, pkt):
        packetInfo = None

        # extracts ip header only
        ip_hdr = pkt[0:20]
        iph = unpack('!BBHHHBBH4s4s', ip_hdr)
        version_ihl = iph[0]
        version = version_ihl >> 4  # converts version into string convertible format
    
        ihl = version_ihl & 0xF  # version gives us ipl
        pktHeaderLength = ihl * 4  # ipl is in that weird form so we convert it into bytes

        pktLength = iph[2]  # ihl + datlen
        protocol = iph[6]

        if protocol == 6:
            tcp_hdr = pkt[pktHeaderLength:pktHeaderLength + 20]
            tcph = unpack('!HHLLBBHHH', tcp_hdr)
                 # calculates TCP segment and header length
            tcp_offset = tcph[4] >> 4
            segmentHeaderLength = tcp_offset * 4
            segmentLength = pktLength - (pktHeaderLength + segmentHeaderLength)
                # set src,dst,srcPort,dstPort,protocol,timestamp

            packetInfo = BasicPacketInfo(
                    iph[8],
                    iph[9],
                    tcph[0],
                    tcph[1],
                    protocol,
                    ts,
                    1,
                    )
            packetInfo.setTCPWindow(tcph[6])
            packetInfo.setFlags(tcph[5])
            packetInfo.setPayloadBytes(segmentLength)
            packetInfo.setHeaderBytes(segmentHeaderLength)

        elif protocol == 17:
            udp_hdr = pkt[pktHeaderLength:pktHeaderLength + 8]
            udph = unpack('!HHHH', udp_hdr)
            packetInfo = BasicPacketInfo(iph[8],iph[9],udph[0],udph[1],protocol,ts,1)
            packetInfo.setPayloadBytes(udph[2]-8)
        #print("Size:{}".format(udph[2]-8))
            packetInfo.setHeaderBytes(8)
        return packetInfo
    

    def getIpv6Info(self,ts, pkt):
        packetInfo = None
        pktHeaderLength = 40
        ip_hdr = pkt[0:40]

        iph = unpack('!BHsHBB16s16s', ip_hdr)
    # converts version into string convertible format

        payloadLength = iph[3]  # ihl + datlen
        protocol = iph[4]
        if protocol == 6:
            tcp_hdr = pkt[pktHeaderLength:pktHeaderLength + 20]
            tcph = unpack('!HHLLBBHHH', tcp_hdr)

            tcp_offset = tcph[4] >> 4
            segmentHeaderLength = tcp_offset * 4
            segmentLength = payloadLength - segmentHeaderLength
            packetInfo = BasicPacketInfo(
                    iph[6],
                    iph[7],
                    tcph[0],
                    tcph[1],
                    protocol,
                    ts,
                    1,
                    )

            packetInfo.setTCPWindow(tcph[6])
            packetInfo.setFlags(tcph[5])
            packetInfo.setPayloadBytes(segmentLength)
            packetInfo.setHeaderBytes(segmentHeaderLength)
            

        elif protocol == 17:
            udp_hdr = pkt[pktHeaderLength:pktHeaderLength + 8]
            udph = unpack('!HHHH', udp_hdr)
            packetInfo = BasicPacketInfo(iph[6],iph[7],udph[0],udph[1],protocol,ts,1)
            packetInfo.setPayloadBytes(udph[2]-8)
            packetInfo.setHeaderBytes(8)
        return packetInfo


'''print('TS:{}'.format(ts))
        print ('Payload:{}'.format(iph[3]))
        print ('NH:{}'.format(iph[4]))
        print ('Hop:{}'.format(iph[5]))
        print ('SRC:{}'.format(socket.inet_ntop(10,iph[6])))
        print ('DEST:{}'.format(socket.inet_ntop(10,iph[7])))
        print ('Length of SRC:{}'.format(len(iph[6])))
        print ('SRCPORT:{}'.format(udph[0]))
        print ('DSTPORT:{}'.format(udph[1]))
        print()'''    


            