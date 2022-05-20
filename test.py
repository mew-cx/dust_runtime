#! /usr/bin/env python

import syslog_client
log = syslog_client.Syslog("remote-host-name")
log.send("howdy", syslog_client.Level.WARNING)
