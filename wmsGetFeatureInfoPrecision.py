# -*- coding: utf-8 -*-

"""
***************************************************************************
    wmsGetFeatureInfoPrecision.py
    ---------------------
    Date                 : April 2016
    Copyright            : (C) 2016 by René-Luc D'Hont - 3Liz
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
__copyright__ = '(C) 2016, DHONT René-Luc - 3Liz'

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.server import *

import os.path
import ConfigParser

FI_POINT_TOLERANCE = 16
FI_LINE_TOLERANCE = 8
FI_POLYGON_TOLERANCE = 4

class ServerGetFeatureInfoPrecisionFilter(QgsServerFilter):

    def requestReady(self):
        request = self.serverInterface().requestHandler()
        params = request.parameterMap( )
        if params.get('SERVICE', '').lower() == 'wms' \
                and params.get('REQUEST', '').lower() == 'getfeatureinfo':
            # Test config file
            if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.cfg')):
                config = ConfigParser.ConfigParser()
                config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.cfg'))

                pointTolerance = config.get('default','FI_POINT_TOLERANCE',str(FI_POINT_TOLERANCE))
                request.setParameter('FI_POINT_TOLERANCE', str(pointTolerance))

                lineTolerance = config.get('default', 'FI_LINE_TOLERANCE', str(FI_LINE_TOLERANCE))
                request.setParameter('FI_LINE_TOLERANCE', str(lineTolerance))

                polygonTolerance = config.get('default', 'FI_POLYGON_TOLERANCE', str(FI_POLYGON_TOLERANCE))
                request.setParameter('FI_POLYGON_TOLERANCE', str(polygonTolerance))
            else:
                request.setParameter('FI_POINT_TOLERANCE', str(FI_POINT_TOLERANCE))
                request.setParameter('FI_LINE_TOLERANCE', str(FI_LINE_TOLERANCE))
                request.setParameter('FI_POLYGON_TOLERANCE', str(FI_POLYGON_TOLERANCE))



class ServerGetFeatureInfoPrecision:
    """Plugin for QGIS server"""

    def __init__(self, serverIface):
        # Save reference to the QGIS server interface
        self.serverIface = serverIface
        try:
            self.serverIface.registerFilter(ServerGetFeatureInfoPrecisionFilter(serverIface), 1000)
        except Exception, e:
            QgsLogger.debug("ServerGetFeatureInfoPrecision- Error loading filter %s", e)



class GetFeatureInfoPrecision:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()


    def initGui(self):
        # Create action that will start plugin
        self.action = QAction(QIcon(":/plugins/"), "About Server GetFeatureInfoPrecision", self.iface.mainWindow())
        # Add toolbar button and menu item
        self.iface.addPluginToMenu("Server GetFeatureInfoPrecision", self.action)
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("activated()"), self.about)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("Server GetFeatureInfoPrecision", self.action)

    # run
    def about(self):
        QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('GetFeatureInfoPrecision', "Server GetFeatureInfoPrecision"), QCoreApplication.translate('GetFeatureInfoPrecision', "Server GetFeatureInfoPrecision is a simple plugin for QGIS Server, it does just nothing in QGIS Desktop. See: <a href=\"https://github.com/3liz/qgis-wmsGetFeatureInfoPrecision\">plugin's homepage</a>"))



if __name__ == "__main__":
    pass
