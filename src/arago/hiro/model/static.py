from typing import Mapping, Optional

VERSION_FIVE_RESULT: Mapping[str, Mapping[str, Optional[str]]] = {
    'auth': {
        'endpoint': '/oauth2',
        'docs': 'https://docs.hiro.arago.co/hiro/5.4.5/developer/hiro-graph-api/index.html#how-to-get-a-token',
        'protocols': None,
    },
    'graph': {
        'endpoint': '/',
        'docs': 'https://docs.hiro.arago.co/hiro/5.4.5/developer/hiro-graph-api/rest-api.html',
        'protocols': None,
    },
    'app': {
        'endpoint': None,
    },
    'iam': {
        'endpoint': None,
    },
    'events-ws': {
        'endpoint': '/_events',
        'docs': 'https://docs.hiro.arago.co/hiro/5.4.5/developer/hiro-graph-api/ws-api.html#ws-event-streaming-api',
        'protocols': 'events-1.0.0',
    },
    'identity': {
        'endpoint': '/_me',
        'docs': 'https://docs.hiro.arago.co/hiro/5.4.5/developer/hiro-graph-api/rest-api.html#_me_get',
        'protocols': None,
    },
    'graph-ws': {
        'endpoint': '/_g',
        'docs': 'https://docs.hiro.arago.co/hiro/5.4.5/developer/hiro-graph-api/ws-api.html#ws-graph-api-graph-2-0-0',
        'protocols': 'graph-2.0.0',
    },
    'health': {
        'endpoint': '/_health',
        'docs': 'https://docs.hiro.arago.co/hiro/5.4.5/developer/hiro-graph-api/rest-api.html#_health_get',
        'protocols': None,
    },
    'info': {
        'endpoint': '/info',
        'docs': None,
        'protocols': None,
    },
}

VERSION_SIX_RESULT: Mapping[str, Mapping[str, Optional[str]]] = {
    'auth': {
        'endpoint': '/api/6/auth',
        'docs': 'https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/auth-rest-api.html',
        'protocols': None,
    },
    'graph': {
        'endpoint': '/',
        'docs': 'https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/rest-api.html',
        'protocols': None,
    },
    'app': {
        'endpoint': '/api/6/app',
        'docs': 'https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/app-rest-api.html',
        'protocols': None,
    },
    'iam': {
        'endpoint': '/api/6/iam',
        'docs': 'https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/iam-rest-api.html',
        'protocols': None,
    },
    'events-ws': {
        'endpoint': '/_events',
        'docs': 'https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/ws-api.html#ws-event-streaming-api',
        'protocols': 'events-1.0.0',
    },
    'identity': {
        'endpoint': '/_me',
        'docs': 'https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/rest-api.html#_me_get',
        'protocols': None,
    },
    'graph-ws': {
        'endpoint': '/_g',
        'docs': 'https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/ws-api.html#ws-graph-api-graph-2-0-0',
        'protocols': 'graph-2.0.0',
    },
    'health': {
        'endpoint': '/_health',
        'docs': 'https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/rest-api.html#_health_get',
        'protocols': None,
    },
    'info': {
        'endpoint': '/info',
        'docs': None,
        'protocols': None,
    },
}
NAMESPACE_BASE_URI = 'http://www.purl.org/'
