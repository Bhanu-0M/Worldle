import json

class Completer(object):  
    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0: 
            if text: 
                text = text.title()
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else: 
                self.matches = self.options[:]
        try: 
            return self.matches[state]
        except IndexError:
            return None

countries = []
with open('info.json') as fl:
    for info in json.loads(fl.read()):
        countries.append(info['name'])

completer = Completer(countries)
# print(completer.options, len(completer.options))