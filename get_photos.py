"""query instagram api and return urls that match"""

from instagram.client import InstagramAPI
import urllib
import urllib2
import os
import json
import pprint

NUM_RETRIES = 3

# endpoint for instagram api request
URL = "https://api.instagram.com/v1/tags/{}/media/recent?access_token={}"

def request_insta_data(tag, access_token=None):
    """Get instagram data based on tag"""

    # get access token from environment 
    access_token = os.environ['ACCESS_TOKEN']

    # add tag and token to request url
    url_request = URL.format(tag, access_token)

    for i in range(NUM_RETRIES):
        try:
            # using the urllib2, make api call
            response = urllib2.urlopen(url_request)
            data = response.read()
            break
        except:
            print "blah"

    pic_info = json.loads(data)

    return pic_info


# print request_insta_data('coffee')


# data = request_insta_data('coffee')
# print data