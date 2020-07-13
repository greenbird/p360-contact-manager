from p360_contact_manager.api.p360 import Ping
from p360_contact_manager.common import PostRequest


def test_ping_dry():
    """Test that we abort and return Success(DRY RUN. No API calls executed."""
    assert Ping(
        'authkey', 'baseurl', PostRequest(), dry=True,
    )().unwrap() == 'DRY RUN: No API calls executed'
