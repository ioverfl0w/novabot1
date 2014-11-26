import sys
sys.path.append("./lib/")
import Utility

class Stats:
	
	def __init__(self, eng):
		self.type = ["PRIVMSG", "JOIN", "PART"]
		self.name = "stats"
		self.engine = eng
		self.func = Utility.Misc()
		self.netlist = []
		
		for i in self.engine.binfo:
			self.netlist.append(NetList(i[0]))
			
		self.engine.log.write("(s) Stats active for " + str(len(self.netlist)) + " networks")
		for net in self.netlist:
			self.engine.log.write("(s) --> " + net.network.name)
			
	def push_all(self):
		for net in self.netlist:
			i = net.push_all()
			if i < 0:
				self.engine.log.write("(s) pushed " + str(i) + " users on " + net.network.name)
		
	def get_network(self, bot):
		for i in range(len(self.netlist)):
			if self.netlist[i].network == bot.network:
				return i
		self.engine.log.write("(s) error: no network for " + str(bot.network))
		return None

	def message(self, bot, who, location, message, args):
		n = self.get_network(bot)
		if not n == None:
			self.netlist[n].record_message(who, message)
			
		if args[0].lower() == "!help":
			return bot.notice(location, "Stats help: !me")
			
		if args[0].lower() == "!me":
			u = self.netlist[n].loadUser(who)
			return bot.message(location, "2(Stats) " + who[0] + " 1- 3Joins: " + str(u.joins()) + " 3Parts: " + str(u.parts()) + " 3Messages: " + str(u.messages()) + " 3Characters: " + str(u.characters()))
		
	def join(self, bot, who, location):
		n = self.get_network(bot)
		if not n == None:
			self.netlist[n].record_join(who)
		
	def part(self, bot, who, location):
		n = self.get_network(bot)
		if not n == None:
			self.netlist[n].record_part(who)

class NetList:
	
	def __init__(self, network):
		self.network = network
		self.users = []
		
	def record_message(self, who, message):
		user = self.loadUser(who)
		user.appmsg(len(message))
		
	def record_join(self, who):
		user = self.loadUser(who)
		user.appjoin()
		
	def record_part(self, who):
		user = self.loadUser(who)
		user.apppart()
		
	def loadUser(self, who):
		who[0] = who[0].lower()
		for u in self.users:
			if u.nick == who[0]:
				return u
		return self.read(who)
		
	def create(self, who):
		u = StatUser(who, [0,0,0,0])
		self.users.append(u)
		return u
		
	def push_all(self):
		for user in self.users:
			f = open(("./data/stats/" + self.network.name + "/" + user.nick + ".u").lower(), 'w')
			for x in user.stats:
				f.write(str(x) + "\n")
			f.close()
		i = len(self.users)
		self.users = []
		return i
		
	def read(self, who):
		try:
			f = open(("./data/stats/" + self.network.name + "/" + who[0] + ".u").lower(), 'r')
			x = f.read()
			f.close()
			r = []
			for a in x.split("\n"):
				if not a == "":
					r.append(int(a))
			u = StatUser(who, r)
			self.users.append(u)
			return u
		except Exception,e:
			print e
			return self.create(who)

class StatUser:
	
	"""
	Stats {
		0 - joins
		1 - parts
		2 - messages
		3 - characters
	}
	"""
	
	def __init__(self, who, stats):
		self.nick = who[0].lower()
		self.stats = stats
		
	def joins(self):
		return self.stats[0]
		
	def parts(self):
		return self.stats[1]
		
	def messages(self):
		return self.stats[2]
		
	def characters(self):
		return self.stats[3]
	
	def adjust(self, i, amount):
		self.stats[i] = self.stats[i] + amount
		
	def appjoin(self):
		self.adjust(0, 1)
		
	def apppart(self):
		self.adjust(1, 1)
		
	def appmsg(self, amount):
		self.adjust(2, 1) #Add a line
		self.adjust(3, amount) #Append characters
