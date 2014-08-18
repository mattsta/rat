def run(flat, sections, mode):
    isLoading = flat['loading_start_time']
    totalSz = flat['loading_total_bytes']
    processedSz = flat['loading_loaded_bytes']
    percentDone = flat['loading_loaded_perc']

    if isLoading:
        return {"loading initial dataset (size in bytes)": totalSz,
                "processed bytes so far": processedSz,
                "percent loaded": percentDone}
