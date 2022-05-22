#! /usr/bin/env python

import syslog_client
log = syslog_client.Syslog(host="pink", facility=syslog_client.Facility.LOCAL3)
log.send("another test", syslog_client.Severity.WARNING)
