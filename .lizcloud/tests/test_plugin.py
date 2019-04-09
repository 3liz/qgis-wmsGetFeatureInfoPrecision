import sys
import os

from qgis.core import Qgis, QgsProject
from qgis.server import (QgsBufferServerRequest,
                         QgsBufferServerResponse)



def test_plugin(client):

    plugin = client.getplugin('wmsGetFeatureInfoPrecision')
    assert plugin is not None



