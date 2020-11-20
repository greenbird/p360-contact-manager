from returns.result import Failure, Success

from p360_contact_manager.api.p360 import GetEnterprises
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


def test_get_enterprises(mocker):
    """Test update enterprise success."""
    post = mocker.patch('p360_contact_manager.common.PostRequest.__call__')
    post.return_value = Success(GoodResponse())

    assert GetEnterprises(
        'authkey',
        'base_url/',
        PostRequest(),
    )({}).unwrap()['Successful']

    post.assert_called()
    post.assert_called_with(
        'base_url/GetEnterprises',
        payload={},
        url_params={'authkey': 'authkey'},
        timeout=20,
    )


def test_get_enterprises_failure(mocker):
    """Test update enterprise failure."""
    post = mocker.patch('p360_contact_manager.common.PostRequest.__call__')
    post.return_value = Success(BadRequestResponse())
    bad_result = GetEnterprises(
        'authkey',
        'base_url',
        PostRequest(),
    )({})

    assert 'An error message' in str(bad_result.failure())
    post.assert_called()


def test_get_enterprises_response_failure(mocker):
    """Test update enterprise post return failure."""
    post = mocker.patch('p360_contact_manager.common.PostRequest.__call__')
    post.return_value = Failure(Exception('Error'))
    bad_result = GetEnterprises(
        'authkey',
        'base_url',
        PostRequest(),
    )({})

    assert 'Error' in str(bad_result.failure())
    post.assert_called()
