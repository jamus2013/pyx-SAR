def get_system_time():
    # CREATE TIME STAMP BASED ON LOCAL SYSTEM TIME
    import datetime
    sys_time = datetime.datetime.now()
    return sys_time.strftime("%Y-%m-%d %H:%M:%S")