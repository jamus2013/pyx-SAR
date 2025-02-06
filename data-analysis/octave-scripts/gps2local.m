function local_time = gps2local(week, milliseconds, utc_offset, sec_offset)
    % Converts GPS Week and Milliseconds to local time
    gps_epoch = datenum(1980, 1, 6, 0, 0, 0); % GPS epoch
    gps_seconds = week * 604800 + milliseconds / 1000 + sec_offset; % Total seconds from GPS epoch
    
    % Convert to UTC datetime
    utc_time = gps_epoch + gps_seconds / 86400; % Convert seconds to days
    
    % Apply UTC offset for local time (e.g., UTC-6 for CST)
    local_time = addtodate(utc_time, utc_offset, 'hour');
    
    % Convert to readable format
    local_time = datestr(local_time, 'yyyy-mm-dd HH:MM:SS.FFF');
end