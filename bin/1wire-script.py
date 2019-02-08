#!/usr/bin/python3
# encoding=utf-8

import os
import glob
import time
import ConfigParser
import socket
import logging
import sys
import paho.mqtt.client as mqtt
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

def main():
	# ---------------------------------------------
	# Globale Variablen
	# ---------------------------------------------
	separator = ";"

#Systemvariable auslesen
lbpconfig = os.environ['LBPCONFIG']
lbsconfig = os.environ['LBSCONFIG']
lbplog = os.environ['LBPLOG']
	
# ---------------------------------------------
# Durchsuche PlugIn config file
# ---------------------------------------------
pluginconfig = ConfigParser.ConfigParser()
pluginconfig.read(lbpconfig + "/1wire-onboard/1wireconfig.cfg")

enabled = pluginconfig.get('1wireconfig', 'ENABLED')
miniservername = pluginconfig.get('1wireconfig', 'MINISERVER')
virtualUDPPort = int(pluginconfig.get('1wireconfig', 'UDPPORT'))

# ---------------------------------------------
# Durchsuche Loxberry config file
# ---------------------------------------------
loxberryconfig = ConfigParser.ConfigParser()
loxberryconfig.read(lbsconfig + "/general.cfg")

miniserverIP = loxberryconfig.get(miniservername, 'IPADDRESS')

# ---------------------------------------------
# MQTT oder UDP Versand
# ---------------------------------------------
udpmqtt = int(pluginconfig.get('1wireconfig', 'UDPMQTT'))


# ---------------------------------------------
# Loglevelerkennung
# ---------------------------------------------
loglv = "WARNING" #standard loglevel
loglvint = int(pluginconfig.get('1wireconfig', 'LOGLV'))
if loglvint == 10:
	loglv = "INFO"
if loglvint == 20:
	loglv = "WARNING"
if loglvint == 30:
	loglv = "ERROR"
# ---------------------------------------------
# Logging
#----------------------------------------------
zeit = time.strftime("%d.%m.%Y %H:%M:%S")
logging.basicConfig(filename= lbplog + '/1wire-onboard/1wire-onboard.log', filemode='a', level=loglv) #logging starten und die einträge anfügen



# ---------------------------------------------
# Exit wenn PlugIn nicht eingeschalten ist
# ---------------------------------------------
if enabled != "1":
	logging.info("SCRIPT BEENDET DA ES NICHT AKTIVIERT IST")
	sys.exit(-1)

anzahl = 0
resultcode = 0
# ---------------------------------------------
# MQTT einstellungen
# ---------------------------------------------
mqttbroker = pluginconfig.get('1wireconfig', 'MQTTBROKER')
mqtttopik = pluginconfig.get('1wireconfig', 'MQTTTOPIK')
mqttuser = pluginconfig.get('1wireconfig', 'MQTTUSER')
mqttpassw = pluginconfig.get('1wireconfig', 'MQTTPASSW')

if udpmqtt == 0:
	def on_connect(client, userdata, flags, rc):
		global resultcode
		print("Connected with result code " + str(rc))
		if rc == 5:
			logging.warning(zeit + " Fehler bei der Authentifizierung des MQTT BROKER ( Password/USER ) ")	
			resultcode = 1
		if rc == 1 or rc == 2 or rc == 3 or rc == 4 or rc > 5:
			logging.warning(zeit + " Fehler bein MQTT CONNECT    RESULT-Code:" + str(rc))
			resultcode = 1
	client = mqtt.Client()
	client.on_connect = on_connect
	client.username_pw_set(mqttuser, mqttpassw)
	client.connect("localhost", 1883, 60)

	client.loop_start()


# ---------------------------------------------
# Neue Abfrage starten
# ---------------------------------------------
try:
	base_dir = '/sys/bus/w1/devices/'
	for dirs in os.listdir(base_dir): #die unterordner werden abgefragt
		if dirs.find("28") != -1:  #die sensoren der 28 er reihe herausfiltern (temperatursensoren)
			anzahl = anzahl + 1
			device_folder = base_dir + dirs
			device_file = device_folder + '/w1_slave'
			def read_temp_raw():
				f = open(device_file, 'r')
				lines = f.readlines()
				f.close()
				return lines
			def read_temp():
				lines = read_temp_raw()
				while lines[0].strip()[-3:] != 'YES':
					time.sleep(0.2)
					lines = read_temp_raw()
				equals_pos = lines[1].find('t=')
				if equals_pos != -1:
					temp_string = lines[1][equals_pos+2:]
					temp_c = float(temp_string) / 1000.0
					temp_f = temp_c * 9.0 / 5.0 + 32.0
					return temp_c#, temp_f
			temp = str(read_temp())
			ID = device_folder[20:] + "=" + temp
			if udpmqtt == 0:
				client.publish(mqtttopik, ID)
				if resultcode == 1:
					logging.error(zeit + " Script bei der MQTT Übermittlung abgebrochen")	
					sys.exit(-1)
			else:
				sock.sendto(ID, (miniserverIP,virtualUDPPort))
			time.sleep(1)
		else:	# alle anderen ordner überspringen  und weitermachen
			continue
	sens = str(anzahl)
	logging.info(zeit + ".     !!! INFO !!! " + sens +" Sensoren ausgelesen und Übertragung OK")
except Exception as e:
  logging.exception("\n" + "Exception occurred     " + zeit)