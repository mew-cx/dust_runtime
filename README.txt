https://csl.name/post/python-syslog-client/

Posted 14 Nov 2008 — updated 03 Dec 2013

While the Python standard library offers a syslog module,
(https://docs.python.org/2/library/syslog.html)
it seem to be a wrapper around the POSIX syslog system calls.
This means you cannot use it to send syslog messages over the network.
The code below implements a send() function as described in RFC 3164.
(https://www.ietf.org/rfc/rfc3164.txt)
It has been used in production on Windows boxes sending messages to a Linux syslog server.
For this to work you must configure your syslog daemon to accept logs from the network.


If you put it in a file syslog_client.py you can use it as a module.
```
    import syslog_client
    log = syslog_client.Syslog("remote-host-name")
    log.send("howdy", syslog_client.Severity.WARNING)
```

You can easily extend the class in several ways.
E.g., you may want to add some convenience functions like warn(), etc.
