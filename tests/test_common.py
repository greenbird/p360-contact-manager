from p360_contact_manager.common import GetRequest, PostRequest


def test_get_request(mocker):
    """Test get function works."""
    assert GetRequest()(
        'http://www.github.com', {},
    ).unwrap().status_code == 200


def test_post_request(mocker):
    """Test post function works."""
    assert PostRequest()(
        'http://www.github.com', {}, {},
    ).unwrap().status_code == 200
