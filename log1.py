# syslog_rfc5424.py

#############################################################################

class Facility:
    "Syslog facilities"
    KERN,USER,MAIL,DAEMON,AUTH,SYSLOG,LPR,NEWS,UUCP,CRON,AUTHPRIV,FTP = range(0,12)
    LOCAL0,LOCAL1,LOCAL2,LOCAL3,LOCAL4,LOCAL5,LOCAL6,LOCAL7 = range(16, 24)

class Severity:
    "Syslog severities"
    EMERG,ALERT,CRIT,ERR,WARNING,NOTICE,INFO,DEBUG = range(0,8)

def FormatRFC5424( facility = Facility.USER,
                   severity = Severity.NOTICE,
                   timestamp = None,
                   hostname = None,
                   app_name = None,
                   procid = None,
                   msgid = None,
                   structured_data = None,
                   msg = None) :
        return "<{}>1 {} {} {} {} {} {} {}".format(
            (facility << 3) + severity,
            timestamp or "-",
            hostname or "-",
            app_name or "-",
            procid or "-",
            msgid or "-",
            structured_data or "-",
            msg or "")

print( FormatRFC5424( app_name="Foo" ))
#############################################################################

import wifi
import socketpool
import ipaddress
from secrets import secrets

HOST = "pink"
PORT = 514
TIMEOUT = 5  #None

wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Self IP", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
server_ipv4 = ipaddress.ip_address(pool.getaddrinfo(HOST, PORT)[0][4][0])
print("Server ping", server_ipv4, wifi.radio.ping(server_ipv4), "ms")

with pool.socket(pool.AF_INET, pool.SOCK_STREAM) as s:
    s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    s.connect((HOST, PORT))

    logmsg = FormatRFC5424(
        facility = Facility.LOCAL3,
        severity = Severity.INFO,
        timestamp = "now",
        app_name = "dust",
        msgid = "data1",
        msg = "This is the real message here")
    sent = s.send(logmsg)
