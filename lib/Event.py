import traceback

class Event:

	def __init__(self, access):
		self.mods = []
		self.unloaded = []
		self.access = access
		self.last = None

	def add_mod(self, mod):
		self.mods.append(mod)
		
	def get_mod(self, name):
		for mod in self.mods:
			if mod.name == name:
				return mod
		return None
		
	def unload(self, name):
		name = name.lower()
		for mod in self.mods:
			if mod.name == name:
				self.mods.remove(mod)
				self.unloaded.append(mod)
				return True
		return False
		
	def reload(self, name):
		name = name.lower()
		for mod in self.unloaded:
			if mod.name == name:
				self.add_mod(mod)
				self.unloaded.remove(mod)
				return True
		return False
		
	def get_list(self):
		result = []
		for m in self.mods:
			result.append(m.name)
		return result

	def reload_mods(self):
		if len(self.unloaded) > 0:
			self.mods = self.mods + self.unloaded
			self.unloaded = []
		for mod in self.mods:
			try:
				mod.reload_mod()
			except Exception:
				pass

	def process(self, bot, line):
		if line == "":
			return
		
		line = line.strip()

		x = line.split("\n")
		for y in x:
			if not self.last == None:
				y = self.last + y
				self.last = None
			
			args = y.split(" ")
			if len(args) == 1:
				self.last = args[0]
				continue
			#debug
			#print line
			try:

				if args[0] == "PING":
					return bot.pong(args[1])

				if len(args) < 2:
					return

				if args[1] == "PRIVMSG":
					self.msg(bot, args[0][1:], args[2], line[line[1:].index(' :') + 3:])
				
				if args[1] == "JOIN":
					self.join(bot, args[0][1:], args[2])
	
				if args[1] == "PART":
					self.part(bot, args[0][1:], args[2])

				if args[1] == "QUIT":
					self.quit(bot, args[0][1:], args[2])
	
				if args[1] == "MODE":
					self.mode(bot, args[0][1:], args[2], line[(line.index(args[2]) + len(args[2]) + 1):] if len(args) > 3 else "")
	
				if args[1] == "NICK":
					self.nick(bot, args[0][1:], args[2])

				if args[1] == "KICK":
					self.kick(bot, args[0][1:], args[2], args[3])

				if args[1] == "352": #namelist
					self.namelist(bot, [args[7],args[4], args[5]], args[3])

				if args[1] == "307" or args[1] == "330":
					self.identify(bot, args[3])
					
			except Exception:
				print("Error:[" + line + "]")
				print traceback.format_exc()

	#auth user
	def identify(self, bot, who):
		if self.access.has_rights(who, bot) and not self.access.is_authed(who, bot):
			if self.access.auth.add_session(bot.network.name, who):
				bot.notice(who, "You have been authenticated.")

	def namelist(self, bot, who, location):
		for mod in self.mods:
			if (mod.type == "NAMELIST") if len(mod.type) == 1 else ("NAMELIST" in mod.type):
				mod.namelist(bot, who, location)

	def msg(self, bot, who, location, rem):
		#split for parsing by command modules
		user = [who[:who.index('!')], who[who.index('!') + 1:who.index('@')], who[who.index('@') + 1:]]
		args = rem.split(" ")
		
		for mod in self.mods:
			if (mod.type == "PRIVMSG") if len(mod.type) == 1 else ("PRIVMSG" in mod.type):
				mod.message(bot, user, location, rem, args)

	def mode(self, bot, who, location, modes):
		user = [who[:who.index('!')], who[who.index('!') + 1:who.index('@')], who[who.index('@') + 1:]]

		for mod in self.mods:
			if (mod.type == "MODE") if len(mod.type) == 1 else ("MODE" in mod.type):
				mod.mode(bot, user, location, modes)

	def kick(self, bot, who, location, kicked):
		user = [who[:who.index('!')], who[who.index('!') + 1:who.index('@')], who[who.index('@') + 1:]]

		for mod in self.mods:
			if (mod.type == "KICK") if len(mod.type) == 1 else ("KICK" in mod.type):
				mod.kick(bot, user, location, kicked)

	def nick(self, bot, who, name):
		user = [who[:who.index('!')], who[who.index('!') + 1:who.index('@')], who[who.index('@') + 1:]]

		for mod in self.mods:
			if (mod.type == "NICK") if len(mod.type) == 1 else ("NICK" in mod.type):
				mod.nick(bot, user, name)

	def join(self, bot, who, location):
		#split for parsing by command modules
		user = [who[:who.index('!')], who[who.index('!') + 1:who.index('@')], who[who.index('@') + 1:]]
		location = location[1:]
		
		for mod in self.mods:
			if (mod.type == "JOIN") if len(mod.type) == 1 else ("JOIN" in mod.type):
				mod.join(bot, user, location)

	def part(self, bot, who, location):
		#split for parsing by command modules
		user = [who[:who.index('!')], who[who.index('!') + 1:who.index('@')], who[who.index('@') + 1:]]
		
		for mod in self.mods:
			if (mod.type == "PART") if len(mod.type) == 1 else ("PART" in mod.type):
				mod.part(bot, user, location)

	def quit(self, bot, who, location):
		#split for parsing by command modules
		user = [who[:who.index('!')], who[who.index('!') + 1:who.index('@')], who[who.index('@') + 1:]]
		
		for mod in self.mods:
			if mod.type == "QUIT":
				mod.quit(bot, user, location)
