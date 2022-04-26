"""
Original:
https://github.com/bbelderbos/Codesnippets/blob/master/python/ferriss_podcast_tags.py
"""
from collections import Counter
import re

import feedparser
import requests

AUTHOR = "ferris"  # sometimes it gets misspelled
TAG_REGEX = re.compile(r'tag-[^" ]+')


def parse_html_page(url):
    resp = requests.get(url)
    tags = re.findall(TAG_REGEX, resp.text)
    return Counter(tags)


def parse_feed(url):
    ret = feedparser.parse(url)
    tags = []
    for entry in ret.entries:
        tags.extend(
            [t.term.lower() for t in entry.tags
             if AUTHOR not in t.term.lower()]
        )
    return Counter(tags)


def show_results(tags, min_tags=1):
    for tag, count in tags.most_common():
        if count > min_tags:
            print(f"{tag:30} | {count}")


def main():
    url = "http://fourhourworkweek.com/podcast/"
    feed = "https://rss.art19.com/tim-ferriss-show"
    tags = parse_feed(feed)
    show_results(tags)


if __name__ == "__main__":
    main()
