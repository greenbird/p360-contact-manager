# -*- coding: utf-8 -*-

"""Package to get list of duplicate enterprises in ContactService API."""

import argparse

from attr import dataclass
from returns.result import safe
from typing_extensions import Final, final

DEFAULT_ERROR_MARGIN: Final[int] = 50


class SafeArgumentParser(argparse.ArgumentParser):
    """Change default ArgumentParser Error to Exception on failure."""

    def exit(self, status=0, message=None):  # noqa: A003, WPS125
        """Raise Exception on failure."""
        if status:
            raise Exception(r'Error: {message}'.format(
                message=message,
            ))
        exit(status)  # noqa: WPS421


@final
@dataclass(frozen=True, slots=True)
class ArgsParser(object):
    """Parse command-line arguments."""

    _parser = SafeArgumentParser(
        description='Public 360 Contact Service Enterprise manager',
    )

    @safe
    def __call__(self, args):
        """Parse command-line arguments."""
        self._add_arguments()
        return self._parser.parse_args(args)

    def _add_arguments(self) -> None:
        self._parser.add_argument(
            'action',
            choices=[
                'test',
                'cache_enterprises',
                'find_malformed_external',
                'find_malformed_internal',
                'duplicates',
                'enrich',
                'update',
                'brreg_synchronize',
                'synchronize',
            ],
            help='test connection, cache enterprises, worklist, remove, enrich',
        )

        self._parser.add_argument(
            '-ak',
            '--authkey',
            type=str,
            required=True,
            help='Autorization key for ContactService API',
        )

        self._parser.add_argument(
            '-pbu',
            '--p360_base_url',
            type=str,
            help='Base url to ContactService API',
            default=None,
        )

        self._parser.add_argument(
            '-bu',
            '--brreg_base_url',
            type=str,
            help='Base url to Brønnoysundregisteret API',
            default='https://data.brreg.no/enhetsregisteret/api/',
        )

        self._parser.add_argument(
            '-w',
            '--worklist',
            type=str,
            help='worklist to use when updating',
            default='remove_worklist.json',
        )

        self._parser.add_argument(
            '-kn',
            '--kommune_numbers',
            type=str,
            help='Comma seperated list of norwegian Kommune numbers',
            default='0301',  # oslo
        )

        self._parser.add_argument(
            '-c',
            '--cached',
            action='store_true',
            default=False,
            help='use data from cache.json',
        )

        self._parser.add_argument(
            '-d',
            '--dry',
            action='store_true',
            default=False,
            help='This will prevent any updates from actually being sent in remove',  # noqa: E501
        )

        self._parser.add_argument(
            '-em',
            '--error_margin',
            type=int,
            default=DEFAULT_ERROR_MARGIN,
            help='After failure to update has happened x times, program will stop',  # noqa: E501
        )
