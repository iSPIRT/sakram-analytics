#!/usr/bin/env python3
"""
Program utilities.

LICENCE:
Author: Dhruva Kashyap
"""

import re
from pathlib import Path
from typing import Dict, List

import pandas as pd


def text_transforms(text: str) -> str:
    """Remove mentions and unnecesarry whitespaces."""
    text = text.strip()
    text = re.sub(r"((@|#)\w+\b|\n)", "", text)
    text.strip()
    return text


def clean_data(raw_tweets: Dict[str, List[str]]) -> pd.DataFrame:
    """Clean data and return dataframe."""
    tweets_df = pd.DataFrame(raw_tweets)
    tweets_df.drop_duplicates(inplace=True)
    return tweets_df


def store_tweets(tweets_df: pd.DataFrame, path: Path) -> None:
    """Store tweets to a csv."""

    if path.exists():
        tweets_df = pd.concat([tweets_df, pd.read_csv(path)])
        tweets_df.drop_duplicates(inplace=True)
    with open(path, "w") as f:
        tweets_df.to_csv(f, index=False, header=True)
    print(f"Written {len(tweets_df)} rows to {path}")
