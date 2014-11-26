import time

class StatPush:
	
	def __init__(self, stats):
		self.name = "statpush"
		#delay in seconds
		self.delay = 60*1 #1 minute
		self.start = 0
		self.stats = stats
		
	def strike(self):
		return (self.start + self.delay) <= time.time()
			
	def clear(self):
		self.start = time.time()
	
	def perform(self):
		self.stats.push_all()
