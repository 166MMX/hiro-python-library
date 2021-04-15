import threading
from abc import ABC, abstractmethod
from typing import Callable, TYPE_CHECKING, Optional, Final, overload

from requests import PreparedRequest, Response
from requests.auth import AuthBase, extract_cookies_to_jar
from urllib3.util import url as url_utils

from arago.hiro.model.auth import SessionCredentials, AccessToken

if TYPE_CHECKING:
    from arago.hiro.client.client import HiroClient


class AuthLocal(threading.local):
    pos: Optional[int] = None
    num_401_calls: Optional[int] = None


class HiroAuthBase(AuthBase, ABC):
    __token: Optional[AccessToken]
    _thread_local: Final[AuthLocal]
    path_is_excluded: Callable[[str], bool]
    recover_401: bool

    def __init__(self) -> None:
        super().__init__()
        self.__token = None
        self._thread_local = AuthLocal()
        # self.excluded_paths: List[Callable[[str], bool]] = []
        self.path_is_excluded = lambda path: False
        self.recover_401 = True

    @overload
    def exclude_path(self, literal: str):
        ...

    @overload
    def exclude_path(self, startswith: str):
        ...

    @overload
    def exclude_path(self, endswith: str):
        ...

    def exclude_path(self, **kwargs):
        if 'literal' in kwargs:
            value = kwargs['literal']

            def func(path: str) -> bool:
                return path == value
        elif 'startswith' in kwargs:
            value = kwargs['startswith']

            def func(path: str) -> bool:
                return path.startswith(value)
        elif 'endswith' in kwargs:
            value = kwargs['endswith']

            def func(path: str) -> bool:
                return path.endswith(value)
        else:
            raise RuntimeError('''keyword must be one of {'literal','startswith','endswith'}''')
        old_func = self.path_is_excluded
        self.path_is_excluded = lambda path: old_func(path) or func(path)

    # https://docs.hiro.arago.co/hiro/6.2.0/user/general-information/release-notes/release-user-6.1.1.html#backend-changes
    def apply_authorization_header(self, r: PreparedRequest) -> None:
        r.headers['Authorization'] = 'Bearer %s' % self.token.value

    def handle_401(self, r: Response, **kwargs) -> Response:
        if r.status_code != 401:
            return r

        if r.headers['Content-Type'].lower() == 'application/json':
            res_data = r.json()
            try:
                message = res_data['error']['message']
            except KeyError:
                return r
            if message != 'token invalid':
                return r

        if self._thread_local.pos is not None:
            # Rewind the file position indicator of the body to where
            # it was to resend the request.
            # noinspection PyUnresolvedReferences
            r.request.body.seek(self._thread_local.pos)

        if self._thread_local.num_401_calls < 2:
            self._thread_local.num_401_calls += 1

            # Consume content and release the original connection
            # to allow our new request to reuse the same one.
            # noinspection PyStatementEffect
            r.content
            r.close()
            prep = r.request.copy()
            # noinspection PyUnresolvedReferences,PyProtectedMember
            extract_cookies_to_jar(prep._cookies, r.request, r.raw)
            # noinspection PyUnresolvedReferences,PyProtectedMember
            prep.prepare_cookies(prep._cookies)

            self.invalidate_token()

            self.apply_authorization_header(prep)

            # noinspection PyUnresolvedReferences
            _r = r.connection.send(prep, **kwargs)
            _r.history.append(r)
            _r.request = prep

            return _r

        self._thread_local.num_401_calls = 1
        return r

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        parsed_url = url_utils.parse_url(r.url)
        if self.path_is_excluded(parsed_url.path):
            return r

        self.apply_authorization_header(r)

        if self.recover_401:
            try:
                # noinspection PyUnresolvedReferences
                self._thread_local.pos = r.body.tell()
            except AttributeError:
                # In the case of HTTPDigestAuth being reused and the body of
                # the previous request was a file-like object, pos has the
                # file position of the previous body. Ensure it's set to
                # None.
                self._thread_local.pos = None

            r.register_hook('response', self.handle_401)
            self._thread_local.num_401_calls = 1

        return r

    def invalidate_token(self) -> None:
        self.__token = None

    @abstractmethod
    def get_new_token(self) -> AccessToken:
        ...

    @property
    def is_token_valid(self) -> bool:
        token = self.__token
        return token is not None and token.valid

    @property
    def token(self) -> AccessToken:
        # https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/authentication.html#obtaining-a-graph-application-token
        if self.is_token_valid:
            return self.__token

        self.__token = token = self.get_new_token()
        return token


class HiroPasswordAuth(HiroAuthBase):
    credentials: Final[SessionCredentials]
    client: Final['HiroClient']

    def __init__(
            self,
            client: 'HiroClient',
            credentials: SessionCredentials,
    ) -> None:
        super().__init__()
        self.client = client
        self.credentials = credentials

    def get_new_token(self) -> AccessToken:
        return self.client.model.auth.password(self.credentials)


class HiroConstantAuth(HiroAuthBase):
    __token: Final[AccessToken]

    def __init__(
            self,
            token: AccessToken
    ) -> None:
        super().__init__()
        self.__token = token

    def get_new_token(self) -> AccessToken:
        return self.__token
