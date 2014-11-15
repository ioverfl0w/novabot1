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
import Alarms
sys.path.append("./mods/")
import Basic
import AdvControl
import AlarmClock
import Stats

logger = Logger.Logger()
access = Access.Access(logger)
event = Event.Event(access)
scheduler = Scheduler.Scheduler()

# bot network info
#		Title	Network			Port	NICK	USER		NICKSERV		[AJOIN]
rizon = [Utility.Network("Rizon", "irc.rizon.net", 6697),
		Utility.Identity("NovaBot1", "nova", "passwordhere", ["#testing"])]

#create Engine
eng = Engine.Engine(event, [rizon], scheduler, logger) #event, bots, sched, logger

#modules we are loading
scheduler.schedule_event(AuthSys.AuthSys(eng))
scheduler.schedule_event(KeepAlive.KeepAlive(eng))
scheduler.schedule_event(Alarms.Alarms())
event.add_mod(Basic.Basic(eng))
event.add_mod(AdvControl.AdvControl(eng))
event.add_mod(AlarmClock.AlarmClock(scheduler.get_event("alarms")))
event.add_mod(Stats.Stats(eng))

eng.execute()

