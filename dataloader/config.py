import os
from Configs import ConfigBase


class DEFAULT(ConfigBase):
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    # Load to db every n patent file
    # Increase or decrease this according to the amount of memory you have
    BATCH_SIZE = 300

    # Commit to db every n nodes
    COMMIT_INTERVAL = 10000

    LOG_LEVEL = "INFO"
    GC_NEO4J_URL = "localhost"
    GC_NEO4J_USER = None
    GC_NEO4J_PASSWORD = None

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
    ]
    # Where to store the downloaded dataset
    DATASET_BASE_DIR = os.path.join(SCRIPT_DIR, "../dataset/")

    JSON2GRAPH_DEFAULT_IDS = [
        "lens_id",
        "family_id",
        "_id",
    ]

    JSON2GRAPH_LABEL_OVERRIDE = {
        "bibliographic_data": "Patent",
        "nlp_cit": "NonPatentLiteratureCitation",
        "pat_cit": "PatentLiteratureCitation",
        "claims": "PatentClaim",
        "description": "PatentDescription",
        "abstract": "PatentAbstract",
        "title": "PatentTitle",
        "Collection_NonPatentLiteratureCitation": "PatentCitations",
        "Collection_PatentLiteratureCitation": "PatentCitations",
        "family_extended": {"Family": {"type": "extended"}},
        "family_simple": {"Family": {"type": "simple"}},
        "lens_id": "LensID",
    }
    JSON2GRAPH_COLLECTION_ANCHOR_EXTRA_LABELS = []

    JSON2GRAPH_PRIMARYKEY_ATTR_BY_LABEL = {}
    JSON2GRAPH_PRIMARYKEY_GENERATED_HASHED_ATTRS_BY_LABEL = {
        "PatentDescription": ["text"],
        "PatentClaim": ["text"],
        "PatentAbstract": ["text"],
        "PatentLiteratureCitation": "AllAttributes",
        "NonPatentLiteratureCitation": "AllAttributes",
    }

    JSON2GRAPH_SKIP_COLLECTION_HUBS = [
        "Collection_PatentTitle",
        "Collection_PatentClaim",
        "Collection_PatentAbstract",
        "Collection_Entity",
        "Collection_PatentDescription",
        "Collection_lens_id",
    ]

    JSON2GRAPH_ATTR_TO_RELTYPE_INSTEAD_OF_LABEL = {
        "inventor": "Entity",
        "owner": "Entity",
        "applicant": "Entity",
    }

    JSON2GRAPH_PROPERTY_NAME_OVERRIDE = {
        "Entity": {"inventor": "name", "owner": "name", "applicant": "name"},
        "LensID": {"lens_id": "id"},
    }

    JSON2GRAPH_RELTYPE_OVERRIDE = {}

    # merge/pull-up attr of family into bibliographic_data and attrs of bibliographic_data into patent
    JSON2GRAPH_INTERFOLD_JSON_ATTR = {
        "Patent": {
            "bibliographic_data": {"combine_attr_names": False},
            "family": {"combine_attr_names": True},
        },
    }


class DEV(ConfigBase):
    pass


class PROD(ConfigBase):
    pass


class LOCAL(ConfigBase):
    pass
