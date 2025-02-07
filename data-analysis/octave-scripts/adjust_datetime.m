function output = adjust_datetime(datetime_str, n_seconds)
  % Adds n_seconds to an existing date-time string
  main_part = datetime_str(1:19); % Everything up to seconds place
  if length(datetime_str) > 19
    ms_part = str2double(datetime_str(21:end)) / 1000; % Convert FFF to fraction of second
  else
    ms_part = 0;
  end
  datetime_num = datenum(main_part, 'yyyy-mm-dd HH:MM:SS');
  datetime_num = datetime_num + (n_seconds + ms_part) / 86400;  % Add seconds back into time

  new_main_part = datestr(datetime_num, 'yyyy-mm-dd HH:MM:SS');
  new_ms = mod(datetime_num * 86400, 1) * 1000;

  output = sprintf('%s.%03d', new_main_part, round(new_ms));  % Construct full precision string
  end
