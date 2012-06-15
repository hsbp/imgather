#!/usr/bin/env python

import twitpic

TWITTER_USER = 'hackerspacebp'

def main():
    tp = twitpic.Fetcher('cache_twitpic')
    tp.fetch_photos(TWITTER_USER)

if __name__ == '__main__':
    main()
