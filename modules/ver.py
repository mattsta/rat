def run(flat, sections, mode):
    result = {}
    version = flat['redis_version']

    if ("2.8." in version) or ("3.0." in version):
        versionStatus = "OK"
    elif ("2.9." in version):
        versionStatus = "BETA"
    elif version:
        versionStatus = "OLD"
    else:
        versionStatus = "UNKNOWN"

    result['version'] = version
    result['status'] = versionStatus

    if flat['redis_git_dirty']:
        result['contaminated build'] = (flat['redis_version'], flat['redis_git_sha1'])

    return result
