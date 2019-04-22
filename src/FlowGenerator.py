#!/usr/bin/python
# -*- coding: utf-8 -*-
import pcap
import sys
import socket
import signal 
from BasicPacketInfo import BasicPacketInfo
from BasicFlow import BasicFlow
from struct import *


# All that is left is for us to figure out how can finished flows be stored and or printed

class FlowGenerator:
    def sig_handler(self,sig,frame):
        print('HandlerCalled!')
        sys.exit(0)


    def __init__(
        self,
        bidirectional,
        flowTimeout,
        activityTimeout,
        output_file_object
        ):
        self.__bidirectional = bidirectional
        self.__flowTimeout = flowTimeout
        self.__activityTimeout = activityTimeout
        self.init()
        self.__header = 0
        self.__fileObject = output_file_object
        signal.signal(signal.SIGINT, self.sig_handler)



    def init(self):
        self.__flowCount = 0 
        self.__currentFlows = {}
        self.__finishedFlowCount = 0
        self.__IpAddresses = {}

    def addPacket(self, packetInfo):

        if packetInfo == None:
            return
        if self.__header == 0:
            self.__header = 1
            test = BasicFlow(self.__bidirectional,packetInfo)
            test.dumpFileHeadings(',',self.__fileObject)


        currentTimestamp = packetInfo.getTimestamp()

        if packetInfo.getFlowId() in self.__currentFlows:
            #print('Flow exists:{}'.format(packetInfo.getFlowId()))
            flow = self.__currentFlows[packetInfo.getFlowId()]
            #print ('Flow: {} exists'.format(packetInfo.getFlowId()))
            if currentTimestamp - flow.getFlowStartTime() > self.__flowTimeout:

                # flow count
                    # flow listener
                        # extra shit

                print ('Flow time out')
                self.__currentFlows[packetInfo.getFlowId()].dumpFlowBasedFeatures(",",self.__fileObject)
                del self.__currentFlows[packetInfo.getFlowId()]
                self.__currentFlows[packetInfo.getFlowId()] =  BasicFlow(self.__bidirectional,packetInfo, flow.getSrc(),flow.getDst(),flow.getSrcPort(), flow.getDstPort())
            elif packetInfo.hasFlagFIN():

                # 1
                # 2

                #print ('Flow finished')

                flow.addPacket(packetInfo)
                self.__currentFlows[packetInfo.getFlowId()].dumpFlowBasedFeatures(",",self.__fileObject)
                del self.__currentFlows[packetInfo.getFlowId()]
            else:

               
                print ('flow updated')

                
                flow.updateActiveIdleTime(currentTimestamp, self.__activityTimeout)
                flow.addPacket(packetInfo)
                self.__currentFlows[packetInfo.getFlowId()] = flow
        else:

            print ('Creating Flow:{}'.format(packetInfo.getFlowId()))
            self.__flowCount += 1
            self.__currentFlows[packetInfo.getFlowId()] = BasicFlow(self.__bidirectional, packetInfo)

    def listBasic(self):
        #print ('final list')
        print("A total of {}".format(self.__flowCount))
        
        for (key, val) in self.__currentFlows.items():           
            val.dumpFlowBasedFeatures(',', self.__fileObject)
            #if count == 5:
            #    break 

#printer remaining!!

