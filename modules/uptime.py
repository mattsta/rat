def run(flat, sections, mode):
    uptime = flat['uptime_in_seconds']

    # arbitrary gauge of server "newness"
    if uptime < 300:
        return "server is less than five minutes old"
