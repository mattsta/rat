def run(flat, sections, mode):
    isCluster = flat['cluster_enabled']

    if isCluster:
        return "active cluster node"
