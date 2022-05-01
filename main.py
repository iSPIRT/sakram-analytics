#!/usr/bin/env python
"""
sakram_security.
Daemon to fetch tweets and store to a DB
Author: Dhruva Kashyap
"""

import logging
import signal

from dotenv import dotenv_values

from arguments import parse_args
from extraction import do_main, initial_program_setup, program_terminate

CRON_INTERVAL: int = 60 * 60  # Seconds between API Calls


def main():
    """
    Main function to fetch tweets periodically.
    """
    args = parse_args()
    config = dotenv_values()

    args.bearer_token = config.get("Bearer_token", None)
    args.CRON_INTERVAL = config.get("Cron_Interval", CRON_INTERVAL)

    logging.basicConfig(
        handlers=[logging.FileHandler("extract.log"), logging.StreamHandler()],
        level=args.logging.upper(),
        format="[%(asctime)s] %(funcName)s: [%(levelname)s] %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p %Z",
    )
    signal.signal(signal.SIGTERM, program_terminate)
    signal.signal(signal.SIGINT, program_terminate)
    initial_program_setup(args)
    do_main(args)


if __name__ == "__main__":
    main()
