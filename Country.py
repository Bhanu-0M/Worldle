import pandas as pd
from math import radians, sin, cos, asin, sqrt, ceil, atan2, pi, degrees, floor
from emoji import emojize
import numpy as np 
from PIL import Image
import PIL.ImageOps
from io import BytesIO
from time import sleep

R = 6371 # radius of earth
M = 2004 # Maximum distance b/w any 2 countries on earth
pd.set_option("max_colwidth", None)
df = pd.read_json('info.json') # country data
bearings = np.array([[360], np.arange(start=1, stop=90, step=1), [90], np.arange(start=90, stop=180, step=1), [180], np.arange(start=180, stop=270, step=1), [270], np.arange(start=270, stop=360, step=1)], dtype=object)
directions = np.array(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
compass = np.stack((bearings, directions), axis=1)

class Country:
	def __init__(self, name):
		if name == 'Random':
			print("Loading Data...")
			entry = df.sample()
			self.name = entry.name.item()
		else:
			self.name = name 
			entry = df.loc[df.name == self.name]
		self.longitude, self.latitude, self.map = entry.longitude.item(), entry.latitude.item(), entry.maplink.item()
		self.country = entry.country.item()

	# Haversine formula: https://en.wikipedia.org/wiki/Haversine_formula
	# Formula: d = 2R⋅sin⁻¹(√[sin²((θ₂ - θ₁)/2) + cosθ₁⋅cosθ₂⋅sin²((φ₂ - φ₁)/2)]).
	def distance_to(self, country):
		lon1 = radians(self.longitude)
		lon2 = radians(country.longitude)
		lat1 = radians(self.latitude)
		lat2 = radians(country.latitude)
		dlon = lon2 - lon1
		dlat = lat2 - lat1

		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * asin(sqrt(a))
		d = ceil(c * R)
		# proximity = abs(M-d)
		# percentage = floor((proximity/M)*100)
		#   const proximity = Math.max(MAX_DISTANCE_ON_EARTH - distance, 0); return Math.floor((proximity / MAX_DISTANCE_ON_EARTH) * 100);
		return d


	# θ = atan2(sin(Δlong)*cos(lat2), cos(lat1)*sin(lat2) − sin(lat1)*cos(lat2)*cos(Δlong))
	# Δlong = long2-long1
	# Compass bearing: http://academic.brooklyn.cuny.edu/geology/leveson/core/graphics/mapgraphics/circ-360newsx.gif
	def direction_to(self, country, with_emoji=False):
		lon1 = radians(self.longitude)
		lon2 = radians(country.longitude)
		lat1 = radians(self.latitude)
		lat2 = radians(country.latitude)
		dlon = lon2 - lon1

		angle = degrees(atan2(sin(dlon)*cos(lat2), cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dlon)))
		angle = ceil((angle + 360) % 360)
			
		# print("Angle:", angle)

		# for d in [90, 180, 270, 360]:
		# 	if abs(d - angle) in range(1, 6): # if off by 1 to 9 degrees still consider it and round it off (eg. 97 -> 90, 353 -> 360, etc)
		# 		angle = d
				# break

		if with_emoji:
			direction = self.get_direction(angle)
			E = {
				'E': emojize(":right_arrow:", variant="emoji_type"),
				'NE': emojize(":up-right_arrow:", variant="emoji_type"),
				'N': emojize(":up_arrow:", variant="emoji_type"),
				'NW': emojize(":up-left_arrow:", variant="emoji_type"),
				'W': emojize(":left_arrow:", variant="emoji_type"),
				'SW': emojize(":down-left_arrow:", variant="emoji_type"),
				'S': emojize(":down_arrow:", variant="emoji_type"),
				'SE': emojize(":down-right_arrow:", variant="emoji_type"),
				'There': emojize(":party_popper:", variant="emoji_type")
			}
			# return angle, direction, E[direction] 
			return angle, E[direction]
		else:
			return angle

	def show(self):
		return f"Latitude: {self.latitude}, Longitude: {self.longitude}, Country: {self.country}, Name: {self.name}"

	def get_direction(self, angle):
		if angle == 0:
			return 'There' 
		for info in compass:
			if angle in info[0]:
				return info[1]

	def display_map(self):
		img = Image.open(self.map)
		img.show()