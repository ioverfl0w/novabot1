class AlarmClock:
	
	def __init__(self, alarm):
		self.type = "PRIVMSG"
		self.alarm = alarm

	def message(self, bot, who, location, message, args):
		if not location.startswith("#"):
			return
		
		if args[0] == "!add":
			if len(args) > 2:
				try:
					time = int(args[1])
				except Exception:
					return bot.notice(who[0], "Invalid time. How many minutes from now?")
				chk = self.alarm.add_alarm(who, time, location, message[message.index(args[2]):])
				if chk == 1:
					return bot.notice(who[0], "You already have an alarm set.")
				return bot.notice(who[0], "Your alarm has been set for " + args[1] + " minutes from now.")
			else:
				return bot.notice(who[0], "Syntax: !add [time] [message]")
				
		if args[0] == "!view":
			alarm = self.alarm.read_alarm(who)
			if len(alarm) == 0:
				return bot.notice(who[0], "You have no alarm set.")
			return bot.notice(who[0], "Channel: " + alarm[2] + " - Time left: " + alarm[1] + " mins - Message - " + alarm[3])
			
		if args[0] == "!cancel":
			alarm = self.alarm.read_alarm(who)
			if len(alarm) == 0:
				return bot.notice(who[0], "You have no alarm set.")
			if len(args) > 1 and args[1] == "confirm":
				if self.alarm.rem_alarm(who) == 1:
					return bot.notice(who[0], "Your alarm was removed successfully.")
				return bot.notice(who[0], "There was a conflict removing your alarm!")
			return bot.notice(who[0], "Type !cancel confirm to confirm the removal of your current alarm.")
