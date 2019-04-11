"""
***************************************************************************
    wmsGetFeatureInfoPrecision.py
    ---------------------
    Date                 : April 2016
    Copyright            : (C) 2016 by René-Luc D'Hont - 3Liz
                         : (C) 2019 by David Marteau - 3liz
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

__author__ = 'DHONT René-Luc'
__date__ = 'April 2016'
__copyright__ = '(C) 2016-2019, DHONT René-Luc - 3Liz'

# Import the PyQt and QGIS libraries
from qgis.core import Qgis, QgsMessageLog
from qgis.server import QgsServerFilter
from qgis.PyQt.QtCore import QCoreApplication, QObject
from qgis.PyQt.QtWidgets import QAction, QMessageBox

from pathlib import Path
from .configcache import ConfigCache

FI_POINT_TOLERANCE = 16
FI_LINE_TOLERANCE = 8
FI_POLYGON_TOLERANCE = 4

class ServerGetFeatureInfoPrecisionFilter(QgsServerFilter):

    def __init__(self, serverIface: 'QgsServerInterface') -> None:
        super().__init__(serverIface)

        # Set default configuration
        defaultcfg = Path(__file__).resolve().parent / 'config.cfg'
        self._cache = ConfigCache(default=defaultcfg)

    def get_config(self, configpath: Path = None) -> 'ConfigParser':
        """ Return configuration
        """
        return self._cache[configpath or self._cache.defaultconfig]

    def requestReady(self) -> None:
        request = self.serverInterface().requestHandler()
        params = request.parameterMap( )
        if params.get('SERVICE', '').lower() == 'wms' \
            and params.get('REQUEST', '').lower() == 'getfeatureinfo':

            # Test config file in project path
            configpath = Path(self.serverInterface().configFilePath()).parent / 'featureInfoPrecision.cfg'
            config = self._cache[configpath]
            if config:
                pointTolerance = config.get('default','FI_POINT_TOLERANCE', fallback=str(FI_POINT_TOLERANCE))
                request.setParameter('FI_POINT_TOLERANCE', pointTolerance)

                lineTolerance = config.get('default', 'FI_LINE_TOLERANCE', fallback=str(FI_LINE_TOLERANCE))
                request.setParameter('FI_LINE_TOLERANCE', lineTolerance)

                polygonTolerance = config.get('default', 'FI_POLYGON_TOLERANCE', fallback=str(FI_POLYGON_TOLERANCE))
                request.setParameter('FI_POLYGON_TOLERANCE', polygonTolerance)
            else:
                request.setParameter('FI_POINT_TOLERANCE'  , str(FI_POINT_TOLERANCE))
                request.setParameter('FI_LINE_TOLERANCE'   , str(FI_LINE_TOLERANCE))
                request.setParameter('FI_POLYGON_TOLERANCE', str(FI_POLYGON_TOLERANCE))



class ServerGetFeatureInfoPrecision:
    """Plugin for QGIS server"""

    def __init__(self, serverIface: 'QgsServerInterface') -> None:
        # Save reference to the QGIS server interface
        self.serverIface = serverIface
        self.serverIface.registerFilter(ServerGetFeatureInfoPrecisionFilter(serverIface), 1000)

    def create_filter(self) -> ServerGetFeatureInfoPrecisionFilter:
        """ Create a new filter instance - Used for tests
        """
        return ServerGetFeatureInfoPrecisionFilter(self.serverIface)


class GetFeatureInfoPrecision:
    def __init__(self, iface: 'QgsInterface') -> None:
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()


    def initGui(self) -> None:
        # Create action that will start plugin
        self.action = QAction(QIcon(":/plugins/"), "About Server GetFeatureInfoPrecision", self.iface.mainWindow())
        # Add toolbar button and menu item
        self.iface.addPluginToMenu("Server GetFeatureInfoPrecision", self.action)
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("activated()"), self.about)

    def unload(self) -> None:
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("Server GetFeatureInfoPrecision", self.action)

    # run
    def about(self) -> None:
        QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('GetFeatureInfoPrecision', "Server GetFeatureInfoPrecision"), QCoreApplication.translate('GetFeatureInfoPrecision', "Server GetFeatureInfoPrecision is a simple plugin for QGIS Server, it does just nothing in QGIS Desktop. See: <a href=\"https://github.com/3liz/qgis-wmsGetFeatureInfoPrecision\">plugin's homepage</a>"))


