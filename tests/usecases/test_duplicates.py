import json
from copy import deepcopy

from returns.result import Success

from p360_contact_manager.common import WriteLocalFile
from p360_contact_manager.usecases.duplicates import Duplicates

enterprises = {
    'Enterprises': [
        {
            'Recno': 0,
            'ContactRelations': {},
            'EnterpriseNumber': '123',
            'ExternalID': 'string',
            'Name': 'string',
        },
        {
            'Recno': 1,
            'ContactRelations': {},
            'EnterpriseNumber': '123',
            'ExternalID': 'string',
            'Name': 'string',
        },
    ],
    'TotalPageCount': 0,
    'TotalCount': 0,
    'Successful': True,
    'ErrorMessage': 'string',
    'ErrorDetails': 'string',
}


def test_create_empty_duplicate_worklist_file(mocker):
    """Test finding duplicates work success."""

    write_patch = mocker.patch(
        'p360_contact_manager.common.WriteLocalFile.__call__',
    )
    write_patch.return_value = Success(True)
    test_data = deepcopy(enterprises)
    test_data['Enterprises'].pop()
    update_payload = {'update': True}
    assert Duplicates(
        lambda: Success(test_data),  # _get_all_enterprises
        WriteLocalFile(),  # _write
        output='outputfile.json',  # _duplicate_worklist
        duplicate_remove_payload=update_payload,
    )().unwrap() is True
    write_patch.assert_called_once_with(
        json.dumps({'update': [], 'skip': []}),
        file_path='outputfile.json',
    )


def test_recno_one_enterprises_are_skipped(mocker):
    """Test finding duplicates work success."""

    write_patch = mocker.patch(
        'p360_contact_manager.common.WriteLocalFile.__call__',
    )
    write_patch.return_value = Success(True)
    test_data = deepcopy(enterprises)
    test_data['Enterprises'][0]['Categories'] = ['recno:1']
    update_payload = {'update': True}
    assert Duplicates(
        lambda: Success(test_data),  # _get_all_enterprises
        WriteLocalFile(),  # _write
        output='outputfile.json',  # _duplicate_worklist
        duplicate_remove_payload=update_payload,
    )().unwrap() is True
    write_patch.assert_called_once_with(
        json.dumps({'update': [], 'skip': []}),
        file_path='outputfile.json',
    )


def test_create_duplicate_worklist_file(mocker):
    """Test finding duplicates work success."""

    write_patch = mocker.patch(
        'p360_contact_manager.common.WriteLocalFile.__call__',
    )
    write_patch.return_value = Success(True)
    test_data = enterprises
    update_payload = {'update': True}
    assert Duplicates(
        lambda: Success(test_data),  # _get_all_enterprises
        WriteLocalFile(),  # _write
        output='outputfile.json',  # _duplicate_worklist
        duplicate_remove_payload=update_payload,
    )().unwrap() is True
    write_patch.assert_called_once_with(
        json.dumps(
            {
                'update': [
                    {
                        'original_data': {
                            'Recno': 1,  # highest number should be updated
                            'ContactRelations': {},
                            'EnterpriseNumber': '123',
                            'ExternalID': 'string',
                            'Name': 'string',
                        },
                        'payload': {
                            'parameters': {
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
        ),
        file_path='outputfile.json',
    )
