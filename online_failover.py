#!/usr/bin/env python
"""test module"""
# pylint : invalid-name
from online_api import api
from netifaces import interfaces  # pylint: no-name-in-module
from netifaces import ifaddresses, AF_INET
from pprint import pprint
import sys
import logging

logger = logging.getLogger("online-failover")

class OnlineDedup(object):

    def __init__(self, ips):
        self.ips = ips
        self._failover = None
        self._server_props = None
        self._server_id = None

    @property
    def server_props(self):
        if not self._server_props:
            logger.warn("fetching server props for %i" % self.server_id)
            self._server_props = api.server(self.server_id).get()
        return self._server_props

    def fo_status(self):
        failovers = self.server_props["network"]["ipfo"]
        hostname = self.server_props["hostname"]
        print "Configured failovers for %s:" % hostname
        for ip in failovers:
            print " - %s" % ip

        configured_ip = [
            ip for ip in self.server_props["ip"] if "server" in ip]
        for ip in configured_ip:
            s = "(MYSELF)"if hostname in ip["reverse"] else "(BACKUP)"
            print " - %s (%s)" % ( ip["address"], s)
            pprint(ip)
        return None

    @property
    def server_id(self):
        if not self._server_id:
            logger.warn("fetching server_id")
            def get_server_id(server):
                if server:
                    return int(server["$ref"].split('/')[-1])
                else:
                    return None
            server_ids = set([(f["source"], get_server_id(f["server"])) for f in self.failover ])
            logger.info("failover ips -> servers:")
            for k, v in server_ids:
                logger.info("%s -> %s" % (k, v))
            my_server = [(k, v) for k, v in server_ids if k in self.ips]
            if my_server:
                my_id = set(v for k, v in my_server)
                if len(my_id) > 1:
                    logger.exception(
                        "more than one server id correspond to the given ip: %s" % ",".join(my_id))
                    raise RuntimeError("more than one server id detected")
                else:
                    my_id = my_id.pop()
                    logger.info("server id: %i" % my_id)
            else:
                logger.exception("no server detected for the given ips")
                raise RuntimeError("no server id detected")
            self._server_id = my_id
        return self._server_id

    @property
    def failover(self):
        if not self._failover:
            self._failover = api.server.failover.get()
        return self._failover


if __name__ == '__main__':
    ips = sys.argv[1:]
    if not ips:
        logger.info("no ip provided as argument. detecting ips...")
        ips = set(
            [i['addr'] for ifaceName in interfaces() for i in ifaddresses(ifaceName).setdefault(AF_INET) \
            ])
        logger.info("testing consistency for server with ips: %s" % ",".join(ips))

    o = OnlineDedup(ips)
    print o.server_id
    #pprint(o.server_props)
    print o.fo_status()
