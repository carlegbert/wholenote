import json


def post_json(client, url, data, headers={}):
    """Send POST request with JSON data to specified URL.
    :url: URL string
    :data: Data dict
    :headers: Optional headers argument (usually will be authorization)
    :returns: Flask response object
    """
    return client.post(url, data=json.dumps(data),
                       content_type='application/json', headers=headers)


def put_json(client, url, data, headers={}):
    """Send PUT request with JSON data to specified URL.
    :url: URL string
    :data: Data dict
    :headers: Optional headers argument (usually will be authorization)
    :returns: Flask response object
    """
    return client.put(url, data=json.dumps(data),
                      content_type='application/json', headers=headers)


def get_json(response):
    """Unload JSON from Flask response.
    :response: Flask response object
    :returns: Data dict
    """
    return json.loads(response.data.decode('utf8'))
