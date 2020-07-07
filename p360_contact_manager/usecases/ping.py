# -*- coding: utf-8 -*-

"""Code to produce a list of organizations from ContactService api."""
from typing import Callable

from attr import dataclass
from returns.pipeline import pipeline
from returns.result import Result
from typing_extensions import final


@final
@dataclass(frozen=True, slots=True)
class Ping(object):
    """Call api/ping to test connection to p360."""

    _ping_p360: Callable

    @pipeline
    def __call__(self) -> Result[bool, Exception]:
        """Call ping function."""
        return self._ping_p360()
