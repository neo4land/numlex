# -*- coding: utf8 -*-
import ConfigParser
import logging
log = logging.getLogger(__name__)

__author__ = "Stinger <neo4land@gmail.com>"
__license__ = "GNU Lesser General Public License (LGPL)"


class MyDict(dict):
    def __init__(self, parent, name, seq, **kwargs):
        self.name = name
        self.parent = parent
        seq = [(y, int(x)) if str(x).isdigit() else (y, x) for y, x in seq]
        super(MyDict, self).__init__(seq, **kwargs)

    def __setitem__(self, key, value):
        if key not in ['allow_local_infile','sql_mode','client_flags']:
            self.parent.cp.set(self.name, key, value)
            self.parent.save_config()
        super(MyDict, self).__setitem__(key, value)

    def __getitem__(self, item):
        return super(MyDict, self).__getitem__(item)


class Settings(object):
    def __init__(self, cfile='settings.cfg'):
        self.cp = ConfigParser.RawConfigParser()
        self.__config_file = cfile
        self.__config_default = \
            {
                'MYSQL':
                {
                    'user': 'your_mysql_user',
                    'password': 'your_mysql_pass',
                    'host': '127.0.0.1',
                    'database': 'BDPN',
                    'connection_timeout': '600'
                },
                'SFTP':
                {
                    'host': 'prod-sftp.numlex.ru',
                    'user': 'your_numlex_user',
                    'secret': 'your_numlex_pass',
                    'port': '3232'
                },
                'MAIN':
                {
                    'local_dir': '/tmp/',
                    'log_file': '/var/log/bdpnsync.log',
                    'log_level': 40,
                    'sync_every_minutes': 120  # Timer step - every even hour
                }
            }
        self._config_cache = {}
        self.load_config()
        handler = logging.FileHandler(self.main['log_file'], 'a')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        handler.setLevel(self.main['log_level'])
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(self.main['log_level'])

    def load_config(self):
        """This loads configuration file if one exist or uses default settings otherwise."""
        for section in self.cp.sections():
            self.cp.remove_section(section)
        if not self.cp.read(self.__config_file):
            log.warning("Settings file '%s' was not found! Creating one with defaults..." % self.__config_file)
            self.__create_default()
        if self.__check_config():
            for section_name in self.cp.sections():
                setattr(self, section_name.lower(), MyDict(self, section_name, self.cp.items(section_name)))
        else:
            return False
        return True

    def __check_config(self):
        """Checks if current configuration file has all settings we need."""
        for section_name in self.__config_default:
            if self.cp.has_section(section_name):
                if not sorted(self.cp.options(section_name)) == sorted(self.__config_default[section_name].keys()):
                    log.critical('Options in section %s are not complete.' % section_name)
                    raise RuntimeError('Options in section %s are not complete.' % section_name)
            else:
                log.critical('There is no section %s in settings file.' % section_name)
                raise RuntimeError('There is no section %s in settings file.' % section_name)
        return True

    def __create_default(self):
        """Creates default configuration file."""
        for section_name in self.__config_default:
            self.cp.add_section(section_name)
            for name, value in self.__config_default[section_name].items():
                self.cp.set(section_name, name, value)
        self.save_config()

    def save_config(self):
        """Saves configuration to file."""
        log.debug("Saving settings to:%s" % self.__config_file)
        with open(self.__config_file, 'wb') as configfile:
            self.cp.write(configfile)
