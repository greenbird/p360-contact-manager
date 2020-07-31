from importlib import reload

from returns.pipeline import is_successful
from typing_extensions import Final

import p360_contact_manager.arguments  # noqa: WPS301
from p360_contact_manager.arguments import DEFAULT_ERROR_MARGIN

AUTH_KEY: Final[str] = 'test-key'
ACTION: Final[str] = 'test'
BASE_URL: Final[str] = 'http://dev.test'
BRREG_BASE_URL: Final[str] = 'http://brreg.no'
WORKLIST: Final[str] = 'my_worklist.json'
OUTPUT: Final[str] = 'output.json'
KOMMUNE_NUMBERS: Final[str] = '0505'
ERROR_MARGIN: Final[str] = '35'

MINIMUN_KEYS_LIST: tuple = (
    ACTION, '-ak', AUTH_KEY, '-o', OUTPUT,
)


class TestArgsParser(object):  # noqa: WPS214
    """Test args parser."""

    def setup_method(self):
        """Set up argument parser."""
        self.parser = p360_contact_manager.arguments.ArgsParser()

    def teardown_method(self):
        """Reload arguments.

        This is hack to remove existing ArgsParser after each method.
        Otherwise, arg parser creates duplicated
        definition of the arguments.
        """
        p360_contact_manager.arguments = reload(p360_contact_manager.arguments)

    def test_parse_no_auth_key(self):
        """Parse when no auth keys."""
        response = self.parser([ACTION])
        assert not is_successful(response)
        string = 'following arguments are required: -ak/--authkey'
        assert string in response.failure().args[0]

    def test_short_auth_key(self):
        """Test auth key with short arg version."""
        response = self.parser([ACTION, '-ak', AUTH_KEY, '-o', OUTPUT])
        assert is_successful(response)
        assert response.unwrap()['authkey'] == AUTH_KEY

    def test_long_auth_key(self):
        """Test auth key with long arg version."""
        response = self.parser([ACTION, '--authkey', AUTH_KEY, '-o', OUTPUT])
        assert is_successful(response)
        assert response.unwrap()['authkey'] == AUTH_KEY

    def test_short_p360_base_url_key(self):
        """Test p360 base url key with short arg version."""
        response = self.parser(MINIMUN_KEYS_LIST + ('-pbu', BASE_URL))
        assert is_successful(response)
        assert response.unwrap()['p360_base_url'] == BASE_URL

    def test_long_p360_base_url_key(self):
        """Test p360 base url key with long arg version."""
        response = self.parser(
            MINIMUN_KEYS_LIST + ('--p360_base_url', BASE_URL),
        )
        assert is_successful(response)
        assert response.unwrap()['p360_base_url'] == BASE_URL

    def test_default_keys(self):  # noqa: WPS218
        """Test default values of keys."""
        wrapped_response = self.parser(MINIMUN_KEYS_LIST)
        assert is_successful(wrapped_response)

        response = wrapped_response.unwrap()
        assert 'p360_base_url' not in response
        assert response['brreg_base_url'] == \
            'https://data.brreg.no/enhetsregisteret/api/'  # noqa: N400
        assert response['worklist'] == 'worklist.json'
        assert response['kommune_numbers'] == '0301'
        assert response['cached'] is False
        assert response['error_margin'] == DEFAULT_ERROR_MARGIN

    def test_short_brreg_base_url_key(self):
        """Test brreg base url key with short arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + ('-bu', BRREG_BASE_URL))
        assert is_successful(response)
        assert response.unwrap()['brreg_base_url'] == BRREG_BASE_URL

    def test_long_brreg_base_url_key(self):
        """Test brreg base url key with long arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + (
            '--brreg_base_url',
            BRREG_BASE_URL,
        ))
        assert is_successful(response)
        assert response.unwrap()['brreg_base_url'] == BRREG_BASE_URL

    def test_short_worklist_key(self):
        """Test worklist key with short arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + ('-w', WORKLIST))
        assert is_successful(response)
        assert response.unwrap()['worklist'] == WORKLIST

    def test_long_worklist_key(self):
        """Test worklist key with long arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + (
            '--worklist',
            WORKLIST,
        ))
        assert is_successful(response)
        assert response.unwrap()['worklist'] == WORKLIST

    def test_short_kommune_numbers_key(self):
        """Test kommune numbers key with short arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + ('-kn', KOMMUNE_NUMBERS))
        assert is_successful(response)
        assert response.unwrap()['kommune_numbers'] == KOMMUNE_NUMBERS

    def test_long_kommune_numbers_key(self):
        """Test kommune numbers key with long arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + (
            '--kommune_numbers',
            KOMMUNE_NUMBERS,
        ))
        assert is_successful(response)
        assert response.unwrap()['kommune_numbers'] == KOMMUNE_NUMBERS

    def test_short_cached_key(self):
        """Test cached key with short arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + ('-c',))
        assert is_successful(response)
        assert response.unwrap()['cached'] is True

    def test_long_cached_key(self):
        """Test cached key with long arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + ('--cached',))
        assert is_successful(response)
        assert response.unwrap()['cached'] is True

    def test_short_dry_key(self):
        """Test dry key with short arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + ('-d',))
        assert is_successful(response)
        assert response.unwrap()['dry'] is True

    def test_long_dry_key(self):
        """Test dry key with long arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + ('--dry',))
        assert is_successful(response)
        assert response.unwrap()['dry'] is True

    def test_short_error_margin_key(self):
        """Test error margin key with short arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + ('-em', ERROR_MARGIN))
        assert is_successful(response)
        assert response.unwrap()['error_margin'] == int(ERROR_MARGIN)

    def test_long_error_margin_key(self):
        """Test error margin key with long arg key."""
        response = self.parser(MINIMUN_KEYS_LIST + (
            '--error_margin',
            ERROR_MARGIN,
        ))
        assert is_successful(response)
        assert response.unwrap()['error_margin'] == int(ERROR_MARGIN)

    def test_invalid_action_key(self):
        """Test invalid action key."""
        response = self.parser(['clean_code', '-ak', AUTH_KEY])

        string = 'error: argument action: invalid choice: {0}{1}{2}'.format(
            "'clean_code' (choose from 'test', 'cache_enterprises', ",
            "'duplicates', 'enrich', 'update', 'brreg_synchronize', ",
            "'synchronize')",
        )

        assert not is_successful(response)
        assert string in response.failure().args[0]
