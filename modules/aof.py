def run(flat, sections, mode):
    result = {}
    enabled = flat['aof_enabled']
    rewriting = flat['aof_rewrite_in_progress']
    rewritingDuration = flat['aof_current_rewrite_time_sec']

    if not sections['Persistence']:
        return

    if enabled:
        result['enabled'] = True

    if rewriting:
        result['currently rewriting'] = True
        result['current rewrite duration'] = rewritingDuration

    return result
