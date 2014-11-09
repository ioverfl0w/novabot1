import sys
sys.path.append("./lib/")
import Utility

class AdvControl:
	
	def __init__(self, eng):
		self.type = "PRIVMSG"
		self.engine = eng
		self.func = Utility.Misc()

	def message(self, bot, who, location, message, args):
		
		if (self.engine.get_access().get_user_rights(who, bot) < 1): # Trusted Commands and Above (1+)
			return
