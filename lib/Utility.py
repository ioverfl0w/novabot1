class Network:

	def __init__(self, name, address, port):
		self.name = name
		self.address = address
		self.port = port

class Identity:

	def __init__(self, nick, user, pw, ajoin):
		self.nick = nick
		self.user = user
		self.nickserv = pw
		self.ajoin = ajoin

class Misc:

	def space(self, string, total_len):
		if len(string) > total_len:
			return string_a
		
		return string + (" " * (total_len - len(string)))
