from Country import Country

while True:
	try:
		c1, c2 = Country(input("Enter a country > ")), Country(input("Enter a country > "))
		print("The distance and direction between", c1.name, "and", c2.name, "is", c1.distance_to(c2), "k.m.", c1.direction_to(c2, with_emoji=True))
	except ValueError:
		print("Unknown Country")
