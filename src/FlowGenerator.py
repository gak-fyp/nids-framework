#!/usr/bin/python
# -*- coding: utf-8 -*-
import pcap
import sys
import socket
import signal 
from BasicPacketInfo import BasicPacketInfo
from BasicFlow import BasicFlow
import time
from struct import *


class FlowGenerator:
    


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
                self.__currentFlows[packetInfo.getFlowId()].dumpFlowBasedFeatures(",",self.__fileObject)
                del self.__currentFlows[packetInfo.getFlowId()]
                self.__currentFlows[packetInfo.getFlowId()] =  BasicFlow(self.__bidirectional,packetInfo, flow.getSrc(),flow.getDst(),flow.getSrcPort(), flow.getDstPort())
            elif packetInfo.hasFlagFIN():
                flow.addPacket(packetInfo)
                self.__currentFlows[packetInfo.getFlowId()].dumpFlowBasedFeatures(",",self.__fileObject)
                del self.__currentFlows[packetInfo.getFlowId()]
            else:

                flow.updateActiveIdleTime(currentTimestamp, self.__activityTimeout)
                flow.addPacket(packetInfo)
                self.__currentFlows[packetInfo.getFlowId()] = flow
        else:

            self.__flowCount += 1
            self.__currentFlows[packetInfo.getFlowId()] = BasicFlow(self.__bidirectional, packetInfo)

    def flush_flows(self):
        print("A total of {} flows generated".format(self.__flowCount))
        for (key, val) in self.__currentFlows.items():           
            val.dumpFlowBasedFeatures(',', self.__fileObject)

    def flow_timeout(self):
        print('Checking flowtimeout.')
        ts = time.time()
        ts = ts*1000000
        target_keys = []
        for (key, val) in self.__currentFlows.items():           
            if ts - val.getFlowStartTime() > self.__flowTimeout:
                target_keys.append(key)
        for key in target_keys:
            self.__currentFlows[key].dumpFlowBasedFeatures(",",self.__fileObject)
            del self.__currentFlows[key]
