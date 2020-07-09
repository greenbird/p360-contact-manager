# -*- coding: utf-8 -*-

"""Code to produce a list of organizations from ContactService api."""
import json
from copy import deepcopy
from typing import Callable

import requests
from attr import dataclass
from returns.pipeline import is_successful, pipeline
from returns.result import Result, safe
from typing_extensions import Final, final

URL_PARAM_AUTHKEY: Final[str] = 'authkey'


@final
@dataclass(frozen=True, slots=True)
class Ping(object):
    """Ping p360 endpoint."""

    _authkey: str
    _p360_base_url: str
    _post: Callable

    _dry: bool = False
    _endpoint = 'Ping'

    @pipeline
    def __call__(
        self,
        timeout: int = 10,
    ) -> Result[requests.Response, Exception]:
        """Call api get list and write to file."""
        if self._dry:
            return 'DRY RUN: No API calls executed'  # type: ignore

        return self._post(
            self._p360_base_url + self._endpoint,
            url_params={'authkey': self._authkey},
            payload={},
            timeout=timeout,
        )


@final
@dataclass(frozen=True, slots=True)
class UpdateEnterprise(object):
    """Produce a list of Organizations."""

    _authkey: str
    _p360_base_url: str
    _post: Callable

    _dry: bool = False
    _endpoint = 'UpdateEnterprise'

    @safe
    def __call__(
        self,
        payload: str,
        timeout: int = 10,
    ) -> requests.Response:
        """Call api get list and write to file."""
        if self._dry:
            return 'DRY RUN: No API calls executed'  # type: ignore

        response = self._post(
            self._p360_base_url + self._endpoint,
            url_params={URL_PARAM_AUTHKEY: self._authkey},
            payload=payload,
            timeout=timeout,
        )

        if not is_successful(response):
            raise response.failure()

        response_json = response.unwrap().json()

        if not response_json.get('Successful'):
            raise RuntimeError(response_json['ErrorMessage'])

        return response_json


@final
@dataclass(frozen=True, slots=True)
class SynchronizeEnterprise(object):
    """Produce a list of Organizations."""

    _authkey: str
    _p360_base_url: str
    _post: Callable

    _dry: bool = False
    _endpoint = 'SynchronizeEnterprise'

    @safe
    def __call__(
        self,
        payload: str,
        timeout: int = 20,
    ) -> requests.Response:
        """Call api syncronize endpoint with given payload."""
        if self._dry:
            return 'DRY RUN: No API calls executed'  # type: ignore

        response = self._post(
            self._p360_base_url + self._endpoint,
            url_params={URL_PARAM_AUTHKEY: self._authkey},
            payload=payload,
            timeout=timeout,
        )

        if not is_successful(response):
            raise response.failure()

        response_json = response.unwrap().json()

        if not response_json.get('Successful'):
            raise RuntimeError(response_json['ErrorMessage'])

        return response_json


@final
@dataclass(frozen=True, slots=True)
class GetEnterprises(object):
    """Call get enterprises endpoint with given payload."""

    _authkey: str
    _p360_base_url: str
    _post: Callable

    _endpoint = 'GetEnterprises'

    @safe
    def __call__(
        self,
        payload: str,
        timeout: int = 20,
    ) -> requests.Response:
        """Call api get list and write to file."""
        response = self._post(
            self._p360_base_url + self._endpoint,
            url_params={URL_PARAM_AUTHKEY: self._authkey},
            payload=payload,
            timeout=timeout,
        )

        if not is_successful(response):
            raise response.failure()

        response_json = response.unwrap().json()

        if not response_json.get('Successful'):
            raise RuntimeError(response_json['ErrorMessage'])

        if not response_json.get('Enterprises'):
            raise ValueError('No enterprises found')

        return response_json


@final
@dataclass(frozen=True, slots=True)
class GetAllEnterprises(object):
    """Call p360 api and return all enterprises."""

    _get_enterprises: Callable
    _base_payload: dict

    @safe
    def __call__(self) -> Result[dict, Exception]:
        """Use payload and get all enterprises."""
        payload = deepcopy(self._base_payload)

        aggregated = self._get_enterprises(payload).unwrap()
        # create reference to enterprises array in first request

        for page in range(1, aggregated['TotalPageCount']):
            payload['parameter']['Page'] = page

            self._call_api(payload).map(
                # Add to enterprises list in aggregated result.
                aggregated['Enterprises'].extend,
            )

        return aggregated

    @pipeline
    def _call_api(self, payload) -> Result[list, Exception]:

        return self._get_enterprises(payload).map(
            lambda response: response.get('Enterprises'),
        )


@final
@dataclass(frozen=True, slots=True)
class GetAllCachedEnterprises(object):
    """Get return contents of cache.json if exists."""

    _read: Callable
    _cache_file: str

    @pipeline
    def __call__(self) -> Result[dict, Exception]:
        """Read data load to json and return."""
        return self._read(self._cache_file, 'r').map(
            json.loads,
        )