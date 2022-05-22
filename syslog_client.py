"""
syslog_client.py
Derived from Author: Christian Stigen Larsen, License: PUBLIC DOMAIN
See RFC 3164, 5424.
"""

import socket

class Facility:
  "Syslog facilities"
  KERN, USER, MAIL, DAEMON, AUTH, SYSLOG, LPR, NEWS, UUCP, CRON, \
      AUTHPRIV, FTP = range(12)
  LOCAL0, LOCAL1, LOCAL2, LOCAL3, LOCAL4, LOCAL5, LOCAL6, \
      LOCAL7 = range(16, 24)

class Severity:
  "Syslog severities"
  EMERG, ALERT, CRIT, ERR, WARNING, NOTICE, INFO, DEBUG = range(8)

class Syslog:
  "A syslog client that logs to a remote server via UDP."
  def __init__(self,
               host="localhost",
               port=514,
               facility=Facility.DAEMON):
    self.host = host
    self.port = port
    self.facility = facility
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def send(self, message, severity):
    "Send a syslog message to remote host using UDP."
    data = "<%d> %s" % (severity + (self.facility << 3), message)
    self.socket.sendto(data.encode('utf-8'), (self.host, self.port))
