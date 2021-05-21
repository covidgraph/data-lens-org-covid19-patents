import os
import json
import logging
import py2neo
from Configs import getConfig
from dict2graph import Dict2graph

config = getConfig()
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(getattr(logging, config.LOG_LEVEL))


def get_graph():
    return py2neo.Graph(**config.NEO4J)


class PatentLoader(object):
    _loader: Dict2graph = None

    def __init__(self, json_file_path_list: list):
        log.info("  Parse next {} json files".format(len(json_file_path_list)))
        for file_path in json_file_path_list:
            json_data = None
            with open(file_path) as json_file:
                json_data = json.load(json_file)
            self.loader.load_json(json_data, "Patent")
        log.info(
            "  Load next {} json files into neo4j".format(len(json_file_path_list))
        )
        self.loader.create_indexes(get_graph())
        self.loader.merge(get_graph())

    @property
    def loader(self):
        if self._loader is None:
            # instantiate and configure the Json2graphio loader
            self._loader = Dict2graph()
            self._loader.config_graphio_batch_size = config.COMMIT_INTERVAL
            self._loader.config_list_blocklist_collection_hubs = [
                "PatentTitleCollection",
                "PatentClaimCollection",
                "PatentAbstractCollection",
                "EntityCollection",
                "PatentDescriptionCollection",
                "LensIDCollection",
            ]
            self._loader.config_list_collection_hub_extra_labels = []
            self._loader.config_str_collection_hub_label = (
                "{LIST_MEMBER_LABEL}Collection"
            )
            self._loader.config_dict_label_override = {
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
                "familyextended": {"PatentFamily": {"type": "extended"}},
                "familysimple": {"PatentFamily": {"type": "simple"}},
                "lens_id": "LensID",
                "classification_cpc": "CooperativePatentClassification",
                "classification_ipc": "InternationalPatentClassification",
                "classification_us": "USPatentClassification",
                "CooperativePatentClassificationCollection": "PatentClassificationCollection",
                "InternationalPatentClassificationCollection": "PatentClassificationCollection",
                "USPatentClassificationCollection": "PatentClassificationCollection",
            }
            self._loader.config_dict_attr_name_to_reltype_instead_of_label = {
                "inventor": "Entity",
                "owner": "Entity",
                "applicant": "Entity",
            }
            self._loader.config_dict_property_name_override = {
                "Entity": {"inventor": "name", "owner": "name", "applicant": "name", "Entity": "name"},
                "LensID": {"LensID": "id", "lens_id": "id"},
            }
            self._loader.config_list_default_primarykeys = [
                "id",
            ]
            self._loader.config_dict_primarykey_attr_by_label = {
                "Patent": ["lens_id"],
                "Entity": ["name"],
                "Family": ["family_id"],
            }
            self._loader.config_dict_property_to_extra_node = {
                "Patent": {"lens_id": "copy", "pub_key": "copy"},
                "PatentLiteratureCitation": ["pub_key"],
            }

            # self._loader.config_dict_primarykey_attr_by_label = None
            self._loader.config_dict_primarykey_generated_hashed_attrs_by_label = {
                "Patent": "AllAttributes",
                "PatentDescription": ["text"],
                "PatentClaim": ["text"],
                "PatentTitle": ["text"],
                "PatentAbstract": ["text"],
                "PatentLiteratureCitation": "AllAttributes",
                "NonPatentLiteratureCitation": "AllAttributes",
            }
            self._loader.config_str_primarykey_generated_attr_name = "_hash_id"

            self._loader.config_dict_interfold_json_attr = {
                "Patent": {
                    "bibliographic_data": {"combine_attr_names": False},
                    "family": {"combine_attr_names": True},
                },
            }
            self._loader.config_list_drop_reltypes = ["PATENT_HAS_PATENTFAMILY"]

            self.config_dict_reltype_override = {}
        return self._loader

    @classmethod
    def load_dir(cls, source_dir):
        batch = []
        log.info("Process json data from dir '{}'".format(source_dir))
        for root, dirs, files in os.walk(source_dir):
            for name in files:
                batch.append(os.path.join(root, name))

                if len(batch) >= config.BATCH_SIZE:
                    cls(batch)
                    batch = []
        # load leftovers
        cls(batch)


def load_data():
    for d in os.listdir(config.DATASET_BASE_DIR):
        PatentLoader.load_dir(os.path.join(config.DATASET_BASE_DIR, d))
    log.info("Run Postprocess queries...")


if __name__ == "__main__":
    load_data()
