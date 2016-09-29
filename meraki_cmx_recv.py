#!/usr/bin/env python
from bottle import get, route, run, request
import urllib
import json
import os

VALIDATOR = 'c339128dc0fc4584b8b970acdb7a4968911d8dc8'
SECRET = "test123"

@route('/events')
def events():
	return VALIDATOR

@route('/events', method='POST')
def do_events():
	f = open("/var/www/meraki_cmx/meraki_post.csv",'a')
	
	secret = request.json["secret"]
	
	if (secret != SECRET):
		return "FAILED"
	
	event = request.json["data"]
	
	if event.get("apMac", "None") is not None:
		apMac = event.get("apMac", "None")
	
	for item in iter(event["apTags"]):
		if item.startswith('CMX-'):
			siteName = item.replace("CMX-","",1)
			break

	for item in iter(event["observations"]):
		csvString = ""
		clientMac = item.get("clientMac", "None")
		if clientMac is None:
			clientMac = ""
		ipv4 = item.get("ipv4", "None")
		if ipv4 is None:
			ipv4 = ""
		else:
			ipv4 = ipv4.strip('/')
		ipv6 = item.get("ipv6", "None")
		if ipv6 is None:
			ipv6 = ""
		else:
			ipv6 = ipv6.strip('/')
		seenTime = item.get("seenTime", "None")
		if seenTime is None:
			seenTime = ""
		seenEpoch = str(item.get("seenEpoch", "None"))
		if seenEpoch is None:
			seenEpoch = ""
		ssid = item.get("ssid", "None")
		if ssid is None:
			ssid = ""
		rssi = str(item.get("rssi", "None"))
		if rssi is None:
			rssi = ""
                manufacturer = item.get("manufacturer", "None")
		if manufacturer is None:
			manufacturer = ""
		operatingSystem = item.get("os", "None")
		if operatingSystem is None:
			operatingSystem = ""
		csvString = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (siteName,apMac,clientMac,ipv4,ipv6,seenTime,seenEpoch,ssid,rssi,manufacturer,operatingSystem)
		f.write(csvString + "\n")

	f.close()
	return 'OK'
		
if __name__ == "__main__":
    run(host="localhost", port=8433)
else:
    application = default_app()

