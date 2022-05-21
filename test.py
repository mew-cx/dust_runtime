#! /usr/bin/env python

import syslog_client
log = syslog_client.Syslog(host="pink", facility=syslog_client.Facility.LOCAL3)
log.send("syslog_client Hi pink", syslog_client.Severity.INFO)
