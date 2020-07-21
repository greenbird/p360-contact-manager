# -*- coding: utf-8 -*-

"""Package to get list of duplicate enterprises in ContactService API."""

import logging
import sys

from dependencies import Injector

from p360_contact_manager.api import p360
from p360_contact_manager.arguments import ArgsParser
from p360_contact_manager.common import ConfigureLogging, ReadLocalFile
from p360_contact_manager.injected import (
    BrregSynchronizeScope,
    CacheEnterprisesScope,
    DuplicatesScope,
    PingScope,
    SynchronizeScope,
    UpdateScope,
)

ConfigureLogging()()
log = logging.getLogger('main')

args = ArgsParser()(sys.argv[1:]).unwrap()

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
    'brreg_synchronize': BrregSynchronizeScope,
    'synchronize': SynchronizeScope,
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
