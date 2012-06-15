#!/usr/bin/env python2
# -*- coding: utf8 -*-
"""
Python interface to Twitpic photostreams
Author: András Veres-Szentkirályi <vsza@vsza.hu>
License: MIT
"""

from __future__ import with_statement
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from lxml import etree
from urllib import urlretrieve
from time import mktime, strptime
import json, requests, os

HTML_PARSER = etree.HTMLParser()
USER_PHOTO_XPATH = etree.XPath('//div[@class="user-photo-wrap"]/div/a/@href')
FULL_PHOTO_XPATH = etree.XPath('//div[@id="media-full"]/img/@src')
TWITPIC_API = 'http://api.twitpic.com/2/media/show.json?id={pid}'
TWITPIC_FMT = '%Y-%m-%d %H:%M:%S'

class Fetcher(object):
    """Fetches photostreams of Twitpic users into a file cache"""
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

    def fetch_photos(self, user):
        """Fetch up to 20 photos of a user"""
        user_cache_dir = os.path.join(self.cache_dir, user)
        if not os.path.exists(user_cache_dir):
            os.mkdir(user_cache_dir)
        req = requests.get('https://twitpic.com/photos/' + user)
        page = etree.parse(StringIO(req.content), HTML_PARSER)
        for photo in USER_PHOTO_XPATH(page):
            pid = photo[1:]
            cache_file_name = os.path.join(user_cache_dir, pid) + '.jpg'
            if os.path.exists(cache_file_name):
                continue
            timestamp = mktime(get_image_timestamp(pid))
            img_url = get_full_image_url(pid)
            urlretrieve(img_url, cache_file_name)
            os.utime(cache_file_name, (timestamp, timestamp))


def get_image_timestamp(pid):
    """Get the timestamp of a photo in struct_time format"""
    req = requests.get(TWITPIC_API.format(pid=pid))
    metadata = json.loads(req.content)
    return strptime(metadata['timestamp'], TWITPIC_FMT)

def get_full_image_url(pid):
    """Get the URL of the full resolution version of a photo"""
    req = requests.get('https://twitpic.com/{pid}/full'.format(pid=pid))
    fullpage = etree.parse(StringIO(req.content), HTML_PARSER)
    (img_url,) = FULL_PHOTO_XPATH(fullpage)
    return img_url
