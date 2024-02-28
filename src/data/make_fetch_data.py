# -*- coding: utf-8 -*-
import logging
from pathlib import Path

import click
from dotenv import find_dotenv, load_dotenv
from scrapper import JobScrapper


@click.command()
def main():

    logger = logging.getLogger(__name__)
    logger.info("making scrapper")
    scrapper = JobScrapper()
    scrapper.begin_scrap()


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
