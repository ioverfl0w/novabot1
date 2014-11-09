import sys
sys.path.append("./lib/")
import Utility

class Basic:
	
	def __init__(self, eng):
		self.type = "PRIVMSG"
		self.engine = eng
		self.func = Utility.Misc()

	def message(self, bot, who, location, message, args):
		if args[0].lower() == "!test":
			return bot.message(location, "The test was successful, " + who[0] + "!")

		if (self.engine.get_access().get_user_rights(who, bot) < 1):
			return

		if args[0].lower() == "!test2":
			bot.notice(who[0], str(self.engine.get_access().get_user_rights(who, bot)))
			bot.message(location, "Permissions test was successful, " + who[0] + "!")
