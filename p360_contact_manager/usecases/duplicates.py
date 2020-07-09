# -*- coding: utf-8 -*-

"""Code to produce a list of organizations from ContactService api."""

import json
import logging
from copy import deepcopy
from typing import Callable

from attr import dataclass
from returns.pipeline import is_successful, pipeline
from returns.result import Result, safe
from typing_extensions import Final, final

RECNO: Final[str] = 'Recno'
UPDATE: Final[str] = 'update'
SKIP: Final[str] = 'skip'


@final
@dataclass(frozen=True, slots=True)
class Duplicates(object):
    """Produce worklist that contains entries which has duplicates in p360."""

    _duplicate_worklist: str
    _update_payload: dict
    _get_all_enterprises: Callable
    _write: Callable

    _log = logging.getLogger('produce_list')

    @pipeline
    def __call__(self) -> Result[bool, Exception]:
        """Load enterprises, remove duplicates, restructure, write worklist."""
        return self._get_all_enterprises().bind(  # noqa: WPS221 allow complex
            self._group_by_org_no,
        ).bind(
            self._remove_non_duplicates,
        ).bind(
            self._restructure_data,
        ).bind(
            self._restructure_with_payload,
        ).map(
            json.dumps,
        ).bind(
            self._write_file,
        )

    @pipeline
    def _write_file(self, output_data) -> Result[bool, Exception]:
        return self._write(
            self._duplicate_worklist,
            output_data,
        )

    @safe
    def _group_by_org_no(self, payload) -> dict:

        grouped: dict = {}
        for enterprise in payload.get('Enterprises'):
            e_number = enterprise.get('EnterpriseNumber')
            # any enterprise without a number we will skip
            if not e_number:
                continue

            # any enterprise with 'recno:1' in categories are internal and
            # should be skipped
            if 'recno:1' in enterprise.get('Categories', []):
                continue

            if e_number not in grouped:
                grouped[e_number] = []

            grouped[e_number].append(enterprise)

        return grouped

    @safe
    def _remove_non_duplicates(self, payload) -> dict:

        for org_no in list(payload.keys()):
            if len(payload[org_no]) == 1:
                payload.pop(org_no)

        return payload

    @safe
    def _restructure_data(self, org_dict: dict) -> dict:
        restructured: dict = {UPDATE: [], SKIP: []}
        for orgno in org_dict:  # noqa: WPS528
            temp = self._restructure_with_skip(org_dict[orgno])
            if is_successful(temp):
                restructured[UPDATE].extend(temp.unwrap().get(UPDATE))
                restructured[SKIP].append(temp.unwrap().get(SKIP))
            else:
                self._log.warning('Unable to restructure data:')
                self._log.warning(org_dict[orgno])
        return restructured

    @safe
    def _restructure_with_skip(self, organizations: list) -> dict:
        restructured: dict = {}
        min_recno = organizations[0][RECNO]
        index = 0

        for list_index, org in enumerate(organizations):
            if org[RECNO] < min_recno:
                min_recno = org[RECNO]
                index = list_index

        restructured[SKIP] = organizations.pop(index)
        restructured[UPDATE] = organizations
        return restructured

    @safe
    def _restructure_with_payload(self, enterprises: dict) -> dict:

        update_list = []

        for enterprise in enterprises[UPDATE]:
            payload = deepcopy(self._update_payload)
            payload[RECNO] = enterprise[RECNO]
            update_list.append({
                'original_data': enterprise,
                'payload': {'parameters': payload},
            })

        enterprises[UPDATE] = update_list
        return enterprises