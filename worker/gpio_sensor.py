from tools.sensor import Sensor
import pigpio
from tools.pigpio433 import rx
import logging
import time
import sys
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
			self.checker_thread = threading.Thread(name="thread-checker-%s" % self.device_id,
												   target=self.check_listen_data)
			self.checker_thread.start()
		else:
			logging.error("AlkAlarm Sensor couldn't be activated")

	def deactivate(self):
		if not self.corrupted:
			self.stop_thread = True
		else:
			logging.error("AlkAlarm Sensor couldn't be deactivated") # maybe make this more clear

	def check_listen_data(self):
		pi = pigpio.pi() # Connect to local Pi.
		while True:
			bus = rx(pi, gpio=27)
			logging.error(bus.details())
			self.alarm("Sensor detected something: %s" % bus.code())
			time.sleep(60)
		pi.stop()