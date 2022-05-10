#!/usr/bin/env python3

import psycopg2 as sql
import json


def format_tweets(tweets):
    iters = len(tweets["id"])
    rows = []
    for row in range(iters):
        data = {k: tweets[k][row] for k in tweets}
        data["source"] = "twitter"
        data["link"] = f"https://twitter.com/i/status/{data['id']}"
        data["category"] = None
        data["ranking"] = None
        data["media_keys"] = None
        if data.get("attachments") is not None:
            data["media_keys"] = data["attachments"].get("media_keys", None)
        if data["media_keys"]:
            data["media_keys"] = json.dumps(data["media_keys"])
        data["public_metrics"] = json.dumps(data["public_metrics"])
        data["status"] = None
        data["urls"] = None
        if data.get("entities") is not None:
            data["urls"] = data["entities"].get("urls", None)
        data["mentions"] = None
        if data.get("entitites") is not None:
            data["mentions"] = json.dumps(
                [(i["username"], i["id"]) for i in data["entities"].get("mentions")]
            )
            data["mentions"] = data["mentions"][:min(450,len(data["mentions"]))]
        data["text"] = data["text"][:min(450,len(data["text"]))]
        data["entities"] = json.dumps(data["entities"])
        data["geo"] = data.get("geo", None)
        data["phone"] = None
        data["sms"] = None
        rows.append(data)
    return rows


def format_media(media):
    iters = len(media["media_key"])
    rows = []
    for row in range(iters):
        data = {k: media[k][row] for k in media}
        if data["imgs"] is not None:
            with open(data["imgs"], "rb") as f:
                data["attachment"] = sql.Binary(f.read())
        else:
            data["attachment"] = None
        rows.append(data)
    return rows


def format_user(users):
    iters = len(users["id"])
    rows = []
    for row in range(iters):
        data = {k: users[k][row] for k in users}
        rows.append(data)
    return rows


def store_db(tweets, media, users):
    params = {
        "host": "localhost",
        "database": "twitter",
        "user": "test",
        "password": "postgres",
    }
    with sql.connect(**params) as conn:
        cur = conn.cursor()
        TWEET_SQL = (
            "INSERT INTO tweet_store (source_name, tweet_id, link, category, ranking, user_id,media_key, public_engagements, status,"
            + " time_stamp, text_content, mentions, location, urls, phone_numbers, sms_headers, lang) "
            + "VALUES (%(source)s, %(id)s, %(link)s, %(category)s, %(ranking)s, %(author_id)s, %(media_keys)s, %(public_metrics)s, %(status)s, "
            + "%(created_at)s, %(text)s, %(mentions)s, %(geo)s, %(urls)s, %(phone)s, %(sms)s, %(lang)s);"
        )
        for row in format_tweets(tweets):
            cur.execute(TWEET_SQL, row)

        MEDIA_SQL = "INSERT INTO media_store(media_key,url,attachments) VALUES (%(media_key)s,%(url)s, %(attachment)s)"
        for row in format_media(media):
            cur.execute(MEDIA_SQL, row)
        USER_SQL = "INSERT INTO user_store(user_id,user_name,user_username) VALUES (%(id)s, %(name)s, %(username)s)"
        for row in format_user(users):
            cur.execute(USER_SQL, row)
        # conn.commit()
        cur.close()


def test():
    t = {"id": [1, None], "b": [2, None], "c": [3, {"a": 8}]}
    store_db(t, t, t)


if __name__ == "__main__":
    test()
