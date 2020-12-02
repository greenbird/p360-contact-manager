import json

from returns.result import Success

from p360_contact_manager.api.p360 import UpdateEnterprise
from p360_contact_manager.common import PostRequest, WriteLocalFile
from p360_contact_manager.usecases.update import Update

worklist = json.dumps(
    {
        'update': [
            {
                'original_data': {
                    'Recno': 1,
                    'ContactRelations': {},
                    'EnterpriseNumber': '123',
                    'ExternalID': 'string',
                    'Name': 'string',
                },
                'payload': {
                    'parameter': {
                        'update': True,
                        'Recno': 1,
                    },
                },
            },
        ],
        'skip': [
            {
                'Recno': 0,
                'ContactRelations': {},
                'EnterpriseNumber': '123',
                'ExternalID': 'string',
                'Name': 'string',
            },
        ],
    },
)


def test_create_empty_duplicate_worklist_file(mocker):
    """Test finding duplicates work success."""
    api_patch = mocker.patch(
        'p360_contact_manager.api.p360.UpdateEnterprise.__call__',
    )
    api_patch.return_value = Success(
        {
            'Recno': 1,
            'Successful': True,
            'ErrorMessage': 'string',
            'ErrorDetails': 'string',
        },
    )

    write_patch = mocker.patch(
        'p360_contact_manager.common.WriteLocalFile.__call__',
    )
    write_patch.return_value = Success(True)

    assert Update(
        'worklistfile.json',  # _worklist
        50,  # _error_margin
        UpdateEnterprise('authkey', 'base_url', PostRequest()),
        lambda _filename, _mode: Success(worklist),  # _read
        WriteLocalFile(),  # _write
        output='outputfile.json',  # _update_result
    )().unwrap()

    api_patch.assert_called_once_with(
        json.loads(worklist)['update'][0]['payload'],
    )

    write_patch.assert_called_once_with(
        json.dumps(
            {'errors': 0, 'updated': [1], 'failed': []},
        ),
        file_path='outputfile.json',
    )
