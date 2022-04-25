"""
Script from
https://github.com/bbelderbos/Codesnippets/blob/master/python/ferriss_podcast_tags.py
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter
from functools import wraps, partial
import re
from urllib.request import urlopen

import bs4
import requests

filename = "index.html"
podcast_url = "http://fourhourworkweek.com/podcast/"
TAG_REXEG = re.compile(r'tag-[^" ]+')


def retry(func=None, *, times=3):
    if func is None:
        return partial(retry, times=times)
    @wraps(func)
    def wrapper(*args, **kwargs):
        attempt = 0
        while attempt < times:
            try:
                 return func(*args, **kwargs)
            except Exception as exc:
                attempt += 1
                print(f"Exception {func}: {exc} (attempt: {attempt})")
        return func(*args, **kwargs)
    return wrapper


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
    ret = Counter(res).most_common()
    return ret


def main():
    get_index(podcast_url)
    res = parse_feed()

    order = []
    for t, tot in res.items():
        order.append( (tot, "%-50s | %s" % (t, "+"*tot) ) )

    for (tot, line) in reversed(sorted(order)):
        if tot > 1:
            print(line)


if __name__ == "__main__":
    main()
