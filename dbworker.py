# -*- coding: utf8 -*-
import os
from functools import wraps
import mysql.connector
from mysql.connector import errorcode
import logging
log = logging.getLogger(__name__)

__author__ = "Stinger <neo4land@gmail.com>"
__license__ = "GNU Lesser General Public License (LGPL)"


class DBworker(object):
    """
    Class for all database related jobs.
    """
    def __init__(self, db_array=None, config=None):
        self._mysql = None
        self.config = config
        self.db_array = db_array

    def _connector(self, conn_params=None):
        """
        Open connection to MySQL server
        :param conn_params: a tuple with connection parameters
        :return: True/False depending on connection result
        """
        if not conn_params:
            conn_params = self.config.mysql
        """Connects to MySQL db"""
        try:
            log.info("Attempt to connect to MySQL")
            conn_params['client_flags'] = [128]
            conn_params['allow_local_infile'] = True
            self._mysql = mysql.connector.connect(**conn_params)
            self._cursor = self._mysql.cursor()
            log.info("MySQL connected successfuly")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                log.error("Something wrong with your user name or password. "
                          "Change settings or create a new user.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                log.error("Database '%s' does not exists. "
                          "Change settings or try to run with initdb key." % conn_params['database'])
            else:
                log.error("MySQL error:%s" % err)
        else:
            return True

    def _disconnector(self):
        """
        Drops MySQL connection
        :return: True
        """
        if self._mysql:
            self._cursor.close()
            self._mysql.disconnect()
            self._mysql.close()
            log.info("MySQL disconnected")
        return True

    def _mysql_pipe(mtd):
        """
        MySQL connection decorator for convenience.
        """
        @wraps(mtd)
        def _mysql_conn(self, *args, **kwargs):
            _res = False
            if self._connector():
                _res = mtd(self, *args, **kwargs)
                self._disconnector()
            return _res
        return _mysql_conn

    @_mysql_pipe
    def get_last(self):
        """
        Gets last update file time and update permission status for each object in array.
        :param gl_obj: a single object in case we need to check it.
        :return: True/False depending on job success.
        """
        result = False
        obj_array = self.db_array
        if obj_array:
            try:
                for obj in obj_array:
                    self._cursor.execute(obj.sql.get_info)
                    if self._cursor.with_rows:
                        row = dict(zip(self._cursor.column_names, self._cursor.fetchone()))
                        db_time = row['last_update']
                        db_upd = bool(row['enable_update'])
                        log.info("DB says that update for '%s' enabled status is: %s" % (obj.remote_dir,
                                                                                         db_upd))
                        obj.enabled = db_upd
                        if db_upd:
                            if not (obj.last_update_file_time and obj.last_update_file_time > db_time):
                                obj.last_update_file_time = db_time
                                log.info("    Using last time for '%s' from db:%i" % (obj.remote_dir,
                                                                                      db_time))
                result = True
            except StandardError as err:
                result = False
                log.error("Error in get_last data from DB:%s" % err)
        return result

    @_mysql_pipe
    def update(self):
        """
        This one doing main job related to update data in database.
        Firstly, it creates temporary table and uploads csv file contents in it.
        Then it makes some integrity checks and if succeeded moves data to production tables,
        otherwise, returns number of found errors.
        :param u_obj: a single object in case we need to process it.
        :return: True/False depending on job success.
        """
        obj_array = self.db_array
        if obj_array:
            for obj in obj_array:
                if obj.enabled and obj.files:
                    for sfile in obj.files:
                        log.info("MySQL. Processing file '%s'." % sfile[0])
                        err_in_file = False
                        source = self.config.main['local_dir'] + sfile[0]
                        try:
                            for recset in self._cursor.execute(obj.sql.update.format(fst=source,
                                                                                     snd=sfile[0],
                                                                                     frd=sfile[1]
                                                                                     ), multi=True):
                                if recset.with_rows:
                                    log.error("MySQL. Found next errors in '{0}':"
                                              .format(sfile[0]))
                                    for row in recset.fetchall():
                                        for col in row:
                                            log.error(u'\t{0}'.format(col))
                                    err_in_file = True
                                else:
                                    log.debug("MySQL. Number of rows affected by statement '{0}': {1}"
                                              .format(recset.statement, recset.rowcount))
                        except mysql.connector.Error or StandardError as err:
                            log.error("Error while updating db from file '%s':%s" % (sfile[0], err))
                            # self._mysql.rollback()
                        finally:
                            self._mysql.commit()
                        if not err_in_file:
                            os.remove(source)
                            log.info("MySQL. Done with '%s'. File deleted." % sfile[0])
                    del obj.files[0:len(obj.files)]
        return True
