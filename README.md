# pyx-SAR
Integrating Pixhawk-based robotic systems into CalTopo

Features Python scripts to broadcast MAVLink locations to CalTopo API endpoint

INSTRUCTIONS
1. Clone repo (or just download base-station-service)
2. Install Python and dependencies (will eventually be packaged)
3. Populate "key" variable with your CalTopo URL key 
4. Populate "device_id" variable with your CalTopo device ID
5. Create CalTopo map and enable Realtime Data > Shared Locations > [All] or [your team]
6. Connect GCS to your CalTopo network (local or internet)
7. Connect aircraft to GCS using wireless modem
8. Start base-station-service and verify connection
9. [OPTIONAL] Click on CalTopo live track when it appears and select "Record to Map"
