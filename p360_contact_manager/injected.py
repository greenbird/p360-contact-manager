# -*- encoding: utf-8 -*-

"""Dependencies for usecases."""
from dependencies import Injector

from p360_contact_manager import common
from p360_contact_manager.api import brreg, p360
from p360_contact_manager.usecases.brreg_syncronize import BrregSyncronize
from p360_contact_manager.usecases.cache import CacheEnterprises
from p360_contact_manager.usecases.duplicates import Duplicates
from p360_contact_manager.usecases.ping import Ping
from p360_contact_manager.usecases.synchronize import Synchronize
from p360_contact_manager.usecases.update import Update

CommonScope = Injector.let(
    post=common.PostRequest,
    read=common.ReadLocalFile,
    write=common.WriteLocalFile,
)

GetAllEnterprisesScope = Injector.let(
    get_all_enterprises=p360.GetAllEnterprises,
    get_enterprises=p360.GetEnterprises,
    base_payload={
        'parameter': {
            'Active': True,
            'Page': 0,
            'MaxRows': 20,
            'SortCriterion': 'RecnoDescending',
            'IncludeCustomFields': False,
        },
    },
    post=common.PostRequest,
)

GetAllCachedEnterprisesScope = Injector.let(
    get_all_enterprises=p360.GetAllCachedEnterprises,
    read=common.ReadLocalFile,
)

PingScope = Injector.let(
    run=Ping,
    post=common.PostRequest,
    ping_p360=p360.Ping,
)

CacheEnterprisesScope = GetAllEnterprisesScope.let(
    run=CacheEnterprises,
    write=common.WriteLocalFile,
)

DuplicatesScope = GetAllEnterprisesScope.let(
    run=Duplicates,
    duplicate_worklist='duplicates_worklist.json',
    write=common.WriteLocalFile,
    update_payload={
        'Recno': None,
        'Active': False,
        'EnterpriseNumber': '',
    },
)

UpdateScope = Injector.let(
    run=Update,
    update_result='update_result',
    update_enterprise=p360.UpdateEnterprise,
    post=common.PostRequest,
    read=common.ReadLocalFile,
    write=common.WriteLocalFile,
)

# Removed: BO, KBO, UTLA
organisasjonsforms = [  # noqa: WPS317
    'AAFY', 'ADOS', 'ANNA', 'ANS', 'AS', 'ASA', 'BA', 'BBL', 'BEDR', 'BRL',
    'DA', 'ENK', 'EOFG', 'ESEK', 'FKF', 'FLI', 'FYLK', 'GFS', 'IKJP', 'IKS',
    'KF', 'KIRK', 'KOMM', 'KS', 'KTRF', 'NUF', 'OPMV', 'ORGL', 'PERS', 'PK',
    'PRE', 'SA', 'SAM', 'SE', 'SF', 'SPA', 'STAT', 'STI', 'SÆR', 'TVAM',
    'VPFO',
]

BrregSynchronizeScope = Injector.let(
    run=BrregSyncronize,
    brreg_worklist='brreg_syncronize_worklist.json',
    search_criteria={
        'organisasjonsform': ','.join(organisasjonsforms),
        'konkurs': False,
        'fraAntallAnsatte': 1,
        'registrertIMvaregisteret': True,
        'registrertIForetaksregisteret': True,
        'naeringskode': 'A,C,D,E,F,I,K,L,M,N,O,P,Q,R,S',
        'size': 100,
    },
    get_country=common.GetCountryCode,
    get_all_organizations=brreg.GetAllOrganizations,
    get_organizations=brreg.GetOrganizations,
    get=common.GetRequest,
    write=common.WriteLocalFile,
)

SynchronizeScope = Injector.let(
    run=Synchronize,
    synchronize_result='synchronize_result',
    synchronize_enterprise=p360.SynchronizeEnterprise,
    post=common.PostRequest,
    read=common.ReadLocalFile,
    write=common.WriteLocalFile,
)
