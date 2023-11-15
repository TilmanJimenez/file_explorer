import re

FILE_NAME_PATTERNS = [
        # Current Expedition
        re.compile('^{}{}_{}_{}{}{}_{}{}_{}_{}{}.{}$'.format(r'(?P<prefix>u|d)?',
                                                        r'(?P<instrument>sbe\d{2})',
                                                        r'(?P<instrument_number>\d{4})',
                                                        r'(?P<year>\d{4})',
                                                        r'(?P<month>\d{2})',
                                                        r'(?P<day>\d{2})',
                                                        r'(?P<hour>\d{2})',
                                                        r'(?P<minute>\d{2})',
                                                        r'(?P<ship>\d{2}_\w{2})',
                                                        r'(?P<serno>\d{4})',
                                                        r'(?P<tail>[a-z0-9\-_åäö ]*)?',
                                                        r'(?P<suffix>\w*)?'
                                                        )
                   ),
        # New standard format test file
        re.compile('^{}{}_{}_{}{}{}_{}{}_{}_{}_{}_{}{}.{}$'.format(r'(?P<prefix>u|d)?',
                                                           r'(?P<instrument>sbe\d{2})',
                                                           r'(?P<instrument_number>\d{4})',
                                                           r'(?P<year>\d{4})',
                                                           r'(?P<month>\d{2})',
                                                           r'(?P<day>\d{2})',
                                                           r'(?P<hour>\d{2})',
                                                           r'(?P<minute>\d{2})',
                                                           r'(?P<ship>\d{2}\w{2})',
                                                           r'(?P<cruise>\d{2})',
                                                           r'(?P<serno>\d{4})',
                                                           r'(?P<test>test)',
                                                           r'(?P<tail>['
                                                           r'a-z0-9\-_åäö ]*)?',
                                                           r'(?P<suffix>\w*)?'
                                                           )
                   ),
        # New standard format
        re.compile('^{}{}_{}_{}{}{}_{}{}_{}_{}_{}{}.{}$'.format(r'(?P<prefix>u|d)?',
                                                           r'(?P<instrument>sbe\d{2})',
                                                           r'(?P<instrument_number>\d{4})',
                                                           r'(?P<year>\d{4})',
                                                           r'(?P<month>\d{2})',
                                                           r'(?P<day>\d{2})',
                                                           r'(?P<hour>\d{2})',
                                                           r'(?P<minute>\d{2})',
                                                           r'(?P<ship>\d{2}\w{2})',
                                                           r'(?P<cruise>\d{2})',
                                                           r'(?P<serno>\d{4})',
                                                           r'(?P<tail>['
                                                           r'a-z0-9\-_åäö ]*)?',
                                                           r'(?P<suffix>\w*)?'
                                                           )
                   ),
        # Early utsjön
        re.compile('^{}{}{}{}{}.{}$'.format(r'(?P<ship>\w{2})',
                                       r'(?P<year>\d{2})',
                                       r'(?P<midfix>u|d)',
                                       r'(?P<serno>\d{3,4})',
                                       r'(?P<tail>[a-z0-9\-_åäö ]*)?',
                                       r'(?P<suffix>\w*)?'
                                       )
                   ),
        # DV Profile: ctd_profile_20151007_7798_0001.txt
        re.compile('^ctd_profile_{}{}{}_{}_{}.{}$'.format(r'(?P<year>\d{4})',
                                                       r'(?P<month>\d{2})',
                                                       r'(?P<day>\d{2})',
                                                       r'(?P<ship>.{4})',
                                                       r'(?P<serno>\d{4})',
                                                       r'(?P<suffix>\w*)?'
                                                       )
                   ),
        # MVP: mvp_2021-10-17_071640_a13-a17.cnv
        re.compile('^{}{}_{}-{}-{}_{}{}{}_{}.{}$'.format(r'(?P<prefix>u|d)?',
                                                    r'(?P<instrument>mvp)',
                                                     r'(?P<year>\d{4})',
                                                     r'(?P<month>\d{2})',
                                                     r'(?P<day>\d{2})',
                                                     r'(?P<hour>\d{2})',
                                                     r'(?P<minute>\d{2})',
                                                     r'(?P<second>\d{2})',
                                                     r'(?P<transect>[a-z0-9\-_åäö ]*)',
                                                     r'(?P<suffix>cnv)?'
                                                    )
                    ),
        # MVP: MVP_2021-10-17_071640_xedited
        re.compile('^{}_{}-{}-{}_{}{}{}{}.{}$'.format('(?P<instrument>mvp)',
                                                    r'(?P<year>\d{4})',
                                                    r'(?P<month>\d{2})',
                                                    r'(?P<day>\d{2})',
                                                    r'(?P<hour>\d{2})',
                                                    r'(?P<minute>\d{2})',
                                                    r'(?P<second>\d{2})',
                                                    r'(?P<tail>[a-z0-9\-_åäö ]*)?',
                                                    r'(?P<suffix>\w*)?'
                                                    )
                   ),
        # ODV '\d*_ODV_\w{4}\d{4}_\d*_\w{3}_\w{2}.\w*'
        re.compile('^{}_{}_{}{}_{}_{}_{}.{}$'.format(r'(?P<originator>\d*)',
                                                    r'(?P<format>odv)',
                                                    r'(?P<ship>\d{2}\w{2})',
                                                    r'(?P<year>\d{4})',
                                                    r'(?P<number>\d*)',
                                                    r'(?P<dtype>\w{3})',
                                                    r'(?P<version>\w{2})',
                                                    r'(?P<suffix>\w*)?'
                                                    )
                   ),
        # ODEN specific
        re.compile('^aom{}-station-{}-cast{}.{}$'.format(r'(?P<year>\d{2})',
                                                 r'(?P<station>\d{2})',
                                                 r'(?P<number>\d+)',
                                                 r'(?P<suffix>\w*)?',
                                                 )),

        re.compile('^ryder{}-{}-ctd{}.{}$'.format(r'(?P<year>\d{2})',
                                                         r'(?P<station>\d{2})',
                                                         r'(?P<number>\d+)',
                                                         r'(?P<suffix>\w*)?',
                                                         ))
    ]

CRUISE_PATTERNS = [
    # 77SE-2022-02
    re.compile('^{}-{}-{}$'.format(r'(?P<ship>\d{2}\w{2})',
                                   r'(?P<year>\d{4})',
                                   r'(?P<cruise>\d{2})')
               ),
    re.compile('^smhi-{}-{}$'.format(r'(?P<cruise>\d{2})',
                                     r'(?P<year>\d{4})')
               ),
    re.compile('^smhi_{}_{}$'.format(r'(?P<month_str>\d{2})',
                                     r'(?P<year>\d{4})')
               ),
    re.compile('^vecka {}$'.format(r'(?P<week>\d{1,2})')
               )
]


def get_file_name_match(string):
    for PATTERN in FILE_NAME_PATTERNS:
        name_match = PATTERN.search(string.strip().lower())
        if name_match:
            return name_match


def get_cruise_match(string):
    for PATTERN in CRUISE_PATTERNS:
        name_match = PATTERN.search(string.strip().lower())
        if name_match:
            return name_match


def get_cruise_match_dict(string):
    data = {'cruise_string': string}
    name_match = get_cruise_match(string)
    if not name_match:
        data.update({'cruise_info': string})
        return data
    data.update(name_match.groupdict())
    return data
