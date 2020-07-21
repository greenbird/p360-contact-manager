from returns.result import Success

from p360_contact_manager.api.p360 import GetAllCachedEnterprises
from p360_contact_manager.common import ReadLocalFile


def test_get_enterprises(mocker):
    """Test update enterprise success."""
    read = mocker.patch('p360_contact_manager.common.ReadLocalFile.__call__')
    read.return_value = Success("""{"data": "data"}""")  # noqa: WPS322

    assert GetAllCachedEnterprises(
        ReadLocalFile(),
        'filename',
    )().unwrap() is not None
    read.assert_called()
