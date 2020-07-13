from returns.pipeline import is_successful

from p360_contact_manager.api.brreg import (
    GetAllOrganizations,
    GetOrganization,
    GetOrganizations,
)
from p360_contact_manager.common import GetRequest


def test_get_organization():
    """Get an organization by organization number."""
    assert GetOrganization(
        'https://data.brreg.no/enhetsregisteret/api/',
        GetRequest(),
    )('994921142').unwrap()['navn'] == 'GREENBIRD INTEGRATION TECHNOLOGY AS'


def test_get_organization_failure():
    """Make sure we get a failure on bad request."""
    assert GetOrganization(
        'https://data.brreg.no/enhetsregisteret/api/',
        GetRequest(),
    )('123').failure().response.status_code == 400


def test_get_organizations():
    """Test that we get an array with organizations with given text."""
    search_criteria = {
        'navn': 'GREENBIRD',
        'registrertIMvaregisteret': True,
    }

    org_result = GetOrganizations(
        'https://data.brreg.no/enhetsregisteret/api/',
        GetRequest(),
    )(search_criteria)

    assert is_successful(org_result)
    assert isinstance(org_result.unwrap()['_embedded']['enheter'], list)


def test_get_organizations_failure():
    """Bad search criteria should provoke failure."""
    search_criteria = {
        'name': 'GREENBIRD',
    }

    org_result = GetOrganizations(
        'https://data.brreg.no/enhetsregisteret/api/',
        GetRequest(),
    )(search_criteria)

    assert not is_successful(org_result)
    assert org_result.failure().response.status_code == 400
    assert 'Feilaktig forespørsel' in org_result.failure().response.text


def test_get_all_organizations():
    """Test that we get an array with organizations with given text."""
    search_criteria = {
        'navn': 'GREENBIRD',
        'kommunenummer': '0301',
        'naeringskode': 'J',
    }

    org_result = GetAllOrganizations(
        GetOrganizations(
            'https://data.brreg.no/enhetsregisteret/api/',
            GetRequest(),
        ),
    )(search_criteria).alt(print)

    assert is_successful(org_result)
    assert isinstance(org_result.unwrap(), list)


def test_get_all_organizations_failure():
    """Bad search criteria should provoke failure."""
    search_criteria = {
        'kommnummer': '0301',
        'naeringskode': 'J',
    }

    org_result = GetAllOrganizations(
        GetOrganizations(
            'https://data.brreg.no/enhetsregisteret/api/',
            GetRequest(),
        ),
        GetRequest(),
    )(search_criteria)

    assert not is_successful(org_result)
    assert 'kommunenummer' in str(org_result.failure())
