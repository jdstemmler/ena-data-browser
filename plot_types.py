from collections import defaultdict

prefix_to_type = {

    '10um-scattering-linear':       'scattering',
    '10um-scattering-log':          'scattering',
    '1um-scattering-linear':        'scattering',
    '1um-scattering-log':           'scattering',

    'aerosol-concentration-linear': 'aerosol',
    'aerosol-concentration-log':    'aerosol',

    'boundary-layer-radar':         'radar',
    'full-height-radar':            'radar',

    'ccn':                          'ccn',

    'cn-linear':                    'cn',
    'cn-log':                       'cn',

    'co-linear':                    'co',
    'co-log':                       'co',

    'precip':                       'precip',
    'wind':                         'wind',
    'wind-rose':                    'rose',

    'uhsas':                        'uhsas'

}

type_to_prefix = defaultdict(list)

for k, v in prefix_to_type.items():
    type_to_prefix[v].append(k)

prefix_labels = {

    '10um-scattering-linear':       '10um Linear',
    '10um-scattering-log':          '10um Log',
    '1um-scattering-linear':        '1um Linear',
    '1um-scattering-log':           '1um Log',

    'aerosol-concentration-linear': 'Linear',
    'aerosol-concentration-log':    'Log',

    'boundary-layer-radar':         'Boundary Layer',
    'full-height-radar':            'Full Height',

    'ccn':                          'CCN',

    'cn-linear':                    'Linear',
    'cn-log':                       'Log',

    'co-linear':                    'Linear',
    'co-log':                       'Log',

    'precip':                       'Precipitation',
    'wind':                         'Wind',
    'wind-rose':                    'Wind Rose',

    'uhsas':                        'UHSAS'

}
