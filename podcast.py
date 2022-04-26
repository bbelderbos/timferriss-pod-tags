#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter
import re

import feedparser
import requests

FERRISS = "ferris"  # yeah they get it wrong sometimes


def get_data(url):
    response = requests.get(url, timeout=5)
    return response.text


def parse_html(content: str) -> list[str]:
    tags = [tag.replace("tag-", "") for tag in
            re.findall(r'tag-[^" ]+', content)]
    return tags


def parse_feed(feed: str) -> list[str]:
    tags = []
    entries = feedparser.parse(feed).entries
    for entry in entries:
        tags.extend(
            [row.term.lower() for row in entry.tags
             if FERRISS not in row.term.lower()]
        )
    return tags


def show_results(tags, min_count=5):
    for tag, count in tags.most_common():
        if count > min_count:
            print(f"{tag:50} | {count}")


if __name__ == "__main__":
    url = "http://fourhourworkweek.com/podcast/"
    feed = "https://rss.art19.com/tim-ferriss-show"
    # content = get_data(url)
    # tags = parse_html(content)
    tags = parse_feed(feed)
    tags = Counter(tags)
    show_results(tags)
