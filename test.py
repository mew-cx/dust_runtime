#! /usr/bin/env python

import syslog_client
log = syslog_client.Syslog(host="pink", facility=syslog_client.Facility.LOCAL3)
log.send("udp_syslog : Hi to pink LOCAL3.INFO", syslog_client.Severity.INFO)
