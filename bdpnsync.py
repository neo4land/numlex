#!/usr/bin/python
# -*- coding: utf8 -*-
# BDPN sftp synchronisation program.
import logging
logging.basicConfig(level=40,
                    format='%(asctime)s - %(message)s')
log = logging.getLogger(__name__)
import sys
import os
import time
import runpy
from config import Settings
from numlex import make_obj_list
from dbworker import DBworker
from sftp import SftpChannel
from daemon import Daemon

__author__ = "Stinger <neo4land@gmail.com>"
__license__ = "GNU Lesser General Public License (LGPL)"

if sys.version_info <= (2, 7):
    raise RuntimeError('You need Python 2.7+ for this module.')


class BDPNdmn(Daemon):
    def __init__(self, *args, **kwargs):
        self.run_dir = os.path.dirname(os.path.realpath(__file__))+'/'
        self.config = Settings(self.run_dir+"settings.cfg")
        log.debug("Run dir %s" % self.run_dir)
        self.bdpn = make_obj_list()
        self.sftp = SftpChannel(self.bdpn, self.config)
        self.mysql = DBworker(self.bdpn, self.config)
        super(BDPNdmn, self).__init__(*args, **kwargs)

    def wait4next_update(self):
        """Sleep timer"""
        __step = self.config.main['sync_every_minutes'] * 60
        __delta = (__step - ((time.time()+time.timezone) % __step)) + 900
        log.info("Sleeping %i sec..." % __delta)
        time.sleep(__delta)
        return True

    def run(self):
        log.info("Starting daemon...")
        countdown = 3
        while countdown > 0:
            try:
                log.debug("Reading settings...")
                ok = self.config.load_config()
                logging.getLogger().setLevel(self.config.main['log_level'])
                if ok:
                    log.debug("Settings are OK. Doing synchronization...")
                    ok &= self.mysql.get_last() and self.sftp.synchronize() and self.mysql.update()
                if ok:
                    log.info("Synchronization completed! Waiting for next turn.")
                    countdown = 3
                    self.wait4next_update()
                else:
                    countdown -= 1
                    log.warning("Failed to update. Retry in 5min")
                    time.sleep(300)
            except KeyboardInterrupt:
                print("^C received, shutting down")
                break
            except RuntimeError as err:
                log.error("Runtime ERROR:%s\nFix it and try again." % err, exc_info=True)
                break

if __name__ == "__main__":
    BDPNsync = BDPNdmn('/run/BDPNsync.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            BDPNsync.start()
        elif 'stop' == sys.argv[1]:
            BDPNsync.stop()
        elif 'restart' == sys.argv[1]:
            BDPNsync.restart()
        elif 'initdb' == sys.argv[1]:
            if not BDPNsync.getpid():
                runpy.run_module('creator', run_name="__main__", init_globals={'bdpnscfglob': BDPNsync.config})
            else:
                sys.stderr.write("Stop daemon first, then try again.\n")
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart|initdb" % sys.argv[0]
        sys.exit(2)
