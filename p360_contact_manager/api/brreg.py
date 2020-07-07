# -*- coding: utf-8 -*-

"""Code to get organizations from brreg.no api."""

import logging
from typing import Callable

from attr import dataclass
from returns.functions import tap
from returns.pipeline import pipeline
from returns.result import Result, safe
from typing_extensions import final


@final
@dataclass(frozen=True, slots=True)
class GetOrganization(object):
    """Produce a list of Organizations."""

    _brreg_base_url: str
    _get: Callable

    _entities = 'enheter/'
    _sub_entities = 'underenheter/'

    @pipeline
    def __call__(
        self,
        organization_number: str,
    ) -> Result[dict, Exception]:
        """Call api get list and write to file."""
        return self._call_brreg(
            self._entities, organization_number,
        ).rescue(
            lambda _: self._call_brreg(
                self._sub_entities, organization_number,
            ),
        )

    @safe
    def _call_brreg(self, endpoint, org_no) -> dict:
        response = self._get(
            self._brreg_base_url + endpoint + org_no,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()


@final
@dataclass(frozen=True, slots=True)
class GetOrganizations(object):
    """Get a list of organizations with the given criteria."""

    _brreg_base_url: str
    _get: Callable

    _entities = 'enheter/'
    _sub_entities = 'underenheter/'

    _log = logging.getLogger('api.brreg.GetOrganizations')

    @pipeline
    def __call__(
        self,
        search_criteria: dict,
        timeout: int = 20,
    ) -> Result[list, Exception]:
        """Call api with the search criteria and and return list."""
        return self._get(
            self._brreg_base_url + self._entities,
            search_criteria,
            timeout,
        ).alt(
            tap(self._log.warning),
        ).map(
            lambda response: response.json(),
        )


@final
@dataclass(frozen=True, slots=True)
class GetAllOrganizations(object):
    """Get a list of organizations with the given criteria."""

    _get_organizations: Callable

    _log = logging.getLogger('api.brreg.GetAllOrganizations')
    _brreg_max_enterprises: int = 10000

    @safe
    def __call__(
        self,
        search_criteria: dict,
        timeout: int = 20,
    ) -> list:
        """Call api with the search criteria and and return list."""
        business_types = search_criteria['naeringskode'].split(',')
        kommune_numbers = search_criteria['kommunenummer'].split(',')
        search_criteria['naeringskode'] = business_types[0]

        all_orgs: list = []

        for kommune_number in kommune_numbers:
            for business_type in business_types:
                search_criteria['page'] = 0
                search_criteria['naeringskode'] = business_type
                search_criteria['kommunenummer'] = kommune_number

                self._log.info(
                    'Current search criteria %s', search_criteria,
                )

                self._paginator(search_criteria).map(
                    all_orgs.extend,
                ).alt(
                    tap(self._log.warning),
                )

        return all_orgs

    @safe
    def _paginator(self, search_criteria) -> list:
        aggregated_data = self._get_organizations(search_criteria).unwrap()
        page = aggregated_data.get('page')
        total_elements = page.get('totalElements')
        self._log.info(
            '%s elements in %s pages',
            page.get('totalElements'),
            page.get('totalPages'),
        )

        if total_elements < 1:
            return []

        if total_elements > self._brreg_max_enterprises:
            error = 'Number of results exceedes 10 000'
            raise RuntimeError(error)

        for page_number in range(1, page.get('totalPages')):
            search_criteria['page'] = page_number

            self._call_api(search_criteria).map(
                aggregated_data['_embedded']['enheter'].extend,
            ).alt(
                tap(self._log.warning),
            )

        return aggregated_data['_embedded']['enheter']

    @pipeline
    def _call_api(self, search_criteria) -> Result[list, Exception]:
        return self._get_organizations(
            search_criteria,
        ).map(
            lambda response: response.get('_embedded').get('enheter'),
        ).alt(
            tap(self._log.warning),
        )
