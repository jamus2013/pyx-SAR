%% mLRS RADIO RANGE TEST POST-PROCESSOR
% Parses ArduPlane FCU logs and exports RF signal metrics
% Instructions:
%   1. Run radio test
%   2. Download DataFlash Log (*.bin) using GCS software (or pull from FCU MicroSD card)
%   3. Generate *.mat file from *.bin using Mission Planner
%   4. Update timezone ("utc_offset")
%   5. Insert LLA of stationary GCS
%   6. Set export flag to 1 if ready to generate output *csv's
%   7. Set plot flag to 1 to draw figures
%   8. Run this script and import *.mat file

% User variables
%fcu_log_path      = "2025-02-05 16-33-27.bin-969641.mat"; % FCU log filepath [*.mat] COMPILE from *.bin using Mision Planner
clc;
clear all;
[f, p]            = uigetfile('*.mat', 'Select FCU log MAT file');
utc_offset        = -6;  % Timezone offset from UTC to local (-6=CST)
gcs_location      = [34.72714, -86.55389, 247]; % LLA of GCS location (Altitude = m HAE)
export_true       = 0;  % Set to 1 to export CSV files
plot_true         = 1;  % Set to 1 to plot data

fcu_gps_output_filename   = [p "fcu_gps_data.csv"];  %CSV Export filenames
fcu_tm_output_filename    = [p "fcu_tm_metrics.csv"];
fcu_rc_output_filename    = [p "fcu_rc_metrics.csv"];

%% SCRIPT
disp("Importing FCU log");  % Import FCU log
fcu_log_path = [p f];
load(fcu_log_path);
disp("Parsing GPS data...");

% Parse FCU GPS log data
gps_dt            = GPS_1(:,2)/1e6; % Get delta t from power up [s]
gps_ms            = GPS_1(:,5);   % Get GPS clock milliseconds
gps_wk            = GPS_1(:,6);   % Get GPS clock weekday
gps_lat           = GPS_1(:,9);   % GPS latitude [deg N WGS84]
gps_lon           = GPS_1(:,10);  % GPS longitude [deg E WGS84]
gps_alt           = GPS_1(:,11);  % GPS altitude
gps_time          = gps2local(gps_wk, gps_ms, utc_offset,0);
for i = 1:length(gps_lat)
  % Calculate distance from GCS
  [d, ~]        = latLong2DistBear(gcs_location(1),gcs_location(2),...
                    gps_lat(i),gps_lon(i),"km");
  dh            = gps_alt(i) - gcs_location(3);   % Altitude delta [m]
  range(i,1)    = sqrt(d^2 + (dh/1000)^2);        % 3D range [km]
end
N_gps             = length(gps_time); % Get GPS number of samples

% Calculate log time start
disp("Calculating time sync...");
log_start_time    = gps2local(gps_wk(1), gps_ms(1), utc_offset, 0);       % Local time stamp for log start
dt_boot_log       = GPS_1(1,2)/10e6;                                      % Time between power up and log start [s]
powerup_time      = gps2local(gps_wk(1), gps_ms(1), utc_offset, -dt_boot_log);
fprintf("Power up time: %s\n", powerup_time);
fprintf("FCU Log start time: %s\n", log_start_time);

% Parse FCU telemetry metrics
disp("Parsing TM data...");
tm_dt             = RAD(:,2)/1e6;  % Get delta t from power up [s]
N_tm              = length(tm_dt);  % Get number of TM samples
for i = 1:N_tm
  tm_time{i}      = adjust_datetime(powerup_time, tm_dt(i));  % Generate TM time vector
end
tm_rssi_local     = RAD(:,3);       % Get local TM radio RSSI
tm_rssi_remote    = RAD(:,4);       % Get remote TM radio RSSI
tm_noise_local    = RAD(:,6);       % Get local TM noise floor
tm_noise_remote   = RAD(:,7);       % Get remote TM noise floor
tm_rx_err         = RAD(:,8);       % Get number of dropped TM packets

% Parse FCU RC metrics
disp("Parsing RC data...");
rc_dt             = RSSI(:,2)/1e6; % Get delta t from power up [s]
N_rc              = length(rc_dt);  % Get number of RC samples
for i = 1:N_rc
  rc_time{i}      = adjust_datetime(powerup_time, rc_dt(i));  % Generate RC time vector
end
rc_rssi           = RSSI(:,3);      % Get C2 link RSSI
rc_lq             = RSSI(:,4);      % Get C2 link quality


%% EXPORT DATA                % NOTE: these could probably be a function but I'm in a hurry
if export_true == 1
  disp("Exporting parsed FCU GPS data...");
  % Write FCU GPS data
  headers   = {"GPS Time [s]", "GPS Time [CST]", "Latitude [deg N]", "Longitude [deg E]", "Range [km]"};
  fid       = fopen(fcu_gps_output_filename, "w");
  fprintf(fid, "%s,%s,%s,%s,%s\n", headers{:});
  for i = 1:length(gps_time)
    fprintf(fid, "%.8f,%s,%.8f,%.8f,%.8f\n", ...
    gps_dt(i), gps_time(i,:), gps_lat(i), gps_lon(i), range(i));
  end
  fclose(fid);
  disp("Export complete");

  % Write FCU TM data
  disp("Exporting parsed FCU TM RF data...");
  headers   = {"TM Time [s]","TM RSSI Local","TM RSSI Remote","TM Noise Local",...
              "TM Noise Remote","TM RX Errors"};
  fid       = fopen(fcu_tm_output_filename, "w");
  fprintf(fid, "%s,%s,%s,%s,%s,%s\n", headers{:});
  for i = 1:length(tm_dt)
    fprintf(fid, "%.8f,%.1f,%.1f,%.1f,%.1f,%d\n", ...
    tm_dt(i), tm_rssi_local(i), tm_rssi_remote(i), tm_noise_local(i), ...
    tm_noise_remote(i), tm_rx_err(i));
  end
  fclose(fid);
  disp("Export complete");

  % Write FCU RC data
  disp("Exporting parsed FCU RC RF data...");
  headers   = {"RC Time [s]", "RC RSSI", "RC LQ"};
  fid       = fopen(fcu_rc_output_filename, "w");
  fprintf(fid, "%s,%s,%s\n", headers{:});
  for i = 1:length(rc_dt)
    fprintf(fid, "%.8f,%.6f,%.1f\n",rc_dt(i), rc_rssi(i), rc_lq(i));
  end
  fclose(fid);
  disp("Export complete");
end

%% PLOT DATA
if plot_true == 1
  disp("Plotting data...");
  % RC RSSI vs Interpolated Range
  range_interp = interp1(gps_dt, range, rc_dt, 'linear', 'extrap'); % 'linear' interpolation
  figure
  p1 = subplot(2,1,1);
  plot(range_interp, rc_rssi,'.');
  title('RC datalink Quality');
  xlabel('Range [km]');
  ylabel('RC RSSI [%]');
  grid on;
  p2 = subplot(2,1,2);
  plot(range_interp, rc_lq/100,'.');
  xlabel('Range [km]');
  ylabel('RC Link Quality [%]');
  grid on;
end



