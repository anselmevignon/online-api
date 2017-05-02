#!/usr/bin/env python
"""test module"""
from online_api import api
from pprint import pprint
import sys

if __name__ == '__main__':
    user_info = api.user.get()
    print user_info

    failovers = api.server.failover.get()
    pprint(failovers)

    print "\n\nhurray\n\n\n"
    value_it = (
            "%s <- %s" % (
                f["destination"],
                f["server"]['$ref'])
            for f in failovers
            if f["server"] is not None )
    #print "\n".join(value_it)


    servers = api.server.get()
    pprint(servers)

    server_refs = [s.split("/")[-1] for s in servers]

    #pprint(api.server(server_refs[0]).get())
    print "\n\nhurray\n\n\n"
#    pprint(api.server.ip("212.83.167.208").get())
    pprint(api.server.ip("195.154.176.120").get())
    print "\n\nhurray\n\n\n"
    pprint(api.domain.get())


