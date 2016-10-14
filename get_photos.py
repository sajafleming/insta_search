from instagram.client import InstagramAPI
import urllib
import urllib2
import os
import json

URL = "https://api.instagram.com/v1/tags/{}/media/recent?access_token={}"

def request_insta_data(tag, access_token=None):
    """Get instagram data based on tag"""

    access_token = os.environ['ACCESS_TOKEN']

    url_request = URL.format(tag, access_token)
    print url_request

    response = urllib2.urlopen(url_request)
    data = response.read()

    return json.loads(data)

print request_insta_data('LGB')

# https://api.instagram.com/v1/tags/{tag-name}/media/recent?access_token=ACCESS-TOKEN