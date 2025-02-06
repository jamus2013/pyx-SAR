% Created by Jamie Moon
function [d, theta] = latLong2DistBear(lat1,long1,lat2,long2,unit)
    % ESTIMATES DISTANCE AND HEADING BETWEEN 2 GPS COORDINATES
    % [Remote,Local]
    % Inputs = Lat./Long. of Point 1 (origin), Lat./Long. of Point 2 (destination), unit string
    % Returns relative distance of Point 1 relative to Point 2 [unit] and bearing [deg]
    R_e = 6.371e+6; % Earth's radius [m]
    lat1 = deg2rad(lat1); lat2 = deg2rad(lat2); % Convert angular units
    long1 = deg2rad(long1); long2 = deg2rad(long2);
    d = 2*R_e*asin(sqrt(sin((lat1 - lat2)/2)^2 ...    % Compute haversine distance
        + cos(lat1)*cos(lat2)*sin((long2 - long1)/2)^2));
    if unit == 'km'
        d = d/1000; % Kilometer
    elseif unit == 'ft'
        d = d*0.3048;   % Feet
    end
    X = cos(lat2)*sin(long2 - long1);
    Y = sin(lat2)*cos(lat1) - sin(lat1)*cos(lat2)*cos(long2 - long1);
    theta = rad2deg(atan2(X,Y));
end