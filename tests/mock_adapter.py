import json
import os

import dingus

from aweber_api import AWeberUser
from aweber_api import OAuthAdapter

__all__ = ['MockAdapter']


responses = {
    'GET' : {
        '/accounts':                                ({}, 'accounts/page1'),
        '/accounts/1':                              ({}, 'accounts/1'),
        '/accounts/1?ws.op=findSubscribers&' \
                         'email=joe%40example.com': ({}, 'accounts/findSubscribers'),
        '/accounts/1?ws.op=findSubscribers&' \
                         'email=joe%40example.com&' \
                         'ws.show=total_size': ({}, 'accounts/findSubscribers_ts'),
        '/accounts/1?ws.op=getWebForms':             ({}, 'accounts/webForms'),
        '/accounts/1?ws.op=getWebFormSplitTests':    ({}, 'accounts/webFormSplitTests'),
        '/accounts/1/lists':                         ({}, 'lists/page1'),
        '/accounts/1/lists?ws.start=20&ws.size=20':  ({}, 'lists/page2'),
        '/accounts/1/lists/303449':                  ({}, 'lists/303449'),
        '/accounts/1/lists/505454':                  ({}, 'lists/505454'),
        '/accounts/1/lists/303449/any_collection':   ({}, 'any_collection/page1'),
        '/accounts/1/lists/303449/any_collection/1': ({}, 'any_collection/1'),
        '/accounts/1/lists/303449/campaigns':        ({}, 'campaigns/303449'),
        '/accounts/1/lists/303449/custom_fields':    ({}, 'custom_fields/303449'),
        '/accounts/1/lists/505454/custom_fields':    ({}, 'custom_fields/505454'),
        '/accounts/1/lists/303449/custom_fields/1':  ({}, 'custom_fields/1'),
        '/accounts/1/lists/303449/custom_fields/2':  ({}, 'custom_fields/2'),
        '/accounts/1/lists/303449/subscribers':      ({}, 'subscribers/page1'),
        '/accounts/1/lists/303449/subscribers/1':    ({}, 'subscribers/1'),
        '/accounts/1/lists/303449/subscribers/2':    ({}, 'subscribers/2'),
        '/accounts/1/lists/505454/subscribers/3':    ({}, 'subscribers/3'),
        '/accounts/1/lists/303449/subscribers/1?ws.op=getActivity': (
            {}, 'subscribers/get_activity'),
        '/accounts/1/lists/303449/subscribers/1?ws.op=getActivity&ws.show=total_size': (
            {}, 'subscribers/get_activity_ts'),
        '/accounts/1/lists/303449/subscribers?ws.op=find&name=joe': (
            {'status': '400'}, 'error'),
        '/accounts/1?ws.op=findSubscribers&name=bob': (
            {'status': '400'}, 'error'),
        '/accounts/1/lists/303449/subscribers?ws.op=find&' \
                         'email=joe%40example.com': ({}, 'subscribers/find'),
        '/accounts/1/lists/303449/subscribers?ws.op=find&' \
                         'email=joe%40example.com&' \
                         'ws.show=total_size': ({}, 'subscribers/find_ts'),
    },
    'POST' : {
        '/accounts/1/lists/303449/any_collection':  ({
            'status': '201',
            'location': '/accounts/1/lists/303449/any_collection/1'}, None),
        '/accounts/1/lists/303449/custom_fields': ({
            'status': '201',
            'location': '/accounts/1/lists/303449/custom_fields/2'}, None),
        '/accounts/1/lists/505454/custom_fields': ({
            'status': '400'}, 'custom_fields/error'),
        '/accounts/1/lists/303449/subscribers/1': ({
            'status': '201',
            'location': '/accounts/1/lists/505454/subscribers/3'}, None),
    },
    'PATCH' : {
        '/accounts/1/lists/303449/subscribers/1': ({'status': '209'}, None),
        '/accounts/1/lists/303449/subscribers/2': ({'status': '400'}, 'error'),
    },
    'DELETE' : {
        '/accounts/1/lists/303449/subscribers/1': ({'status': '200'}, None),
        '/accounts/1/lists/303449/subscribers/2': ({'status': '400'}, 'error'),
    }
}

def request(self, url, method, **kwargs):
    """Return a tuple to simulate calling oauth2.Client.request."""
    (headers, file) = responses[method][url]
    if 'status' not in headers:
        # assume 200 OK if not otherwise specified
        headers['status'] = '200'
    if file is None:
        return (headers, '')
    path = os.sep.join(__file__.split(os.sep)[:-1]+['data',''])
    filename = "{0}{1}.json".format(path, file)
    data = open(filename).read()
    return (headers, data)


class MockAdapter(OAuthAdapter):
    """Mocked OAuthAdapter."""
    requests = []

    @dingus.patch('oauth2.Client.request', request)
    def request(self, method, url, data={}, response='body'):
        """Mock the oauth.Client.request method"""
        req = super(MockAdapter, self).request(method, url, data, response)
        self.requests.append({'method' : method, 'url' : url, 'data' : data})
        return req

    def __init__(self):
        self.user = AWeberUser()
        return super(MockAdapter, self).__init__('key', 'secret', '')
