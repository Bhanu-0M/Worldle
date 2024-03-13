from Country import Country
from os import system
from sys import exit
from PIL import Image
from print_color import print
from termcolor import colored
import psutil
import readline
from autocompleter import completer, countries

# L = ['gb', 'ax', 'ss', 'bl', 'bq', 'sx', 'mf', 'cw'] # countries without information

# def clean(name):
# 	for country in countries:
# 		if name.lower() == country.lower():
# 			return country	

correctly_guessed, failed_to_guess = [], []

# compass = False
# if (input("Do you need a compass? [y/n]: ")) == "y":
# 	compass = True
# if compass:
# 	print("Loading Compass...", color='white', format='bold')
# 	Image.open('./Compass_rose.png').show()

def closeimages():
	for proc in psutil.process_iter():
		if proc.name() == "Microsoft.Photos.exe": # assuming default photo viewer is microsoft photos
			proc.kill()

readline.set_completer(completer.complete)
readline.parse_and_bind("tab: complete")

end = False
while not end:
	closeimages()
	compass = False
	if (input(colored("Do you need a compass? [y/n]: ", 'white', attrs=['bold']))) == "y":
		compass = True
	if compass:
		print("Loading Compass...", color='white', format='bold')
		Image.open('./Compass_rose.png').show()
	print("Choosing a random country....", color='white', format='bold')
	guess_country = Country(name="Random")
	print("Loading Map...", color='white', format='bold')
	mapimg = guess_country.display_map()
	n = 0
	textblock = ""
	while True:
		if n == 6:
			failed_to_guess.append(guess_country.name)
			system('clear')
			print(textblock) 
			break
		try:
			system('clear')
			print(textblock) 
			given_country = Country(name=input(f"Guess the country {n+1}/6 > "))
			distance = given_country.distance_to(guess_country)
			angle, emoji = given_country.direction_to(guess_country, with_emoji=True)
			result = f"{given_country.name} {distance:,} km {angle}° {emoji}\n"
			if distance == 0:
				result = colored(result, 'green', attrs=['bold'])
				print(result)
				print("You won!\n")
				correctly_guessed.append(guess_country.name)
				break
			n += 1
			textblock += colored(result, 'white', attrs=['bold'])

		except ValueError:
			textblock += colored("Unknown Country!\n", 'red', attrs=['bold'])

	print("\nCountry:", guess_country.name, f"({guess_country.country}) [Latitude: {guess_country.latitude}, Longitude: {guess_country.longitude}]")
	if input(colored("Play another game? [y/n]: ", 'white', attrs=['bold'])) != "y":
		end = True

print()
print(f"Matches played: {len(correctly_guessed)+len(failed_to_guess)}", color='white', format='bold')
print(f"Correctly guessed: {len(correctly_guessed)} ({', '.join(correctly_guessed)})", color='green')
print(f"Incorrectly guessed: {len(failed_to_guess)} ({', '.join(failed_to_guess)})", color='red')
closeimages()
# while True:
# 	if input("Enter anything to exit: "):
# 		exit()
