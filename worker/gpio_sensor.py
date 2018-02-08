from tools.sensor import Sensor
import pigpio
from tools.pigpio433 import rx
import logging
import time
import requests
from requests.auth import HTTPDigestAuth
import json
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

	def request_api_to_manage(self,alarm,value):
		url = 'http://localhost:8080/'+value
		payload = {'id': 1}
		if alarm == "parcial":
			payload = {'id': 2}
		headers = {'content-type': 'application/json'}
		response = requests.post(url, auth=HTTPDigestAuth('admin', 'admin2803'),data=json.dumps(payload), headers=headers)


	def handler_events(self,code, bits, gap, t0, t1):
		if code == 3462412:  # codigos abrir mando (cambiar por lectura a bd)
			self.request_api_to_manage("completa","deactivate")
			self.request_api_to_manage("parcial","deactivate")

		elif code == 3462448:  # codigos cerrar mando completa (cambiar por lectura a bd)
			self.request_api_to_manage("completa","activate")

		elif code == 3462592:  # codigos parcial mando
			self.request_api_to_manage("parcial","activate")

		else:
			self.alarm("Sensor detected something: %s" % self.gpio)

	def check_listendata(self):
		self.stop_thread = False
		pi = pigpio.pi() # Connect to local Pi.
		while not self.stop_thread:

			bus = rx(pi, gpio=27, callback=self.handler_events)
			time.sleep(5)
			bus.cancel()
			continue
		pi.stop()
