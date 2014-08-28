def run(flat, sections, mode):
    result = {}
    changes = flat['rdb_changes_since_last_save']
    lastStatus = flat['rdb_last_bgsave_status']
    lastSaveDuration = flat['rdb_last_bgsave_time_sec']

    if not sections['Persistence']:
        return

    def toTime(sec):
        def es(x):
            if x > 1 or x == 0:
                return "s"
            else:
                return ""

        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        if h:
            hms = "%d hour%s, %d minute%s, %d second%s" % \
                (h, es(h), m, es(m), s, es(s))
        elif m:
            hms = "%d minute%s, %d second%s" % (m, es(m), s, es(s))
        elif s:
            hms = "%d second%s" % (s, es(s))

        return hms

    def toTimeAgo(sec):
        return toTime(sec) + " ago"

    if changes:
        result['changes not written yet'] = "{:,d}".format(changes)

    if flat['rdb_bgsave_in_progress']:
        result['currently saving'] = True
        saveSec = flat['rdb_current_bgsave_time_sec']
        if saveSec:
            result['current save started'] = toTimeAgo(saveSec)

    if lastStatus != "ok":
        result['last save not ok'] = lastStatus

    if lastSaveDuration and lastSaveDuration != -1:
        result['last save duration'] = toTime(lastSaveDuration)
    elif lastSaveDuration == -1:
        result['never wrote snapshot'] = True

    return result
