# If this module is too noisy, we can restrict the output only to
# "info" mode instead of every mode.
def run(flat, sections, mode):
    result = {}
    keys = flat['cmdstat_keys']
    cs = sections['Commandstats']
    bu = "BAD USAGE"
    result[bu] = {}
    bad = result[bu]

    if not cs:
        return

    def es(x):
        if x > 1 or x == 0:
            return "s"
        else:
            return ""

    if keys:
        bad["KEYS command used"] = "{:,d} times".format(keys['calls'])

    usage = []
    sortedByUsage = sorted(cs, key=lambda key: cs[key]['calls'], reverse=True)
    for key in sortedByUsage:
        [_, cmd] = key.split("_")
        usage.append({cmd: "{:,d} times".format(cs[key]['calls'])})

    result['sorted by calls'] = usage

    totalTimeUs = 0L
    for _,v in cs.iteritems():
        totalTimeUs = totalTimeUs + v['usec']

    duration = []
    sortedByDuration = sorted(cs, key=lambda key: cs[key]['usec'], reverse=True)
    for key in sortedByDuration:
        [_, cmd] = key.split("_")
        usTotal = float(cs[key]['usec'])

        # the amount of variable reuse below is pretty inexcusable
        sec, us = divmod(usTotal, 1e6)
        ms, us = divmod(us, 1e3)
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        if h:
            hms = "%d hour%s, %d minute%s, %d second%s" % \
                (h, es(h), m, es(m), s, es(s))
        elif m:
            hms = "%d minute%s, %d second%s" % (m, es(m), s, es(s))
        elif s:
            hms = "%d second%s, %d ms, %d us" % (s, es(s), ms, us)
        elif ms:
            hms = "%d ms, %d us" % (ms, us)
        elif us:
            hms = "%d us" % (us)

        duration.append({cmd:
                         {'total': hms,
                          'runtime': "%.1f%%" % (usTotal/totalTimeUs * 100)}})

    if duration:
        result['sorted by duration'] = duration

    if not result[bu]:
        del result[bu]

    return result
