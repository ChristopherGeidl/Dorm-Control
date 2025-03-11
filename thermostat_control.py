import json

STATE_FILE = "device_states.json"

class Thermostat:
	def __init__(self, max_temperature, min_temperature, fan_status, window_status):
		print(f"Initializing thermostat: Maximum={max_temperature}, Minimum={min_temperature}, Fan Status={fan_status}, Window Status={window_status}")
		self.temperature = ""
		self.max_temperature = max_temperature
		self.min_temperature = min_temperature
		self.fan_status = fan_status
		self.window_status = window_status
	def change_thermostat(self, max_temperature, min_temperature, fan_status, window_status):
		print(f"Setting thermostat to Maximum={max_temperature}, Minimum={min_temperature}, Fan Status={fan_status}, Window Status={window_status}")
		self.max_temperature = max_temperature
		self.min_temperature = min_temperature
		self.fan_status = fan_status
		self.window_status = window_status
	def update_TH_state(self, new_state):
		try:
			with open(STATE_FILE, 'r') as file:
				state = json.load(file)
		except FileNotFoundError:
			state = {}
		state['thermostat'].update(new_state)
		with open(STATE_FILE, 'w') as file:
			json.dump(state, file, indent=4)
