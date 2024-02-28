# -*- coding: utf-8 -*-
import logging
from pathlib import Path

import click
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument("dir_path")
def main(dir_path):
    """Create a directory in the path specified"""
    # Create a new directory
    dir_path = Path(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)
    # Create a new sub-directory
    logger = logging.getLogger(__name__)
    logger.info("making directory: %s", dir_path)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    project_dir = Path(__file__).resolve().parents[2]

    load_dotenv(find_dotenv())

    main()
