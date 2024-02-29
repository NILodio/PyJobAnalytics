# -*- coding: utf-8 -*-
import logging
from urllib import request
from pathlib import Path
import os

import click
from dotenv import find_dotenv, load_dotenv
from scrapper import JobScrapper


@click.command()
@click.argument("output_filepath", type=click.Path())
@click.argument("cache_data", type=click.BOOL)
def main(output_filepath, cache_data):
    # Configure the logging module
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if cache_data:
        logger.info("Trying to download the data from the cache")
        # Download the data from the cache
        key = os.getenv("CACHE_RAW_DATA")
        url = f"https://drive.google.com/uc?export=download&id={key}"
        try:
            request.urlretrieve(url, output_filepath)
        except Exception as e:
            logger.error(f"Error downloading data: {e}")
            raise e
        else:
            logger.info("Data downloaded successfully")

    else:
        logger.info("making scrapper")
        scrapper = JobScrapper()
        scrapper.begin_scrap()
        logger.info("Scraping not implemented yet")
        logger.info("Saving data to %s", output_filepath)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
