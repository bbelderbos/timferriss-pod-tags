"""
Original:
https://github.com/bbelderbos/Codesnippets/blob/master/python/ferriss_podcast_tags.py
"""
from collections import Counter
import re

import requests

TAG_REGEX = re.compile(r'tag-[^" ]+')


def parse_feed(url):
    resp = requests.get(url)
    tags = re.findall(TAG_REGEX, resp.text)
    return Counter(tags)


def main():
    podcast_url = "http://fourhourworkweek.com/podcast/"
    res = parse_feed(podcast_url)
    for tag, count in res.most_common():
        if count > 1:
            print(f"{tag:30} | {count}")


if __name__ == "__main__":
    main()
