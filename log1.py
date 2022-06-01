# syslog_client_rfc5424.py

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
        return "<{}>1 {} {} {} {} {} {} {}\n".format(
            (facility << 3) + severity,
            timestamp or "-",
            hostname or "-",
            app_name or "-",
            procid or "-",
            msgid or "-",
            structured_data or "-",
            msg or "")

#############################################################################

import wifi
import socketpool
import ipaddress
from secrets import secrets

HOST = "pink"
PORT = 514
TIMEOUT = 5  #None

print("connecting to AP", secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("my ipaddr", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
server_ipv4 = ipaddress.ip_address(pool.getaddrinfo(HOST, PORT)[0][4][0])
print("server ipaddr", server_ipv4)
print("ping time", wifi.radio.ping(server_ipv4), "ms")

with pool.socket(pool.AF_INET, pool.SOCK_STREAM) as s:
    print("creating socket")
    s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    print("connecting to socket")
    s.connect((HOST, PORT))

    logmsg = FormatRFC5424(
        facility = Facility.LOCAL3,
        severity = Severity.INFO,
        timestamp = "2022-05-31T22:33:44Z",
        hostname = "1.2.3.4",
        app_name = "dust",
        procid = "PROCid",
        msgid = "MSGid",
        structured_data = "[x]",
        msg = "This is the real message here")
    print(repr(logmsg))
    sent = s.send(logmsg)
    print("sent length : %d\n" % sent)

    logmsg = FormatRFC5424(
        facility = Facility.LOCAL3,
        severity = Severity.NOTICE,
        timestamp = "2022-05-31T22:33:55Z",
        hostname = wifi.radio.ipv4_address,
        app_name = "dust2",
        msg = "Data goes here")
    print(repr(logmsg))
    sent = s.send(logmsg)
    print("sent length : %d\n" % sent)
