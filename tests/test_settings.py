import json

from returns.pipeline import is_successful
from returns.result import Success

from p360_contact_manager.settings import LoadSettings, StoreSettings


def test_loading_settings(mocker):
    expected = {'a': '1', 'b': '1'}
    read_patch = mocker.patch(
        'p360_contact_manager.common.ReadLocalFile.__call__',
    )
    read_patch.return_value = Success(json.dumps(expected))
    loaded = LoadSettings('tests/settings.json')()
    assert is_successful(loaded)
    assert loaded.unwrap() == expected


def test_non_existing_file_returns_empty_dict():
    loaded = LoadSettings('tests/does_not_exist.json')()
    assert is_successful(loaded)
    assert not len(loaded.unwrap())


def test_storing_settings(mocker):
    read_patch = mocker.patch(
        'p360_contact_manager.common.ReadLocalFile.__call__',
    )
    read_patch.return_value = Success(json.dumps({'a': '1', 'b': '1'}))
    write_patch = mocker.patch(
        'p360_contact_manager.common.WriteLocalFile.__call__',
    )
    expected = json.dumps({'a': '1', 'b': '2'})

    StoreSettings()({'b': '2'})

    write_patch.assert_called_once_with(
        'settings.json',
        expected,
    )
