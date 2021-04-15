from typing import Final

import pytest

from arago.extension.requests import HiroPasswordAuth
from arago.hiro.client.client import HiroClient
from arago.hiro.model.auth import SessionCredentials
from arago.hiro.model.probe import Version


class TestClassProbe:
    ENDPOINT_5: Final[str] = 'https://hiro5.ai-projects.co:8443'
    ENDPOINT_6: Final[str] = 'https://pod1159.saasarago.com'
    ENDPOINT_7: Final[str] = 'https://eu-stagegraph.arago.co'

    @pytest.fixture
    def client_5(self, credentials: SessionCredentials) -> HiroClient:
        client = HiroClient()
        client.configure(TestClassProbe.ENDPOINT_5, HiroPasswordAuth(client, credentials))
        yield client

    @pytest.fixture
    def client_6(self, credentials: SessionCredentials) -> HiroClient:
        client = HiroClient()
        client.configure(TestClassProbe.ENDPOINT_6, HiroPasswordAuth(client, credentials))
        yield client

    @pytest.fixture
    def client_7(self, credentials: SessionCredentials) -> HiroClient:
        client = HiroClient()
        client.configure(TestClassProbe.ENDPOINT_7, HiroPasswordAuth(client, credentials))
        yield client

    @pytest.mark.skip
    def test_five_five(self, client_5: HiroClient):
        from arago.hiro.backend.five.probe import Hiro5ProbeModel
        assert Hiro5ProbeModel(client_5).probe() is Version.HIRO_5

    @pytest.mark.skip
    def test_five_six(self, client_5: HiroClient):
        from arago.hiro.backend.six.probe import Hiro6ProbeModel
        assert Hiro6ProbeModel(client_5).probe() is None

    @pytest.mark.skip
    def test_five_seven(self, client_5: HiroClient):
        from arago.hiro.backend.seven.probe import Hiro7ProbeModel
        assert Hiro7ProbeModel(client_5).probe() is None

    def test_six_five(self, client_6: HiroClient):
        from arago.hiro.backend.five.probe import Hiro5ProbeModel
        assert Hiro5ProbeModel(client_6).probe() is None

    def test_six_six(self, client_6: HiroClient):
        from arago.hiro.backend.six.probe import Hiro6ProbeModel
        assert Hiro6ProbeModel(client_6).probe() is Version.HIRO_6

    def test_six_seven(self, client_6: HiroClient):
        from arago.hiro.backend.seven.probe import Hiro7ProbeModel
        assert Hiro7ProbeModel(client_6).probe() is None

    def test_seven_five(self, client_7: HiroClient):
        from arago.hiro.backend.five.probe import Hiro5ProbeModel
        assert Hiro5ProbeModel(client_7).probe() is None

    def test_seven_six(self, client_7: HiroClient):
        from arago.hiro.backend.six.probe import Hiro6ProbeModel
        assert Hiro6ProbeModel(client_7).probe() is None

    def test_seven_seven(self, client_7: HiroClient):
        from arago.hiro.backend.seven.probe import Hiro7ProbeModel
        assert Hiro7ProbeModel(client_7).probe() is Version.HIRO_7
