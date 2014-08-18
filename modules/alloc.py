def run(flat, sections, mode):
    os = flat['os']
    alloc = flat['mem_allocator']

    if os.startswith("Darwin") and not (alloc == "libc"):
        return {'non-standard allocator configuration': alloc}

    if os.startswith("Linux") and not alloc.startswith("jemalloc"):
        return {'non-standard allocator configuration': alloc}
