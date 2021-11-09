def for_program(trg, programs):
    has_trg = True
    if len([p['program_name'] for p in programs if p['program_name'] == trg]) < 1:
        print('Missing {} program...continuing'.format(trg))
        has_trg = False
    return has_trg
