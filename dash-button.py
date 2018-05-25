#!/usr/bin/python

import socket
import struct
import binascii
import time
import json
import urllib2
import datetime

# Adapted from
# https://github.com/zippocage/dash_hack/blob/master/dash-listen.py
# http://www.aaronbell.com/how-to-hack-amazons-wifi-button/

stripOn = -1
# the number of seconds after a dash button is pressed that it will not trigger another event
# the reason is that dash buttons may try to send ARP onto the network during several seconds
# before giving up
trigger_timeout = 1

# Replace this MAC addresses and nickname with your own
macs = {
    'MAC' : 'nickname'
}

powerStripOn = "YOUR_URL_HERE"
powerStripDim = "YOUR_URL_HERE"
powerStripOff = "YOUR_URL_HERE"
lightStripOn = "YOUR_URL_HERE"
lightStripOff = "YOUR_URL_HERE"



# for recording the last time the event was triggered to avoid multiple events fired for one press on the dash button
trigger_time = {}

# Trigger a IFTTT URL. Body includes JSON with timestamp values.
def trigger_url(url):
    data = '{ "value1" : "' + time.strftime("%Y-%m-%d") + '", "value2" : "' + time.strftime("%H:%M") + '" }'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    return response

def is_within_secs(last_time, diff):
    return (datetime.datetime.now() - last_time).total_seconds() < (diff +1)

# check if event has triggered within the timeout already
def has_already_triggered(trigger):
    global trigger_time

    if trigger in trigger_time:
        if (is_within_secs(trigger_time[trigger], trigger_timeout)):
            return True

    trigger_time[trigger] = datetime.datetime.now()
    return False

def button_pressed():
    global stripOn
    stripOn = stripOn + 1
    #print stripOn

    if stripOn % 3 == 0:
        print "lights off"
        trigger_url(powerStripOff)
        trigger_url(lightStripOff)
    elif stripOn % 3 == 1:
        print "dim lights"
        trigger_url(powerStripDim)
        trigger_url(lightStripOff)
    else:
        print "lights on"
        trigger_url(powerStripOn)
        trigger_url(lightStripOn)


rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

while True:
    packet = rawSocket.recvfrom(2048)
    ethernet_header = packet[0][0:14]
    ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)
    # skip non-ARP packets
    ethertype = ethernet_detailed[2]
    if ethertype != '\x08\x06':
        continue
    # read out data
    arp_header = packet[0][14:42]
    arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)
    source_mac = binascii.hexlify(arp_detailed[5])
    source_ip = socket.inet_ntoa(arp_detailed[6])
    dest_ip = socket.inet_ntoa(arp_detailed[8])
    if source_mac in macs:
        print "ARP from " + macs[source_mac] + " with IP " + source_ip
        if macs[source_mac] == 'goldfish':
            if not has_already_triggered(macs[source_mac]):
                button_pressed()
    else:
        continue
        print "Unknown MAC " + source_mac + " from IP " + source_ip
