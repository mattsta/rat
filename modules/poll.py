def run(flat, sections, mode):
    poll = flat['multiplexing_api']

    if poll == 'select':
        return {'non-optimized event system': poll}
