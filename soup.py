#!/usr/bin/env python2
# -*- coding: utf8 -*-
"""
Python interface to soup.io tumbleblog
Author: András Veres-Szentkirályi <vsza@vsza.hu>
License: MIT
"""

from lxml import etree
from urllib import urlretrieve
from email.utils import mktime_tz, parsedate_tz
import os, json

RSS_URL = 'http://{user}.soup.io/rss'
ITEM_XPATH = etree.XPath('/rss/channel/item')
ATTR_XPATH = etree.XPath('soup:attributes/text()',
        namespaces=dict(soup='http://www.soup.io/rss'))
DATE_XPATH = etree.XPath('pubDate/text()')
GUID_XPATH = etree.XPath('guid/text()')

class Fetcher(object):
    """Fetches photos of Soup.io tumbleblogs into a file cache"""
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

    def fetch_photos(self, user):
        """Fetch up to 40 photos from the tumbleblog of a specified user"""
        user_cache_dir = os.path.join(self.cache_dir, user)
        if not os.path.exists(user_cache_dir):
            os.mkdir(user_cache_dir)
        feed = etree.parse(RSS_URL.format(user=user))
        for item in ITEM_XPATH(feed):
            (guid,) = GUID_XPATH(item)
            guid = guid.rsplit(':', 1)[1]
            cache_file_name = os.path.join(user_cache_dir, guid) + '.json'
            if os.path.exists(cache_file_name):
                continue
            attrs = json.loads(ATTR_XPATH(item)[0])
            if attrs['type'] != 'image':
                continue
            (datestr,) = DATE_XPATH(item)
            timestamp = int(mktime_tz(parsedate_tz(datestr)))
            image_url = attrs['url']
            image_file = image_url.rsplit('/', 1)[1]
            local_image = os.path.join(user_cache_dir, image_file)
            urlretrieve(image_url, local_image)
            details = dict(image_file=image_file, timestamp=timestamp,
                    body=attrs['body'])
            with file(cache_file_name, 'wb') as descriptor:
                json.dump(details, descriptor)
