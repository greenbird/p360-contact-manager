# -*- coding: utf-8 -*-

"""Get all active enterprises and save to json file for later use."""
import json
from typing import Callable

from attr import dataclass
from returns.pipeline import pipeline
from returns.result import ResultE
from typing_extensions import final


@final
@dataclass(frozen=True, slots=True)
class CacheEnterprises(object):
    """Get all enterprises and write them to a json file."""

    _get_all_enterprises: Callable
    _write: Callable

    @pipeline(ResultE[bool])
    def __call__(self) -> ResultE[bool]:
        """Call api get list and write to file."""
        return self._get_all_enterprises().map(
            json.dumps,
        ).bind(
            self._write_file,
        )

    @pipeline(ResultE[bool])
    def _write_file(self, output_data) -> ResultE[bool]:
        return self._write(
            'cache.json',
            output_data,
        )
