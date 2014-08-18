def run(flat, sections, mode):
    forkTime = flat['latest_fork_usec']

    if isinstance(forkTime, str):
        return

    # 10e5 = 100ms
    if forkTime > 10e5:
        return {"fork time very large": "%.4f seconds" % (forkTime/10e6)}
