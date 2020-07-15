import json

from returns.result import Success

from p360_contact_manager.api.brreg import (
    GetAllOrganizations,
    GetOrganizations,
)
from p360_contact_manager.common import (
    GetCountryCode,
    GetRequest,
    WriteLocalFile,
)
from p360_contact_manager.usecases.brreg_syncronize import BrregSyncronize

expected = json.dumps([
    {
        'brreg_url': 'https://data.brreg.no/enhetsregisteret/api/enheter/994921142',  # noqa: E501
        'payload': {
            'parameter': {
                'EnterpriseNumber': '994921142',
                'Name': 'GREENBIRD INTEGRATION TECHNOLOGY AS',
                'Web': 'www.greenbird.com',
                'OfficeAddress': {
                    'Country': 'NOR',
                    'County': 'OSLO',
                    'StreetAddress': 'Storgata 1',
                    'ZipCode': '0155',
                    'ZipPlace': 'OSLO',
                }, 'PostAddress': {
                    'Country': 'NOR',
                    'County': 'OSLO',
                    'StreetAddress': 'Storgata 1',
                    'ZipCode': '0155',
                    'ZipPlace': 'OSLO',
                },
            },
        },
    },
])


def test_create_synchronize_worklist_file(mocker):
    """Test finding duplicates work success."""

    write_patch = mocker.patch(
        'p360_contact_manager.common.WriteLocalFile.__call__',
    )
    write_patch.return_value = Success(True)

    assert BrregSyncronize(
        'outputfile.json',  # _brreg_worklist
        {
            'navn': 'GREENBIRD',
            'naeringskode': 'J',
        },  # _search_criteria
        '0301',  # kommune_numbers
        GetAllOrganizations(
            GetOrganizations(
                'https://data.brreg.no/enhetsregisteret/api/',
                GetRequest(),
            ),
        ),  # _get_all_organizations
        WriteLocalFile(),  # _write
        GetCountryCode(),  # _get_country
    )()

    write_patch.assert_called_once_with(
        'outputfile.json',
        expected,
    )
