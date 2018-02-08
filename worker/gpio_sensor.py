from tools.sensor import Sensor
import pigpio
from tools.pigpio433 import rx
import logging
import time
import requests
import threading


class GPIOSensor(Sensor):
	
	def __init__(self, id, params, worker):
		super(GPIOSensor, self).__init__(id, params, worker)
		self.active = False
		try:
			self.gpio = int(params["gpio"])
			self.bouncetime = int(self.params['bouncetime'])
		except ValueError as ve: # if one configuration parameter can't be parsed as int
			logging.error("GPIOSensor: Wasn't able to initialize the sensor, please check your configuration: %s" % ve)
			self.corrupted = True
			return
		except KeyError as ke: # if config parameters are missing in the file
			logging.error("GPIOSensor: Wasn't able to initialize the sensor, it seems there is a config parameter missing: %s" % ke)
			self.corrupted = True
			return
		logging.debug("GPIOSensor: Sensor initialized")

	def activate(self):
		if not self.corrupted:
			self.stop_thread = False
			self.checker_thread = threading.Thread(name="thread-checker-%s" % self.gpio,
												   target=self.check_listendata)
			self.checker_thread.start()
		else:
			logging.error("AlkAlarm Sensor couldn't be activated")

	def deactivate(self):
		if not self.corrupted:
			self.stop_thread = True
		else:
			logging.error("AlkAlarm Sensor couldn't be deactivated") # maybe make this more clear

	def request_http_api_activate(self):
		url = "http://192.168.10.70:8080/deactivate"
		payload = "{\"id\":1}"
		headers = {
			'Content-Type': "application/json",
			'Authorization': "Digest username=\"admin\", realm=\"secpi\", nonce=\"1518069302:aad6b2b0feb33af26777203701f259cd\", uri=\"/deactivate\", algorithm=\"MD5\", qop=auth, nc=00000001, cnonce=\"0a42swe23\", response=\"3243a8518adb9a15e1b8cd9106e89087\", opaque=\"kkkkkkkkk\"",
			'Cache-Control': "no-cache",
			'Postman-Token': "d4002952-c22e-4554-ba4c-e51eaa753030"
		}
		response = requests.request("POST", url, data=payload, headers=headers)


	def handler_events(self,code, bits, gap, t0, t1):
		if code == "3462412":
			self.request_http_api_activate()
		else:
			self.alarm("Sensor detected something: %s" % self.gpio)

	def check_listendata(self):
		pi = pigpio.pi() # Connect to local Pi.
		while True:
			if self.stop_thread: #exit thread when flag is set
				return
			bus = rx(pi, gpio=27, callback=self.handler_events)
			time.sleep(60)
			continue
		pi.stop()