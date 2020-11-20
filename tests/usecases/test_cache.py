import json

from returns.result import Success

from p360_contact_manager.common import WriteLocalFile
from p360_contact_manager.usecases.cache import CacheEnterprises


def test_cache_enterprises_creates_file(mocker):
    """Test update enterprise success."""

    write_patch = mocker.patch(
        'p360_contact_manager.common.WriteLocalFile.__call__',
    )
    write_patch.return_value = Success(True)
    test_data = {'json': 'data'}
    assert CacheEnterprises(
        lambda: Success(test_data),  # get all enterprises
        WriteLocalFile(),
    )().unwrap() is True
    write_patch.assert_called_once_with(
        json.dumps(test_data),
        file_path='cache.json',
    )
