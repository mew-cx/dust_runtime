#! /usr/bin/env python

import syslog_client
log = syslog_client.Syslog("localhost")
log.send("howdy", syslog_client.Level.WARNING)
