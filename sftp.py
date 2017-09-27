# -*- coding: utf8 -*-
import os
import paramiko
from zipfile import ZipFile
from functools import wraps
import logging
log = logging.getLogger(__name__)

__author__ = "Stinger <neo3land@gmail.com>"
__license__ = "GNU Lesser General Public License (LGPL)"


class SftpChannel(object):
    def __init__(self, db_array=None, config=None):
        self._sftp = None
        self.db_array = db_array
        self.config = config

    def _create_sftp_pipe(mtd):
        """
        This decorator takes care on sftp connection.
        """
        @wraps(mtd)
        def _sftp_connection(self, *args, **kwargs):
            xssh = paramiko.SSHClient()
            xssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            _res = False
            try:
                log.debug("Trying to connect to SFTP server")
                xssh.connect(self.config.sftp['host'],
                             username=self.config.sftp['user'],
                             password=self.config.sftp['secret'],
                             port=self.config.sftp['port'],
                             timeout=10)
                self._sftp = xssh.open_sftp()
                log.debug("Sftp Connected!")
                _res = mtd(self, *args, **kwargs)
            except paramiko.ChannelException as err:
                log.warning("Sftp channel error (%s)" % err)
            except paramiko.SSHException as err:
                log.error("Sftp Connection Error (%s)" % err)
                raise RuntimeError("Sftp Connection Error (%s)" % err)
            finally:
                self._sftp.close()
                xssh.close()
                log.info("Sftp Disonnected.")
            return _res
        return _sftp_connection

    @_create_sftp_pipe
    def _download(self):
        """Download files from SFTP server"""
        def _copy(what=None, where=None, cobj=None):
            if what and where and cobj:
                if not os.path.exists(where):
                    os.makedirs(where)
                where = where + what
                what = cobj.remote_dir + what
                log.debug("Downloading %s to %s" % (what, where))
                self._sftp.get(what, where)
                return True
            else:
                log.error("Nothing to copy! Include file name please!")
                raise ValueError("Nothing to copy! Include file name please!")

        try:
            log.info("Sftp. Searching for new files to update.")
            for dwnl_obj in self.db_array:
                if dwnl_obj.enabled:
                    del dwnl_obj.files[0:len(dwnl_obj.files)]     # .clear() py v3+
                    log.debug("Cheking for new files in %s" % dwnl_obj.remote_dir)
                    files_array = sorted(self._sftp.listdir_attr(path=dwnl_obj.remote_dir),
                                         key=lambda x: x.st_mtime,
                                         reverse=True)
                    if files_array:
                        if dwnl_obj.newest_only:
                            files_array = [files_array[0]]
                        if dwnl_obj.last_update_file_time:
                            files_array = list(filter(lambda y: y.st_mtime > dwnl_obj.last_update_file_time,
                                                      files_array))
                        if files_array:
                            for afile in files_array:
                                if _copy(afile.filename, self.config.main['local_dir'], dwnl_obj):
                                    dwnl_obj.files.append((afile.filename, afile.st_mtime))
                        else:
                            log.info("No fresh updates in %s" % dwnl_obj.remote_dir)
                if dwnl_obj.files:
                    dwnl_obj.last_update_file_time = dwnl_obj.files[0][1]
                    dwnl_obj.files.reverse()
            _res = True
        except StandardError as err:
            _res = False
            log.error("Error in downloading process:%s" % err)
        return _res

    def _unpack(self):
        """
        This one unpack zipped archives and delete source files.
        :return: True/False depending on job success.
        """
        def _unzip(src=None, dst=None):
            if src and dst:
                zip_ref = ZipFile(source, "r")
                ziped = zip_ref.namelist()[0]
                zip_ref.extract(ziped, dst)
                zip_ref.close()
                os.remove(src)
                log.debug("%s Unpacked. %s deleted" % (ziped, src))
                return ziped
            else:
                log.error("Error in unpacking")
                raise RuntimeError("Error in unpacking")
        try:
            for unpack_object in self.db_array:
                destination = self.config.main['local_dir']
                for index, sfile in enumerate(unpack_object.files):
                    source = destination + sfile[0]
                    unpack_object.files[index] = (_unzip(source, destination), sfile[1])
            return True
        except StandardError as err:
            log.error("Error in Unpacking process:%s" % err)
            return False

    def synchronize(self):
        """Makes the whole file synchronisation job"""
        return self._download() and self._unpack()
