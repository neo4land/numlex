# -*- coding: utf8 -*-
import queries

__author__ = "Stinger <neo3land@gmail.com>"
__license__ = "GNU Lesser General Public License (LGPL)"


class NumlexBaseClass(object):
    """
    Representation of numlex csv files we need to process.
    """
    def __init__(self):
        self.remote_dir = '/numlex/'
        self.sql = queries.BDPNquery
        self.files = []
        self.enabled = True
        self.__last_update_file_time = None
        self.newest_only = True
        self._child_list = []

    @property
    def last_update_file_time(self):
        """This is last_update_file_time property."""
        return self.__last_update_file_time

    @last_update_file_time.setter
    def last_update_file_time(self, value):
        """
        This adds 15 minutes to each file time to ensure that it will not be used again.
        Also, this process depended objects.
        """
        if self._child_list:
            for child in self._child_list:
                if child != self:
                    # print("prop setter fired with %s" % value)
                    child.last_update_file_time = value
        self.__last_update_file_time = value + 900

    @last_update_file_time.deleter
    def last_update_file_time(self):
        self.__last_update_file_time = None


def make_obj_list():
    opers = NumlexBaseClass()
    opers.remote_dir = '/numlex/Operators/'
    opers.sql = queries.Operators

    nmbpl = NumlexBaseClass()
    nmbpl.remote_dir = '/numlex/Numbering_Plan/'
    nmbpl.sql = queries.NumberingPlan

    prtin = NumlexBaseClass()
    prtin.remote_dir = '/numlex/Port_Increment/'
    prtin.sql = queries.PortIncrement
    prtin.newest_only = False

    ptout = NumlexBaseClass()
    ptout.remote_dir = '/numlex/Return_Increment/'
    ptout.sql = queries.ReturnIncrement
    ptout.newest_only = False

    ptall = NumlexBaseClass()
    ptall.remote_dir = '/numlex/Port_All/'
    ptall.sql = queries.PortAll
    ptall._child_list = [ptout, prtin]

    return [opers, nmbpl, ptall, ptout, prtin]
