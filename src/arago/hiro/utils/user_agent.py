import requests
import urllib3
from requests_toolbelt.utils import user_agent

import arago.hiro as hiro


def build_user_agent(name:str) -> str:
    return user_agent.UserAgentBuilder(
        name=name,
        version=hiro.__version__,
    ).include_implementation(
    ).include_system(
    ).include_extras((
        ('requests', requests.__version__),
        ('urllib3', urllib3.__version__),
    )).build()
