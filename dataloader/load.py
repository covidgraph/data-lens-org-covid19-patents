import os
import json
import logging
import py2neo
from Configs import getConfig
from DZDjson2GraphIO import Json2graphio

config = getConfig()
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(getattr(logging, config.LOG_LEVEL))


def get_graph():

    if config.GC_NEO4J_USER is not None:
        return py2neo.Graph(
            config.GC_NEO4J_URL,
            password=config.GC_NEO4J_PASSWORD,
            user=config.GC_NEO4J_USER,
        )
    else:
        return py2neo.Graph(config.GC_NEO4J_URL)


class PatentLoader(object):
    _loader = None

    def __init__(self, json_file_path_list: list):
        log.info("  Parse next {} json files".format(len(json_file_path_list)))
        for file_path in json_file_path_list:
            json_data = None
            with open(file_path) as json_file:
                json_data = json.load(json_file)
            self.loader.load_json(json_data, "Patent")
        log.info(
            "  Load next {} json files into neo4j@{}".format(
                len(json_file_path_list), config.GC_NEO4J_URL
            )
        )
        self.loader.create_indexes(get_graph())
        self.loader.merge(get_graph())

    @property
    def loader(self):
        if self._loader is None:
            # instantiate and configure the Json2graphio loader
            self._loader = Json2graphio()
            self._loader.config_list_skip_collection_hubs = (
                config.JSON2GRAPH_SKIP_COLLECTION_HUBS
            )
            self._loader.config_list_collection_anchor_extra_labels = (
                config.JSON2GRAPH_COLLECTION_ANCHOR_EXTRA_LABELS
            )
            self._loader.config_str_collection_anchor_label = (
                "Collection_{LIST_MEMBER_LABEL}"
            )
            self._loader.config_bool_capitalize_labels = False
            self._loader.config_dict_label_override = config.JSON2GRAPH_LABEL_OVERRIDE
            self._loader.config_dict_json_attr_to_reltype_instead_of_label = (
                config.JSON2GRAPH_ATTR_TO_RELTYPE_INSTEAD_OF_LABEL
            )
            self._loader.config_dict_property_name_override = (
                config.JSON2GRAPH_PROPERTY_NAME_OVERRIDE
            )
            self._loader.config_list_default_primarykeys = config.JSON2GRAPH_DEFAULT_IDS
            # self._loader.config_dict_primarykey_attr_by_label = {"Patent": "lens_id"}
            self._loader.config_dict_property_to_extra_node = {"Patent": ["lens_id"]}
            # self._loader.config_dict_primarykey_attr_by_label = None
            self._loader.config_dict_primarykey_generated_hashed_attrs_by_label = (
                config.JSON2GRAPH_PRIMARYKEY_GENERATED_HASHED_ATTRS_BY_LABEL
            )
            self._loader.config_str_primarykey_generated_attr_name = "_hash_id"
            # If set to true, all collections hubs get a second label, named after the list member nodes
            # self._loader.config_str_collection_anchor_attach_list_members_label = False
            # self._loader.config_str_collection_relation_postfix = "_COLLECTION"
            # self._loader.config_bool_collection_anchor_only_when_len_min_2 = False
            # self._loader.config_func_custom_relation_name_generator = None
            # self._loader.config_func_label_name_generator_func = None
            # self._loader.config_dict_concat_list_attr = None
            # self._loader.config_func_node_post_modifier = None
            # self._loader.config_func_node_pre_modifier = None

            self._loader.config_dict_interfold_json_attr = (
                config.JSON2GRAPH_INTERFOLD_JSON_ATTR
            )

            self._loader.config_graphio_batch_size = config.COMMIT_INTERVAL
            # self._loader.config_dict_create_merge_depending_scheme = None
            self.config_dict_reltype_override = config.JSON2GRAPH_RELTYPE_OVERRIDE
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


def load():
    for d in os.listdir(config.DATASET_BASE_DIR):

        PatentLoader.load_dir(os.path.join(config.DATASET_BASE_DIR, d))


if __name__ == "__main__":
    load()
