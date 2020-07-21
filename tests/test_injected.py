from dependencies import Injector

from p360_contact_manager.injected import (
    BrregSynchronizeScope,
    CacheEnterprisesScope,
    DuplicatesScope,
    PingScope,
    SynchronizeScope,
    UpdateScope,
)

Scope = Injector.let(
    dry=True,
    authkey='authkey',
    error_margin=50,
    p360_base_url='p360_base_url/',
    brreg_base_url='brreg_base_url/',
    kommune_numbers='kommune_numbers',
    worklist='worklist',
    cache_file='cache.json',
)


def test_scope_dependency_injection():
    """Test that we dependency injection works."""
    injected_usecases = {
        BrregSynchronizeScope,
        CacheEnterprisesScope,
        DuplicatesScope,
        PingScope,
        SynchronizeScope,
        UpdateScope,
    }

    for usecase in injected_usecases:
        action = (Scope & usecase)

        # try to build it.
        built = action.run
        assert isinstance(built, object)
        assert callable(built)
