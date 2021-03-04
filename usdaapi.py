#!env/bin/python

from json.decoder import JSONDecodeError

import requests

class USDA(requests.Session):
    """
    Class for interfacing with the USDA nutrition API.

    """
    def __init__(self, url=None, token=None, verify=True, **kwargs):
        super().__init__(**kwargs)

        if not url:
            url = 'https://api.nal.usda.gov/fdc/v1'

        self.url = url.rstrip('/')
        self.token = token

    def request(self, method, endpoint, params={}, data=None, json=None, check_response=True, **kwargs):

        from urllib.parse import urljoin

        result = None

        url = f'{self.url}{endpoint}'
        print(f'Inner: {url}')
        params.update(
            {
                'api_key': self.token
            }
        )

        response = super(USDA, self).request(
            method,
            url,
            params=params,
            data=data,
            json=json,
            **kwargs
        )

        if check_response:
            response.raise_for_status()

        try:
            result = response.json()
        except JSONDecodeError:
            print(f'Failed to decode JSON from response: {response.raw}')
            raise JSONDecodeError

        return result

    def search(self, search_string, data_type='Branded', limit=10):
        result = self.post(
            '/foods/search',
            json={
                'query': search_string,
                'dataType': [
                    data_type
                ],
                'pageSize': limit
            }
        )

        return result

    def get_details_by_id(self, *args):

        id_list = list(args)

        if not id_list:
            raise Exception('id_list cannot be empty.')

        result = self.get(
            '/foods',
            params={
                'fdcIds':  ','.join(id_list)
            }
        )

        return result
