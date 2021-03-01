# NL hoogtekaart

This directory provides a library to read the dutch heightmap. View main.py for its use.

You can download the .TIF files using the supplied script: download_ahn3.py. Or you can download the .TIF files from a repo and place them into the folder ./AHN3_data.

The georeferencing data can be obtained through this api call: https://geodata.nationaalgeoregister.nl/ahn3/wfs?service=WFS&request=getFeature&version=2.0.0&typeNames=ahn3_bladindex&outputFormat=application/json
