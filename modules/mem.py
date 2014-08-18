def run(flat, sections, mode):
    result = {}
    memtestResult = flat['memtestResult']
    memtestAll = flat['memtest']
    memusage = flat['used_memory'] or None
    alloc = flat['mem_allocator']
    MB = 1024*1024.0
    GB = MB * 1024.0
    TB = GB * 1024.0

    # memtestResult will only exist in an error report, not just INFO output
    if "error" in memtestResult:
        result["memory test error"] = memtestAll

    if alloc and not alloc.startswith('jemalloc'):
        result['using non-jemalloc allocator'] = alloc

    # Arbitrary size classes
    if 0 < memusage <= 5*MB:
        result['memory usage'] = "%.2f MB" % (memusage/MB)
        result['size'] = "tiny"
    elif 5*MB < memusage <= 100*MB:
        result['memory usage'] = "%.2f MB" % (memusage/MB)
        result['size'] = "small"
    elif 100*MB < memusage <= 4*GB:
        result['memory usage'] = "%.2f GB" % (memusage/GB)
        result['size'] = "medium"
    elif 4*GB < memusage <= 256*GB:
        result['memory usage'] = "%.2f GB" % (memusage/GB)
        result['size'] = "large"
    elif 256*GB < memusage <= 768*GB:
        result['memory usage'] = "%.2f GB" % (memusage/GB)
        result['size'] = "very large"
    elif 768*GB < memusage:
        result['memory usage'] = "%.2f TB" % (memusage/TB)
        result['size'] = "giant"

    return result
