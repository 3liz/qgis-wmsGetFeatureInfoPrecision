# -*- coding: utf-8 -*-
"""
 This script initializes the plugin, making it known to QGIS.
"""


def serverClassFactory(serverIface):
    from wmsGetFeatureInfoPrecision import ServerGetFeatureInfoPrecision
    return ServerGetFeatureInfoPrecision(serverIface)

def classFactory(iface):
    from wmsGetFeatureInfoPrecision import GetFeatureInfoPrecision
    return GetFeatureInfoPrecision(iface)

