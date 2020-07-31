import json

from returns.result import Success

from p360_contact_manager.usecases.synchronize import Synchronize

worklist = json.dumps([
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


def test_create_empty_duplicate_worklist_file(mocker):
    """Test finding duplicates work success."""
    local_write_patch = mocker.patch(
        'p360_contact_manager.usecases.synchronize.Synchronize._write_result',
    )
    local_write_patch.return_value = Success(True)

    assert Synchronize(
        'worklistfile.json',  # _worklist
        50,  # _error_margin
        lambda _: Success(
            {
                'Recno': 0,
                'Successful': True,
                'ErrorMessage': 'string',
                'ErrorDetails': 'string',
            },
        ),  # SynchronizeEnterprise
        lambda _filename, _mode: Success(worklist),  # _read
        lambda _filaneme, _bytes: Success(True),  # _write
    )().unwrap()

    local_write_patch.assert_called_once_with(
        json.dumps(
            {'errors': 0, 'synchronized': ['994921142'], 'failed': []},
        ),
    )
