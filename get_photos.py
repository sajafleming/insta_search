"""query instagram api and return urls that match"""

from instagram.client import InstagramAPI
import urllib
import urllib2
import os
import json
import pprint

# endpoint for instagram api request
URL = "https://api.instagram.com/v1/tags/{}/media/recent?access_token={}"

def request_insta_data(tag, access_token=None):
    """Get instagram data based on tag"""

    # get access token from environment 
    access_token = os.environ['ACCESS_TOKEN']

    # add tag and token to request url
    url_request = URL.format(tag, access_token)

    # using the urllib2, make api call
    response = urllib2.urlopen(url_request)
    data = response.read()
    pic_info = json.loads(data)

    final_urls = []

    # add url for every pic
    for i in range(len(pic_info['data'])):
        url = pic_info['data'][i]['images']['low_resolution']['url']
        final_urls.append(url)

    return final_urls

# print request_insta_data('LGB')


# data = request_insta_data('LGB')
# print data

# pp = pprint.PrettyPrinter(indent=1)
# # pp.pprint(data['data'])

# for i in range(len(data['data'])):
#     print data['data'][i]['images']['low_resolution']['url']
#     print "##############################"

# print data["pagination"]["url"]

# https://api.instagram.com/v1/tags/{tag-name}/media/recent?access_token=ACCESS-TOKEN