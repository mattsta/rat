def run(flat, sections, mode):
    result = {}
    replicaCount = flat['connected_slaves']
    isReplica = flat['role'] == "slave"

    if isReplica:
        result['replicating from'] = \
            flat['master_host'] + ":" + str(flat['master_port'])
        result['server is read only'] = True \
            if flat['slave_read_only'] else False

        if replicaCount > 0:
            result['additional chained replica count'] = additionalReplicas

    return result
