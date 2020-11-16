import os
from Configs import ConfigBase


class DEFAULT(ConfigBase):
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    # Load to db every n patent file
    # Increase or decrease this according to the amount of memory you have
    BATCH_SIZE = 1000

    # Commit to db every n nodes
    COMMIT_INTERVAL = 10000

    LOG_LEVEL = "INFO"
    NEO4J = {"host": "localhost"}

    # if set to True, the dataset will always be downloaded, regardless of its allready existing
    REDOWNLOAD_DATASET_IF_EXISTENT = False

    DATASET_SOURCE_URLS = [
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-broad-keyword-based-patents.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-patents-SARS-and-MERS.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-patents-SARS-and-MERS-TAC.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-limited-keywords-based-patents.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-CPC-based-patents.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-declared-patseq-organism.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-SARS-patents.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-MERS-patents.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-SARS-diagnosis-patents.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-MERS-diagnosis-patents.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-SARS-treatment.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Coronavirus-MERS-treatment.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Ventilators.zip",
        "https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/fulltext/Respirators-and-surgical-masks.zip",
    ]
    # Where to store the downloaded dataset
    DATASET_BASE_DIR = os.path.join(SCRIPT_DIR, "../dataset/")


class DEV(DEFAULT):
    pass


class PROD(DEFAULT):
    pass


class LOCAL(DEFAULT):
    pass
