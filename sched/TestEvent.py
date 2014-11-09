import time

class TestEvent:
	
	def __init__(self, bot):
		self.name = "testevent"
		#delay in seconds
		self.delay = 60
		self.start = 0
		self.bot = bot
		print
		
	def strike(self):
		return 1 if (self.start + self.delay) <= time.time() else 0
			
	def clear(self):
		self.start = time.time()
	
	def perform(self):
		self.bot.message("#channel", "it's been a minute")
