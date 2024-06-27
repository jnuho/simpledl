telnet -c pas.simpledl.net 443 2>&1 < /dev/null | grep Connected
telnet -c mqtt.simpledl.net 1883 2>&1 < /dev/null | grep Connected
telnet -c xmpp.simpledl.net 5223 2>&1 < /dev/null | grep Connected
telnet -c cwmp.simpledl.net 7548 2>&1 < /dev/null | grep Connected
telnet -c cdn.simpledl.net 7551 2>&1 < /dev/null | grep Connected
telnet -c data.simpledl.net 10443 2>&1 < /dev/null | grep Connected
