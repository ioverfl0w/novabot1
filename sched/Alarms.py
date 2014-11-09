import time

class Alarms:
	
	def __init__(self, bot):
		self.name = "alarms"
		#delay in seconds
		self.delay = 1
		self.start = 0
		self.bot = bot
		self.alarms = []
		
	def strike(self):
		return self.start <= time.time()
			
	def clear(self):
		self.start = time.time() + self.delay
		
	def read_alarm(self, registrar):
		for a in self.alarms:
			if a[0] == registrar[0]:
				x = str((int(a[1]) - time.time()) / 60)
				return [a[0], x, a[2], a[3]]
		return []
		
	def rem_alarm(self, registrar):
		for a in self.alarms:
			if a[0] == registrar[0]:
				self.alarms.remove(a)
				return 1
		return 0
		
	def add_alarm(self, registrar, tme, channel, message):
		for a in self.alarms:
			if a[0] == registrar[0]:
				return 1 #already has an alarm set
				
		self.alarms.append([registrar[0], (tme * 60) + time.time(), channel, message])
		return 0
	
	def exec_alarm(self, alarm):
		self.bot.message(alarm[2], "3Alarm 1- " + alarm[3] + " [set by " + alarm[0] + "]")
		self.bot.notice(alarm[0], "Your alarm has gone off!")
		self.alarms.remove(alarm)
	
	def perform(self):
		#do our checks
		for a in self.alarms:
			if a[1] <= time.time():
				self.exec_alarm(a)
