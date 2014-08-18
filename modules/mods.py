def run(flat, sections, mode):
    hasModules = flat['loaded_modules']

    if hasModules:
        return {'contaminated by dynamic code': sections['Modules']}

    # Potentially add checks for too-old kernel versions (OS-specific)
