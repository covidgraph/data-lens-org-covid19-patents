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
    NEO4J={"host":"localhost"}

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

    # Properties that will be taken as mergeKey/PrimaryKey, if not anything other is configured
    JSON2GRAPH_DEFAULT_IDS = [
        "id",
    ]
    # Properties that will be taken into account as mergeKey/PrimaryKey per label
    JSON2GRAPH_PRIMARYKEY_ATTR_BY_LABEL = {
        "Patent": "lens_id",
        "Entity": "name",
        "Family": "family_id",
    }

    # Properties that will be unfold to be an extra single node
    JSON2GRAPH_PROPERTY_TO_EXTRA_NODE = {
        "Patent": ["lens_id", "pub_key"],
        "PatentLiteratureCitation": ["pub_key"],
    }

    JSON2GRAPH_LABEL_OVERRIDE = {
        "bibliographic_data": "Patent",
        "npl_cit": "NonPatentLiteratureCitation",
        "pat_cit": "PatentLiteratureCitation",
        "pub_key": "PatentNumber",
        "claims": "PatentClaim",
        "description": "PatentDescription",
        "abstract": "PatentAbstract",
        "title": "PatentTitle",
        "NonPatentLiteratureCitationCollection": "PatentCitationCollection",
        "PatentLiteratureCitationCollection": "PatentCitationCollection",
        "family_extended": {"PatentFamily": {"type": "extended"}},
        "family_simple": {"PatentFamily": {"type": "simple"}},
        "lens_id": "LensID",
        "classification_cpc": "CooperativePatentClassification",
        "classification_ipc": "InternationalPatentClassification",
        "classification_us": "USPatentClassification",
        "CooperativePatentClassificationCollection": "PatentClassificationCollection",
        "InternationalPatentClassificationCollection": "PatentClassificationCollection",
        "USPatentClassificationCollection": "PatentClassificationCollection",
    }
    JSON2GRAPH_COLLECTION_ANCHOR_EXTRA_LABELS = []
    JSON2GRAPH_PRIMARYKEY_GENERATED_HASHED_ATTRS_BY_LABEL = {
        "PatentDescription": ["text"],
        "PatentClaim": ["text"],
        "PatentTitle": ["text"],
        "PatentAbstract": ["text"],
        "PatentLiteratureCitation": "AllAttributes",
        "NonPatentLiteratureCitation": "AllAttributes",
    }

    JSON2GRAPH_SKIP_COLLECTION_HUBS = [
        "PatentTitleCollection",
        "PatentClaimCollection",
        "PatentAbstractCollection",
        "EntityCollection",
        "PatentDescriptionCollection",
        "LensIDCollection",
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

    JSON2GRAPH_LIST_DROP_RELTYPES = ["PATENT_HAS_PATENTFAMILY"]

    POST_PROCESS_QUERIES = [
        'call db.index.fulltext.createNodeIndex("PatentsFulltextIndex",["PatentTitle","PatentDescription","PatentAbstract","PatentClaim"],["text"])'
    ]


class DEV(DEFAULT):
    pass


class PROD(DEFAULT):
    pass


class LOCAL(DEFAULT):
    pass
