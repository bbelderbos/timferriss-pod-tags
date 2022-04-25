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


def show_results(tags, min_tags=1):
    for tag, count in tags.most_common():
        if count > min_tags:
            print(f"{tag:30} | {count}")


def main():
    podcast_url = "http://fourhourworkweek.com/podcast/"
    tags = parse_feed(podcast_url)
    show_results(tags)


if __name__ == "__main__":
    main()
