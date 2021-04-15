import logging
from abc import ABC
from typing import Optional, Any, TYPE_CHECKING, Union, Iterable, IO, Tuple, Generator, \
    Mapping, MutableMapping

import requests
from requests import PreparedRequest, HTTPError
from requests.models import Response

from arago.extension.requests import HiroAuthBase
from arago.hiro.client.exception import HiroClientError, OntologyValidatorError, HiroServerError

if TYPE_CHECKING:
    from arago.hiro.client.client import HiroClient

logger = logging.getLogger(__name__)


def http_debug(arg: requests.models.Response, title: str = None) -> str:
    import json

    def redact_authorization_req_data(data: MutableMapping[str, str]) -> None:
        if all([v in data for v in [
            'client_id',
            'client_secret',
            'username',
            'password',
        ]]):
            data['client_secret'] = '[...]'
            data['password'] = '[...]'

    def redact_authorization_res_data(data: MutableMapping[str, str]) -> None:
        if all([v in data for v in [
            '_TOKEN',
            '_APPLICATION',
            '_IDENTITY',
            '_IDENTITY_ID',
            'expires-at',
            'type',
        ]]):
            data['_TOKEN'] = '[...]'

    def redact_authorization_token(value: str) -> str:
        tokens = value.split(' ')
        tokens[1] = '[...]'
        tokens = tokens[0:2]
        value = ' '.join(tokens)
        return value

    def curl_cmd(http_request, method, uri, headers, content_length, content_type):
        result = 'curl'
        if method != 'GET':
            result += f' -X {method}'
        for field, value in headers.items():
            if field in [
                'Content-Length',
                'Cache-Control',
                'Connection',
                'Accept',
                'Accept-Encoding',
                'User-Agent',
            ]:
                continue
            if field.lower() == 'authorization' and '[...]' in value:
                value = value.replace('[...]', '$HIRO_TOKEN')
            result += f' -H "{field}: {value}"'
        if content_length and content_type:
            if content_type.lower().startswith('application/json'):
                body = json.loads(http_request.body)
                redact_authorization_req_data(body)
                body = json.dumps(body)
                result += f" -d '{body}'"
        result += f" '{uri}'"
        result += '\n'
        return result

    def request(http_request: PreparedRequest) -> str:
        method = http_request.method.upper()
        uri = http_request.url

        headers = http_request.headers.copy()
        content_length = headers['content-length'] if 'content-length' in headers else None
        content_type = headers['content-type'] if 'content-type' in headers else None
        if 'authorization' in headers:
            headers['Authorization'] = redact_authorization_token(headers['Authorization'])

        result = '# ' + curl_cmd(http_request, method, uri, headers, content_length, content_type)

        result += f'{method} {uri}\n'  # request line

        field: str
        value: str
        for field, value in headers.items():
            result += f'{field}: {value}\n'

        result += '\n'  # separate header with body

        if content_length:
            if content_type:
                if content_type.lower().startswith('application/json'):
                    body = json.loads(http_request.body)
                    redact_authorization_req_data(body)
                    body = json.dumps(body, indent=2)
                    result += body
                    result += '\n'

        return result

    def response(http_response: Response) -> str:
        headers = http_response.headers
        content_length = headers['content-length'] if 'content-length' in headers else None
        content_type = headers['content-type'] if 'content-type' in headers else None

        result = ''

        version = http_response.raw.version
        if version == 10:
            version = 'HTTP/1.0'
        elif version == 11:
            version = 'HTTP/1.1'

        result += '%s %s %s\n' % (version, http_response.raw.status, http_response.raw.reason)

        field: str
        value: str
        for field, value in headers.items():
            result += '%s: %s\n' % (field, value)

        result += '\n'  # separate header with body

        if content_length:
            if content_type:
                if content_type.lower().startswith('application/json'):
                    text = http_response.text
                    if text:
                        body = json.loads(text)
                        redact_authorization_res_data(body)
                        body = json.dumps(body, indent=2)
                        result += body
                        result += '\n'

        return result

    separator = '###'
    if title is not None:
        separator += ' ' + title
    separator += '\n'

    message = separator + '\n'
    message += request(arg.request)
    message += '### <>\n'
    message += response(arg)

    return message


class HiroRestBaseClient(ABC):
    endpoint: Optional[str]
    base_url: Optional[str]
    session: Optional[requests.Session]
    authenticator: Optional[HiroAuthBase]
    parent: Optional['HiroRestBaseClient']
    root: Optional['HiroClient']

    def __init__(self, parent: Optional['HiroRestBaseClient'] = None) -> None:
        if parent is None:
            self.endpoint = None
            self.base_url = None
            self.session = None
            self.authenticator = None
            self.parent = None
            self.root = None
        else:
            self.endpoint = parent.endpoint
            self.base_url = parent.base_url
            self.session = parent.session
            self.authenticator = parent.authenticator
            self.parent = parent
            self.root = parent.root

    def fork(self, append_uri_path: Optional[str] = None) -> 'HiroRestBaseClient':
        client = HiroRestBaseClient(self)
        if append_uri_path:
            client.base_url += append_uri_path
        return client

    # TODO get client for api by api name

    def request(
            self,
            method: str,
            uri: Union[str, bytes],
            params: Optional[Union[bytes, Mapping[str, str]]] = None,
            headers: Optional[Mapping[str, str]] = None,
            data: Optional[Union[
                str, bytes,
                Mapping[str, Any],
                Iterable[Tuple[str, Optional[str]]],
                Generator[Union[str, bytes], None, None], IO]
            ] = None,
            json: Optional[Any] = None,
            stream: Optional[bool] = None,
            debug: Optional[bool] = None,
            recover_888: Optional[bool] = None,
    ) -> Response:
        method = method.upper()
        url = f'{self.base_url}{uri}'
        # TODO add 888 transaction rollback recover hook
        # https://requests.readthedocs.io/en/master/user/advanced/#event-hooks
        # https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/index.html#error-codes
        # https://requests.readthedocs.io/en/master/_modules/requests/auth/#HTTPDigestAuth
        if recover_888 is True:
            hooks = None
            raise NotImplementedError()
        else:
            hooks = None
        response = self.session.request(
            method=method, url=url, params=params,
            headers=headers,
            data=data, json=json,
            stream=stream, hooks=hooks)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(http_debug(response))
        try:
            response.raise_for_status()
        except HTTPError as e:
            with response:
                if 400 <= response.status_code < 500:
                    if response.headers['Content-Type'].lower().startswith('application/json'):
                        res_data = response.json()
                        if OntologyValidatorError.is_validator_error(res_data):
                            raise OntologyValidatorError(res_data) from e
                        else:
                            error = res_data['error']
                            if logger.isEnabledFor(logging.DEBUG):
                                logger.debug(http_debug(response))
                            else:
                                raise HiroClientError(error['message']) from e
                    else:
                        raise HiroServerError(response.reason) from e
                elif 500 <= response.status_code < 600:
                    if response.headers['Content-Type'].lower().startswith('application/json'):
                        res_data = response.json()
                        error = res_data['error']
                        raise HiroServerError(error['message']) from e
                    else:
                        raise HiroServerError(response.reason) from e
                else:
                    raise e
        return response
