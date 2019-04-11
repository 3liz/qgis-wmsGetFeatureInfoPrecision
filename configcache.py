"""
***************************************************************************
    wmsGetFeatureInfoPrecision.py
    ---------------------
    Date                 : April 2019
    Copyright            : (C) 2016 by René-Luc D'Hont - 3Liz
                           (C) 2019 by David Marteau - 3Liz
    Email                : rldhont at 3liz dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
from pathlib import Path
from datetime import datetime
from configparser import ConfigParser
from collections import namedtuple, OrderedDict

from qgis.core import Qgis, QgsMessageLog

_CacheEntry = namedtuple("_CacheEntry",('config','timestamp'))

class ConfigCache:

    def __init__(self, capacity: int=10, default: Path=None) -> None:
        self._table = OrderedDict()
        self._capacity = capacity
        self._default  = default

        self.__getitem__(self._default)

    @property
    def defaultconfig(self) -> Path:
        return self._default

    def _get(self, key: Path) -> ConfigParser:
        """ Look up config

            Act as a LRU cache
            Update cache by comparing modification time
        """
        try:
            timestamp = datetime.fromtimestamp(key.stat().st_mtime)
        except FileNotFoundError:
            return None

        details = self._table.get(key)
        if details is not None:
            # Compare mtime
            if details.timestamp < timestamp:
                del self._table[key]
            else:
                # Found a valid entry
                self._table.move_to_end(key)
                return details.config
        try:
            # (re)create cache entry
            config = ConfigParser()
            config.read(str(key))
            while len(self._table) >= self._capacity:
                self._table.popitem(last=False)
       
            QgsMessageLog.logMessage('Loaded config file %s' % key,'wmsGetFeatureInfoPrecision',Qgis.Info)
            self._table[key] = _CacheEntry(config,timestamp)
            return config
        except Exception as e:
            QgsMessageLog.logMessage('Error reading config file %s' % key,'wmsGetFeatureInfoPrecision',Qgis.Critical)
            return None

    def __getitem__(self, key: Path) -> ConfigParser:
        """ Return default value if key is not found
        """
        cfg = self._get(key)
        if cfg is None:
            cfg = self._get(self._default)
        return cfg


