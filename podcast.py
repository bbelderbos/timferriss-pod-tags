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

from decorators import retry

filename = "index.html"
podcast_url = "http://fourhourworkweek.com/podcast/"
TAG_REXEG = re.compile(r'tag-[^" ]+')


@retry
def get_index(url):
    """
    http://stackoverflow.com/questions/24346872/python-equivalent-of-a-given-wget-command
    """
    resp = requests.get(url)
    with open(filename, 'w') as f:
        f.write(resp.text)


def parse_feed():
    """
    http://stackoverflow.com/questions/6213063/python-read-next
    """
    res = []
    with open(filename, 'r') as f:
        for line in f:
            if 'tag-' not in line:
                continue
            mtags = TAG_REXEG.findall(line)
            tags = [tag.replace("tag-", " ") for tag in mtags]
            res.extend(tags)
    ret = Counter(res)
    return ret


def main():
    get_index(podcast_url)
    res = parse_feed()

    for tag, count in res.most_common():
        if count > 1:
            print(f"{tag:30} | {count}")


if __name__ == "__main__":
    main()
