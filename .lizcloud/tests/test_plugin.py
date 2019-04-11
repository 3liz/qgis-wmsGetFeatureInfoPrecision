import sys
import os
import lxml.etree
import logging

from pathlib import Path

from qgis.core import Qgis, QgsProject
from qgis.server import (QgsBufferServerRequest,
                         QgsBufferServerResponse)



def test_plugin_config(client):

    plugin = client.getplugin('wmsGetFeatureInfoPrecision')
    assert plugin is not None

    # Create a filter instance
    pluginfilter = plugin.create_filter()

    # Check we have a default config
    config = pluginfilter.get_config()
    assert config is not None
    assert config.get('default','FI_POINT_TOLERANCE') == '25'
    assert config.get('default', 'FI_LINE_TOLERANCE') == '10'
    assert config.get('default', 'FI_POLYGON_TOLERANCE') == '5'

    #project = QgsProject()
    #project.setFileName(client.getprojectpath("france_parts.qgs").strpath)

    # Check we load the default config
    configpath = Path(client.getprojectpath("france_parts.qgs")).parent / 'idonotexists.cfg'
    config = pluginfilter.get_config(configpath)
    assert config is not None
    
    # Check we load the project config
    configpath = Path(client.getprojectpath("france_parts.qgs")).parent / 'featureInfoPrecision.cfg'
    config = pluginfilter.get_config(configpath)
    assert config is not None
    assert config.get('default','FI_POINT_TOLERANCE') == '24'
 


def test_wms_request(client):

    qs = "?MAP=france_parts.qgs&SERVICE=WMS&REQUEST=GetFeatureInfo&QUERY_LAYERS=france_parts"
    rv = client.get(qs,'france_parts.qgs')

    #if rv.status_code != 200:
    #    logging.error(lxml.etree.tostring(rv.xml, pretty_print=True))

    #assert rv.status_code == 200

    params = rv.request.parameters()
    # Check that request contains added parameters
    assert params.get('FI_POINT_TOLERANCE') == '24' 
    assert params.get('FI_LINE_TOLERANCE') == '10' 
    assert params.get('FI_POLYGON_TOLERANCE') == '5' 



