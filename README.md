wmsGetFeatureInfoPrecision: QGIS Server Plugin to add precision parameters to WMS GetFeatureInfo request.
==========================================================================================================

Description
---------------

wmsGetFeatureInfoPrecision is a QGIS Server Plugin. It adds or overrides QGIS Server specific precision parameters.

The plugin can be configured with a config file set in the plugin directory. Create a `config.cfg` file with a `default` section.

config.cfg example file:
```
[default]
FI_POINT_TOLERANCE = 25
FI_LINE_TOLERANCE = 10
FI_POLYGON_TOLERANCE = 5
```

Use it for a non QGIS Server specific client.