#!/usr/bin/env python3

from io import BytesIO
from multiprocessing.pool import Pool
from typing import List
import logging

import requests
import tweepy as tw
from PIL import Image


def store_image(media_key, url, type):
    store_path=None
    if type=="photo":
       try:
           response = BytesIO(requests.get(url).content)
           store_path = f"imgs/{media_key}.{url.split('.')[-1]}"
           Image.open(response).save(store_path)
       except requests.exceptions.ConnectionError:
           logging.error(f"Unable to fetch {url}")
    return store_path


def fetch_tweets(bearer_token):
    tweet_store = {
        "author_id": [],
        "entities": [],
        "id": [],
        "in_reply_to_user_id": [],
        "lang": [],
        "referenced_tweets": [],
        "text": [],
        "attachments": [],
        "public_metrics": [],
        "created_at": [],
    }
    media_store = {
        "media_key": [],
        "url": [],
        "type": [],
        "imgs": [],
    }
    user_store = {
        "name": [],
        "id": [],
        "username": [],
    }

    query: List[str] = ["@Cyberdost"]

    client = tw.Client(bearer_token=bearer_token)

    tweets = client.search_recent_tweets(
        query=query,
        max_results=100,
        expansions=[
            "attachments.media_keys",
            "author_id",
            "referenced_tweets.id",
            "entities.mentions.username",
            "geo.place_id",
            "in_reply_to_user_id",
            "referenced_tweets.id.author_id",
        ],
        media_fields=[
            "type",
            "url",
        ],
        user_fields=["name", "id", "username"],
        tweet_fields=[
            "text",
            "attachments",
            "author_id",
            "geo",
            "id",
            "lang",
            "referenced_tweets",
            "public_metrics",
            "created_at",
        ],
    )
    if tweets.includes.get("media", []):
        for i in tweets.includes["media"]:
            for k in media_store:
                v = i.get(k,None)
                media_store[k].append(v)
        with Pool() as p:
            imgs = tweets.includes["media"]
            media_store["imgs"] = p.starmap(
                store_image,
                [(i.media_key, i.url, i.type) for i in imgs],
            )
    if tweets.includes.get("users", []):
        for i in tweets.includes["users"]:
            for k, v in i.items():
                if k in user_store:
                    user_store[k].append(v)
    with open("blacklist") as f:
        Black_list_authors = [i[0] for i in f.readlines()]
    rts = []
    for tweet in tweets.data:
        if tweet.author_id not in Black_list_authors:
            for k in tweet_store:
                v = tweet.get(k, None)
                tweet_store[k].append(v)
            if tweet.referenced_tweets is not None:
                rts.extend(
                    [i.id for i in tweet.referenced_tweets if i.type == "retweeted"]
                )
    rt_tweets = client.get_tweets(rts)
    for tweet in rt_tweets.data:
        if tweet.author_id not in Black_list_authors:
            for k in tweet_store:
                v = tweet.get(k, None)
                tweet_store[k].append(v)

    return tweet_store, media_store, user_store
