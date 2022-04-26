from collections import Counter
import re

import feedparser
import requests

from decorators import retry

FERRISS = "ferris"  # sometimes get it wrong

@retry
def get_podcast_html(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_html(content: str) -> Counter:
    return Counter(
        tag.replace("tag-", "") for tag in
        re.findall(r'tag-[^" ]+', content)
    )


def parse_feed(feed: str) -> list[str]:
    tags = []
    entries = feedparser.parse(feed).entries
    for entry in entries:
        tags.extend(
            [tag.term.lower() for tag in entry.tags
             if FERRISS not in tag.term.lower()]
        )
    return tags


def show_results(tags: Counter, min_count: int = 20) -> None:
    for tag, count in tags.most_common():
        if count > min_count:
            print(f"{tag:30} | {count}")


if __name__ == "__main__":
    podcast_url = "http://fourhourworkweek.com/podcast/"
    # content = get_podcast_html(podcast_url)
    # tags = parse_html(content)
    feed = "https://rss.art19.com/tim-ferriss-show"
    tags = Counter(parse_feed(feed))
    show_results(tags)
