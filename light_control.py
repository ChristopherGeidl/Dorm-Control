import time
import random
import board
import neopixel

def interpolate_step(color1, color2, step_sizez):
	return (
		int(color1[0] + (color2[0] - color1[0]) * step_size),
		int(color1[1] + (color2[1] - color1[1]) * step_size),
		int(color1[2] + (color2[2] - color1[2]) * step_size)
	)


class Light:
	LED_COUNT = 100
	PIN = board.D18

	def __init__(self, status, color, brightness, type):
		print(f"Initializing lights: status={status} color={color}, brightness={brightness}, type={type}")
		self.status = status
		self.color = (color[0], color[1], color[2])
		self.brightness = float(brightness)/100 #0-1
		self.type = type

		self.pixels = neopixel.NeoPixel(Light.PIN, Light.LED_COUNT, brightness=self.brightness)
		self.light_work()

	def change_lights(self, status, color, brightness, type):
		print(f"Setting lights to Status={status}, Color={color}, Brightness={brightness}, Type={type}")
		self.status = status
		self.color = (color[0], color[1], color[2])
		if self.brightness != brightness:
			self.brightness = float(brightness)/100
			self.pixels.brightness = self.brightness
		self.type = type
		if self.type == "Static" or self.type == "Rainbow Static":
			self.light_work()

	def light_work(self):
		rainbow = [
			(255, 0, 0), #Red
			(255, 165, 0), #Orange
			(255, 255, 0), #Yellow
			(0, 255, 0), #Green
			(0, 0, 255), #Blue
			(75, 0, 130), #Indigo
			(238, 130, 238), #Violet
		]
		current_rainbow_color = rainbow[0]
		current_rainbow_index = 0

		current_strobe_color = (0,0,0)
		target_strobe_color = self.color

		slide_strip_length = 10
		slide_start = Light.LED_COUNT - slide_strip_length + 1

		while self.status == "on":
			if self.type == "Static":
				self.pixels.fill((color[0],color[1],color[2]))
				break
			elif self.type == "Rainbow Static":
				section_length = Light.LED_COUNT / (len(rainbow) - 1)
				for i in range(Light.LED_COUNT):
					section = int(i // section_length)
					t = (i % section_length) / section_length
					self.pixels[i] = interpolate_step(rainbow[section], rainbow[section+1], t)
				break
			elif self.type == "Rainbow Cycle":
				next_color = rainbow[(current_rainbow_index + 1) % len(rainbow)]
				current_rainbow_color = interpolate_step(current_rainbow_color, next_color, 0.02)
				self.pixels.fill(current_rainbow_color)
			elif self.type == "Pulse":
				current_strobe_color = interpolate_step(current_strobe_color, target_strobe_color, 0.02)
				self.pixels.fill(current_strobe_color)
				if current_strobe_color == target_strobe_color:
					target_color = (0,0,0) if target_strobe_color == self.color else self.color
			elif self.type == "Sparkle":
				for i in range(Light.LED_COUNT):
					if random.random() < 0.1:
						self.pixels[i] = self.color
					else:
						self.pixels[i] = (0,0,0)
			elif self.type == "Slide":
				self.pixels.fill((0,0,0))
				for i in range(slide_start, slide_start + slide_strip_length):
					self.pixels[i] = self.color
				slide_start += 1
				if slide_start > Light.LED_COUNT - slide_strip_length + 1:
					slide_start = Light.LED_COUNT - slide_strip_length + 1
			elif self.type == "Strobe":
				if self.pixels[0] == (0,0,0):
					self.pixels.fill(self.color)
				else:
					self.pixels.fill((0,0,0))
			else:
				print("Error: type " + type + " is invalid")
				break
			time.sleep(0.05) #0.05 seconds
		if self.status == "off":
			self.pixels.fill((0,0,0))
