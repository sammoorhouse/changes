import paho.mqtt.client as mqtt
import sys
from time import sleep

me = int(sys.argv[1])
all = int(sys.argv[2])
bells = {}

def on_message(client, userdata, message):
	if me == 1:
		print message.topic + " " + message.payload
	if message.topic == "changes/init" and me == 1:
		print "new bell: " + message.payload
		#add new joiner to list && check size against all
		bell = int(message.payload)
		bells[bell] = ""
		if len(bells) == all:
			client.publish("changes/rounds", me)
	elif message.topic == "changes/rounds":
		msg = int(message.payload)
		if msg == (me - 1) or (msg == all and me == 1):
			client.publish("changes/rounds", me)
			sleep(0.5)

def on_connect(client, userdata, flags, code):
	client.subscribe("changes/rounds")
	client.subscribe("changes/init")
	client.publish("changes/init", me)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)


client.loop_forever()
