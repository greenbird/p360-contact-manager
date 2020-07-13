from returns.result import Failure, Success

from p360_contact_manager.api.p360 import UpdateEnterprise
from p360_contact_manager.common import PostRequest


class ResponseObject(object):
    """mock class for response object."""
    def raise_for_status(self):
        pass  # noqa: WPS420

    def json(self):
        pass  # noqa: WPS420


class GoodResponse(ResponseObject):
    """Mock class for good response."""
    def json(self):
        return {
            'Recno': 0,
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


def test_update_enterprise_dry_run(mocker):
    """Test that we abort and return Success(DRY RUN. No API calls executed."""
    assert UpdateEnterprise(
        'authkey', 'base_url', PostRequest(), dry=True,
    )({}).unwrap() == 'DRY RUN: No API calls executed'


def test_update_enterprise(mocker):
    """Test update enterprise success."""
    post = mocker.patch('p360_contact_manager.common.PostRequest.__call__')
    post.return_value = Success(GoodResponse())

    assert UpdateEnterprise(
        'authkey',
        'base_url',
        PostRequest(),
    )({}).unwrap()['Successful']

    post.assert_called()
    post.assert_called_with(
        'base_urlUpdateEnterprise',
        payload={},
        url_params={'authkey': 'authkey'},
        timeout=10,
    )


def test_update_enterprise_failure(mocker):
    """Test update enterprise failure."""
    post = mocker.patch('p360_contact_manager.common.PostRequest.__call__')
    post.return_value = Success(BadRequestResponse())
    bad_result = UpdateEnterprise(
        'authkey',
        'base_url',
        PostRequest(),
    )({})

    assert 'An error message' in str(bad_result.failure())
    post.assert_called()


def test_update_enterprise_response_failure(mocker):
    """Test update enterprise post return failure."""
    post = mocker.patch('p360_contact_manager.common.PostRequest.__call__')
    post.return_value = Failure(Exception('Error'))
    bad_result = UpdateEnterprise(
        'authkey',
        'base_url',
        PostRequest(),
    )({})

    assert 'Error' in str(bad_result.failure())
    post.assert_called()
