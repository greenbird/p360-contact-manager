from returns.result import Failure, Success

from p360_contact_manager.api.p360 import GetAllEnterprises, GetEnterprises
from p360_contact_manager.common import PostRequest


class ResponseObject(object):
    """mock class for response object."""

    headers: dict = {'Content-Type': 'application/json'}

    def raise_for_status(self):
        pass  # noqa: WPS420

    def json(self):
        pass  # noqa: WPS420


class GoodResponse(ResponseObject):
    """Mock class for good response."""

    headers: dict = {'Content-Type': 'application/json; charset=utf-8'}

    def json(self):
        return {
            'Enterprises': [
                {
                    'Recno': 0,
                    'ContactRelations': {},
                    'EnterpriseNumber': 'string',
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


class BadRequestResponse(ResponseObject):
    """Mock class for bad response."""
    def json(self):
        return {
            'Recno': 0,
            'Successful': False,
            'ErrorMessage': 'An error message',
            'ErrorDetails': 'string',
        }


class ResponseWithNonJsonContentType(ResponseObject):
    """Mock class for response with non-json content-type header."""
    headers: dict = {'Content-Type': 'text/html'}

    def json(self):
        return {}


def test_get_all_enterprises(mocker):
    """Test update enterprise success."""
    post = mocker.patch('p360_contact_manager.common.PostRequest.__call__')
    post.return_value = Success(GoodResponse())

    assert GetAllEnterprises(
        GetEnterprises(
            'authkey',
            'base_url/',
            PostRequest(),
        ),
        {},
    )().unwrap()['Successful']

    post.assert_called()
    post.assert_called_with(
        'base_url/GetEnterprises',
        payload={},
        url_params={'authkey': 'authkey'},
        timeout=20,
    )


def test_get_all_enterprises_failure(mocker):
    """Test update enterprise failure."""
    post = mocker.patch('p360_contact_manager.common.PostRequest.__call__')
    post.return_value = Success(BadRequestResponse())
    bad_result = GetAllEnterprises(
        GetEnterprises(
            'authkey',
            'base_url/',
            PostRequest(),
        ),
        {},
    )()
    assert 'An error message' in str(bad_result.failure())
    post.assert_called()


def test_get_all_enterprises_response_failure(mocker):
    """Test update enterprise post returns failure."""
    post = mocker.patch('p360_contact_manager.common.PostRequest.__call__')
    post.return_value = Failure(Exception('Error'))
    bad_result = GetAllEnterprises(
        GetEnterprises(
            'authkey',
            'base_url/',
            PostRequest(),
        ),
        {},
    )()

    assert 'Error' in str(bad_result.failure())
    post.assert_called()


def test_get_all_enterprises_response_with_wrong_header(mocker):  # noqa: WPS118
    """Test update enterprise post returns failure."""
    post = mocker.patch('p360_contact_manager.common.PostRequest.__call__')
    post.return_value = Success(ResponseWithNonJsonContentType())

    bad_result = GetAllEnterprises(
        GetEnterprises(
            'authkey',
            'base_url/',
            PostRequest(),
        ),
        {},
    )()
    assert 'Content-type "text/html" is not equal to application/json' in str(
        bad_result.failure(),
    )
    post.assert_called()
