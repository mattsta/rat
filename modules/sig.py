def run(flat, sections, mode):
    result = {}
    signal = flat['signal']
    name = flat['signalName']

    # If we failed an assert(), Redis automatically killed itself.
    if flat['softwareError']:
        return

    if signal:
        result['killed by'] = (signal, name)

        if signal is 11:
            result['crashed because'] = "memory access error"

        if signal is 9:
            result['crashed because'] = "directly killed by another process"

    return result
