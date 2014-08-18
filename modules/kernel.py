def run(flat, sections, mode):
    os = flat['os']

    if not os:
        return

    if not (os.startswith("Darwin") or os.startswith("Linux")):
        return {'non-standard system': os}

    # Potentially add checks for too-old kernel versions (OS-specific)
