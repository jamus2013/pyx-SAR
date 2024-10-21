# pyx-SAR
Integrating Pixhawk-based robotic systems into CalTopo

Converts plan file from QGC into CalTopo shape file

INSTRUCTIONS
1. Clone repo
2. Install Python and dependencies (will eventually be packaged)
3. Save mission file from QGC 
4. Run qgc-plan-converter
5. Import QGC mission file
6. Open CalTopo map
7. Import geoJSON just created
8. Select layers to import (geofence, waypoints, and/or rally points)
