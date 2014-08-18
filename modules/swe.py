def run(flat, sections, mode):
    softwareError = flat['softwareError']

    if softwareError:
        return {"software error": softwareError}
