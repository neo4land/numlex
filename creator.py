#!/usr/bin/python
# -*- coding: utf8 -*-
import logging
log = logging.getLogger(__name__)
from dbworker import DBworker
from getpass import getpass

__author__ = "Stinger <neo4land@gmail.com>"
__license__ = "GNU Lesser General Public License (LGPL)"


class DBCreator(DBworker):
    """
    This helps to create new database and user.
    """
    def initdb(mtd):
        def _initdb(self, *args, **kwargs):
            _res = False
            if self._connector(kwargs):
                try:
                    _res = mtd(self, *args)
                except StandardError as err:
                    log.error("MySQL error:%s" % err)
                    print(err)
                finally:
                    self._disconnector()
            return _res
        return _initdb

    @initdb
    def create_db(self, dbname=None):
        print("Connected! Creating '%s', please wait..." % dbname)
        fd = open('dbsrc.sql', 'r')
        sqlfile = fd.read().replace("BDPN", dbname, 2)
        fd.close()
        for recset in self._cursor.execute(sqlfile, multi=True):
            if recset.with_rows:
                log.info("Rows produced by statement '{0}':".format(recset.statement))
                print(recset.fetchall())
            else:
                log.info("Number of rows affected by statement '{0}': {1}".format(
                    recset.statement, recset.rowcount))
        return True

    @initdb
    def create_user(self, usr, psw, dbn):
        _ddl_sql = "CREATE USER {usr} IDENTIFIED BY '{psw}'; " \
                   "GRANT ALL ON {dbn}.* TO {usr} ; ".format(usr=usr, psw=psw, dbn=dbn)
        for recset in self._cursor.execute(_ddl_sql, multi=True):
            pass
        return True


def yes_or_no(question):
    reply = str(raw_input(question+' (y/N): ')).lower().strip()
    if reply in ['y', 'yes', 'yep']:
        return True
    else:
        return False

if __name__ == "__main__":
    admn = {}
    config = globals()['bdpnscfglob']
    logging.getLogger().setLevel(config.main['log_level'])
    # Input user/pass for one who allowed to create database
    log.debug("%s module started." % __name__)
    print("Entering initialisation mode...\n"
          "Please, input MySQL information to build new database(will be used only once).")
    admn['host'] = raw_input("Enter database host:")
    config.mysql['host'] = admn['host']
    admn['user'] = raw_input("Enter user with database creation rights:")
    admn['password'] = getpass("Password will not be visible:")
    new_dbname = raw_input("Enter new database name[BDPN]:")
    if not new_dbname:
        new_dbname = "BDPN"
    admn['connection_timeout'] = 20
    creator = DBCreator(config=config)
    if creator.create_db(new_dbname, **admn):
        config.mysql['database'] = new_dbname
        print("Database '%s' created!" % new_dbname)
        log.debug("Database '%s' created!" % new_dbname)
        if yes_or_no("Do you wish to create a user for new database?"):
            new_usr = raw_input("Enter new user name(this will fail if one exists):")
            new_psw = getpass("Enter password for new user:")
            new_host = "%"
            if yes_or_no("Do you wish to limit user's connection to host?"):
                new_host = raw_input("Enter host IP:")
            if creator.create_user("'%s'@'%s'" % (new_usr, new_host), new_psw, new_dbname, **admn):
                config.mysql['user'] = new_usr
                config.mysql['password'] = new_psw
                print("User '%s' created and saved to settings file." % new_usr)
                log.debug("User '%s' created and saved to settings file as a plain text." % new_usr)
            else:
                print("Failed to create new user.")
    del admn
    print("You can change settings in your settings.cfg file.\nDatabase initialization is completed.")
