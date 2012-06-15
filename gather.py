#!/usr/bin/env python

import twitpic, soup

TWITTER_USER = 'hackerspacebp'
SOUP_USER = 'hack'

def main():
    tp = twitpic.Fetcher('cache_twitpic')
    tp.fetch_photos(TWITTER_USER)
    s = soup.Fetcher('cache_soup')
    s.fetch_photos(SOUP_USER)

if __name__ == '__main__':
    main()
