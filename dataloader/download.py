import os
import logging
import requests
import zipfile
from Configs import getConfig


config = getConfig()
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(getattr(logging, config.LOG_LEVEL))


def download():

    if not os.path.isdir(config.DATASET_BASE_DIR):
        os.makedirs(config.DATASET_BASE_DIR)

    log.info("Start downloading Lens.org patentdata dataset...")

    for url in config.DATASET_SOURCE_URLS:
        target_path_zip = os.path.join(config.DATASET_BASE_DIR, os.path.basename(url))
        content_path = os.path.join(
            config.DATASET_BASE_DIR, os.path.splitext(os.path.basename(url))[0]
        )
        if os.path.isdir(content_path) and not config.REDOWNLOAD_DATASET_IF_EXISTENT:
            log.info(
                "Skip downloading '{}'. Seems to be allready existing. Switch 'REDOWNLOAD_DATASET_IF_EXISTENT' in config.py to True to force redownload or delete '{}'".format(
                    url, content_path
                )
            )
            continue
        r = requests.get(url)
        with open(target_path_zip, "wb") as f:
            f.write(r.content)
        unzip(target_path_zip)
        for root, dirs, files in os.walk(content_path):
            for name in files:
                unzip(os.path.join(root, name))

    log.info("Finished downloading Lens.org patentdata dataset...")


def unzip(zipfile_path):
    target_path_content = os.path.dirname(zipfile_path)
    with zipfile.ZipFile(zipfile_path, "r") as zip_ref:
        zip_ref.extractall(target_path_content)
    os.remove(zipfile_path)


if __name__ == "__main__":
    download()
