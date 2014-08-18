def run(flat, sections, mode):
    bits = flat['arch_bits']

    if bits and bits != 64:
        return {'not 64-bit system': bits}
