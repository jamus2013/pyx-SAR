# pyx-SAR
Integrating Pixhawk-based robotic systems into CalTopo

Features Python scripts to broadcast MAVLink locations to CalTopo API endpoint

INSTRUCTIONS
1. Clone repo
2. Install Python and dependencies (will eventually be packaged)
3. Set up QGC
    - Verify autoconnect to SiK radio is disabled
4. Plug in SiK telemetry radio (USB)
5. Power up aircraft; verify GPS fix
6. Run telem-router in dedicated terminal
7. Verify connection on QGC (over modem)
8. Run gps-relay.py
9. Enter your device's ID name for CalTopo
10. Enter your CalTopo URL Key (from admin)
11. Verify location is being broadcast
12. Open CalTopo map; enable Realtime Data > Shared Locations > [All] or [your team]
13. [OPTIONAL] Click on CalTopo live track when it appears and select "Record to Map"
