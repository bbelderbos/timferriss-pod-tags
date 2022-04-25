"""
Script from
https://github.com/bbelderbos/Codesnippets/blob/master/python/ferriss_podcast_tags.py
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter
import re
from urllib.request import urlopen

import bs4
import requests

podcast_url = "http://fourhourworkweek.com/podcast/"
TAG_REXEG = re.compile(r'tag-[^" ]+')


def parse_feed(url):
    """
    http://stackoverflow.com/questions/6213063/python-read-next
    """
    resp = requests.get(url)
    res = []
    for line in resp.text.splitlines():
        if 'tag-' not in line:
            continue
        mtags = TAG_REXEG.findall(line)
        tags = [tag.replace("tag-", " ") for tag in mtags]
        res.extend(tags)
    ret = Counter(res)
    return ret


def main():
    res = parse_feed(podcast_url)

    for tag, count in res.most_common():
        if count > 1:
            print(f"{tag:30} | {count}")


if __name__ == "__main__":
    main()
