class TempRule:
    def __init__(self, rulesstring):
        self.rulesstring = rulesstring
        self.temp = rulesstring['temp']
        self.time = rulesstring['time']