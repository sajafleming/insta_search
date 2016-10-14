"""query instagram api and return urls that match"""

from instagram.client import InstagramAPI
import urllib
import urllib2
import os
import json
import pprint

URL = "https://api.instagram.com/v1/tags/{}/media/recent?access_token={}"

def request_insta_data(tag, access_token=None):
    """Get instagram data based on tag"""

    access_token = os.environ['ACCESS_TOKEN']

    url_request = URL.format(tag, access_token)

    response = urllib2.urlopen(url_request)
    data = response.read()
    pic_info = json.loads(data)

    final_urls = []

    for i in range(len(pic_info['data'])):
        url = pic_info['data'][i]['images']['low_resolution']['url']
        final_urls.append(url)

    return final_urls

print request_insta_data('LGB')


# data = request_insta_data('LGB')
# print data

# pp = pprint.PrettyPrinter(indent=1)
# # pp.pprint(data['data'])

# for i in range(len(data['data'])):
#     print data['data'][i]['images']['low_resolution']['url']
#     print "##############################"

# print data["pagination"]["url"]

# https://api.instagram.com/v1/tags/{tag-name}/media/recent?access_token=ACCESS-TOKEN