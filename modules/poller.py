def run(flat, sections, mode):
    result = {}
    poll = flat['multiplexing_api']

    if poll == "select":
        result['using inefficient multiplexer'] = poll

    return result
