#!/usr/bin/env python

import csv
import re
import tarfile
from datetime import date
from pathlib import Path
from subprocess import PIPE, Popen
from dotenv import dotenv_values
import nltk
import pandas as pd
import psycopg2 as sql
from meta import extended_stopwords
from nltk.corpus import stopwords
from wordcloud import WordCloud


def wc(df):
    nltk.download("stopwords")
    df = df.drop_duplicates(subset=["text_content"])
    full_text = ",".join(
        [i for i in df["text_content"]]
    ).lower()
    full_text = re.sub(r"[,\.!?]", "", full_text)
    full_text = re.sub(r"@.*\w", "", full_text)
    full_text = re.sub(r"#.*\w", "", full_text)
    full_text = re.sub(r"https://tco/.*\w", "", full_text)
    full_text = re.sub(r"\brt", "", full_text)
    full_text = full_text.encode("ascii", "ignore").decode()
    stop_words = stopwords.words("english")
    stop_words.extend(extended_stopwords)
    wordcloud = WordCloud(
        background_color="white",
        width=1000,
        height=500,
        contour_color="steelblue",
        stopwords=stop_words,
        include_numbers=True,
    )  # Generate a word cloud
    wordcloud.generate(full_text)
    return wordcloud


def main():
    from_email = "twitter-analysis@Sakram.com"
    to_list = [
        "dhruva12kashyap@gmail.com",
        #        "rinka.singh@gmail.com",
        #        "parashuramjoshi23@gmail.com",
    ]
    subject = f"Sakram Analysis: Report {date.today()}"
    params = dotenv_values()
    params = {k:v for k,v in params.items() if k in ["host","database","user","password"]}
    with sql.connect(**params) as conn:
        SQL = (
            "SELECT DISTINCT source_name as source, tweet_id, link, category, ranking, user_id as author_id, media_key as media_keys, public_engagements as public_metrics, status,"
            + " time_stamp, text_content, mentions, location, urls, phone_numbers, sms_headers, lang FROM tweet_store "
            + "WHERE time_stamp BETWEEN NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7 AND NOW()::DATE-EXTRACT(DOW from NOW())::INTEGER;"
        )
        tweets: pd.DataFrame = pd.read_sql(SQL, conn)
    num_tweets = len(tweets)
    attachment_dir = Path(f"dumps/{date.today()}/")
    attachment_dir.mkdir(exist_ok=True)
    csv_path = attachment_dir / "tweets.csv"
    wc_path = attachment_dir / "wc.jpg"
    zip_path = attachment_dir / f"{date.today()}.tar.gz"
    with tarfile.open(zip_path, "w:gz") as f:
        tweets.to_csv(csv_path, index=False)
        wc(tweets).to_image().save(wc_path)
        f.add(csv_path, arcname=csv_path.name)
        f.add(wc_path, arcname=wc_path.name)
    msg = (
        "Hello all\nPFA attachment containing tweets collected since last week and a wordcloud depicting the topics of last week.\n"
        + f"{num_tweets} have been collected in the past week.\n"
        + "This is system generated."
    )
    print(",".join(to_list),num_tweets)
    arguments = [
        "/usr/bin/mail",
        "-s",
        subject,
        f"-aFrom:{from_email}",
        "-A",
        zip_path,
        "--",
        ",".join(to_list),
    ]
    p = Popen(arguments, stdin=PIPE, universal_newlines=True)
    p.communicate(msg)


if __name__ == "__main__":
    main()
