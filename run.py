## TODO	- enable raw bash commands (?)

import sys
import time
sys.path.append("./lib/")
import Event
import Access
import Scheduler
import Engine
import Utility
import Logger
sys.path.append("./sched/")
import AuthSys
import KeepAlive
sys.path.append("./mods/")
import Basic

logger = Logger.Logger()
access = Access.Access(logger)
event = Event.Event(access)
scheduler = Scheduler.Scheduler()

# bot network info
#		Title	Network			Port	NICK	USER		NICKSERV		[AJOIN]
rizon = [Utility.Network("Rizon", "irc.rizon.net", 6697),
		Utility.Identity("NovaBot", "nova", "passwordhere", ["#nova"])]

#create Engine
eng = Engine.Engine(event, [rizon], scheduler, logger) #event, bots, sched, logger

#modules we are loading
event.add_mod(Basic.Basic(eng))
scheduler.schedule_event(AuthSys.AuthSys(eng))
scheduler.schedule_event(KeepAlive.KeepAlive(eng))

eng.execute()

