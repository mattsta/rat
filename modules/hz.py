def run(flat, sections, mode):
    result = {}
    hz = flat['hz']

    if not hz:
        return

    if hz != 10:
        result['non standard hz'] = hz

    if not 10 <= hz <= 100:
        result['maybe improperly tuned hz'] = hz

    return result
