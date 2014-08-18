def run(flat, sections, mode):
    result = {}
    totalCxns = flat['total_connections_received']
    totalCmds = flat['total_commands_processed']
    uptime = flat['uptime_in_seconds']
    evicted = flat['evicted_keys']
    hits = flat['keyspace_hits']
    misses = flat['keyspace_misses']

    if not sections['Stats']:
        return

    if uptime > 1:
        if totalCmds:
            result['total commands processed'] = "{:,d}".format(totalCmds)
        else:
            result['no commands processed'] = True
        perSecond = int(float(totalCmds)/uptime)
        if perSecond:
            result['average commands per second'] = perSecond

    if evicted:
        result['evicted key count'] = evicted

    if hits and misses:
        missRatio = float(misses)/(hits + misses)
        if missRatio > 0.10:
            result['high key miss rate'] = True
            missRate = missRatio * 100
            result['key miss percentage'] = "%d%%"  % (int(missRate))

    return result
