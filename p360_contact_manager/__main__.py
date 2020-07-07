# -*- coding: utf-8 -*-

"""Package to get list of duplicate enterprises in ContactService API."""

import argparse
import logging

from dependencies import Injector
from typing_extensions import Final

from p360_contact_manager.api import p360
from p360_contact_manager.common import ConfigureLogging, ReadLocalFile
from p360_contact_manager.injected import (
    BrregSynchronizeScope,
    CacheEnterprisesScope,
    DuplicatesScope,
    PingScope,
    SynchronizeScope,
    UpdateScope,
)

DEFAULT_ERROR_MARGIN: Final[int] = 50


ConfigureLogging()()
log = logging.getLogger('main')

parser = argparse.ArgumentParser(
    description='Public 360 Contact Service Enterprise manager',
)

parser.add_argument(
    'action',
    choices=[
        'test',
        'cache_enterprises',
        'find_malformed_external',
        'find_malformed_internal',
        'duplicates',
        'enrich',
        'update',
        'brreg_syncronize',
        'syncronize',
    ],
    help='test connection, cache enterprises, worklist, remove, enrich',
)

parser.add_argument(
    '-ak',
    '--authkey',
    type=str,
    required=True,
    help='Autorization key for ContactService API',
)

parser.add_argument(
    '-pbu',
    '--p360_base_url',
    type=str,
    help='Base url to ContactService API',
    default=None,
)

parser.add_argument(
    '-bu',
    '--brreg_base_url',
    type=str,
    help='Base url to Brønnoysundregisteret API',
    default='https://data.brreg.no/enhetsregisteret/api/',
)

parser.add_argument(
    '-w',
    '--worklist',
    type=str,
    help='worklist to use when updating',
    default='remove_worklist.json',
)

parser.add_argument(
    '-kn',
    '--kommune_numbers',
    type=str,
    help='Comma seperated list of norwegian Kommune numbers',
    default='0301',  # oslo
)

parser.add_argument(
    '-c',
    '--cached',
    action='store_true',
    default=False,
    help='use data from cache.json',
)

parser.add_argument(
    '-d',
    '--dry',
    action='store_true',
    default=False,
    help='This will prevent any updates from actually being sent in remove',
)

parser.add_argument(
    '-em',
    '--error_margin',
    type=int,
    default=DEFAULT_ERROR_MARGIN,
    help='After failure to update has happened x times, program will stop',
)

args = parser.parse_args()

Scope = Injector.let(
    dry=args.dry,
    authkey=args.authkey,
    error_margin=args.error_margin,
    p360_base_url=args.p360_base_url,
    brreg_base_url=args.brreg_base_url,
    kommune_numbers=args.kommune_numbers,
    worklist=args.worklist,
    cache_file='cache.json',
)

functions = {
    'test': PingScope,
    'brreg_syncronize': BrregSynchronizeScope,
    'syncronize': SynchronizeScope,
    'cache_enterprises': CacheEnterprisesScope,
    'duplicates': DuplicatesScope,
    'update': UpdateScope,
}

log.info('Starting program')
log.debug('settings: %s', Scope)
log.info('action: %s', args.action)
action = (Scope & functions[args.action])
if args.cached:
    log.info('Using cached data')
    action = action.let(
        get_all_enterprises=p360.GetAllCachedEnterprises,
        read=ReadLocalFile,
    )

log.info('result: %s', action.run())
