import sys
sys.path.append("./lib/")
import Utility

class AdvControl:
	
	def __init__(self, eng):
		self.type = "PRIVMSG"
		self.name = "advctrl"
		self.engine = eng
		self.func = Utility.Misc()

	def message(self, bot, who, location, message, args):
		
		if (self.engine.get_access().get_user_rights(who, bot) < 0): # Trusted Commands and Above (1+)
			return
		cmd = args[0].lower()
		
		if cmd == "!botstats":
			return bot.message(location, "BotsConnected: " + str(len(self.engine.get_bots())) + " - " +
						"ModsLoaded: " + str(len(self.engine.event.mods)) + " - " + 
						"SchedLoaded: " + str(len(self.engine.sched.evt)))
						
		if cmd == "!cmods":
			return bot.message(location, "LoadedMods: " + ", ".join(self.engine.event.get_list()))
			
		if cmd == "!csched":
			return bot.message(location, "LoadedSchedules: " + ", ".join(self.engine.sched.get_list()))
