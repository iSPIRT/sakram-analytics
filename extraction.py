#!/usr/bin/env python3

import logging
from time import sleep

from twitter_ import fetch_tweets
from postgres_ import store_db


def initial_program_setup(args):
    pass


def start_extraction(args):
    bearer_token = args.bearer_token
    tweets, media, users = fetch_tweets(bearer_token)
    store_db(tweets, media, users)


def do_main(args) -> None:
    while True:
        logging.info("Starting Extraction")
        start_extraction(args)
        logging.info(f"Finishing Extraction")
        logging.info(f"Sleeping for {args.CRON_INTERVAL}s")
        sleep(args.CRON_INTERVAL)


def program_terminate(signal, _):
    exit()
