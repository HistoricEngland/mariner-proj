## This patch modifies the LabelBasedNode and LabelBasedGraph classes to include a sort order
## for the nodes. This is useful for ensuring a consistent order when rendering the graph, especially
## when dealing with multiple nodes of the same type.

## AzDevOps WorkItem: AB#93480
## Arches modules updated (file path): arches/app/utils/label_based_graph_v2.py
## Arches git commit: f66af6b0dfd75b2632aef6952aad411467143c11

from arches.app.utils.label_based_graph_v2 import LabelBasedNode, LabelBasedGraph
from arches.app.models import models
from arches.app.utils.label_based_graph_v2 import (
    NODE_ID_KEY,
    NON_DATA_COLLECTING_NODE,
    TILE_ID_KEY,
)
from arches.app.datatypes.datatypes import DataTypeFactory
from mariner_proj.utils.patches.base import BasePatch
from django.utils import translation


def patched_init(self, name, node_id, tile_id, value, cardinality=None, sortorder=0):
    self.name = name
    self.node_id = node_id
    self.tile_id = tile_id
    self.cardinality = cardinality
    self.value = value
    self.child_nodes = []
    if sortorder is None:
        sortorder = 0
    self.sortorder = sortorder


def patched_as_json(
    self, compact=False, include_empty_nodes=True, include_hidden_nodes=True
):
    display_data = {}

    if not include_hidden_nodes:
        card = models.CardModel.objects.filter(nodegroup_id=self.node_id).first()
        try:
            if not card.visible:
                return None
        except AttributeError:
            pass

    for child_node in self.child_nodes:
        formatted_node = child_node.as_json(
            compact=compact,
            include_empty_nodes=include_empty_nodes,
            include_hidden_nodes=include_hidden_nodes,
        )
        if formatted_node is not None:
            formatted_node_name, formatted_node_value = formatted_node.popitem()

            if include_empty_nodes or not child_node.is_empty():
                previous_val = display_data.get(formatted_node_name)
                cardinality = child_node.cardinality

                # let's handle multiple identical node names
                if not previous_val:
                    should_create_new_array = (
                        cardinality == "n" and self.tile_id != child_node.tile_id
                    )
                    if should_create_new_array:
                        formatted_node_value["@sortorder"] = child_node.sortorder
                    display_data[formatted_node_name] = (
                        [formatted_node_value]
                        if should_create_new_array
                        else formatted_node_value
                    )
                elif isinstance(previous_val, list):
                    formatted_node_value["@sortorder"] = child_node.sortorder
                    display_data[formatted_node_name].append(formatted_node_value)
                    # sort the list
                    display_data[formatted_node_name] = sorted(
                        display_data[formatted_node_name],
                        key=lambda x: x["@sortorder"],
                    )
                else:
                    formatted_node_value["@sortorder"] = child_node.sortorder
                    display_data[formatted_node_name] = [
                        previous_val,
                        formatted_node_value,
                    ]
                    # sort the list
                    display_data[formatted_node_name] = sorted(
                        display_data[formatted_node_name],
                        key=lambda x: x["@sortorder"],
                    )

    val = self.value
    if compact and display_data:
        if self.value is not NON_DATA_COLLECTING_NODE:
            if self.value is not None:
                display_data.update(self.value)
    elif compact and not display_data:  # if compact and no child nodes
        display_data = self.value
    elif not compact:
        display_data[NODE_ID_KEY] = self.node_id
        display_data[TILE_ID_KEY] = self.tile_id
        if self.value is not None and self.value is not NON_DATA_COLLECTING_NODE:
            display_data.update(self.value)

    return {self.name: display_data}


class LabelBasedNodePatch(BasePatch):
    def apply(self):
        print("Applying LabelBasedNodePatch...")
        LabelBasedNode.__init__ = patched_init
        LabelBasedNode.as_json = patched_as_json


# Class method patches need to be
@classmethod
def _patched_build_graph(
    cls,
    input_node,
    input_tile,
    parent_tree,
    node_ids_to_tiles_reference,
    nodegroup_cardinality_reference,
    serialized_graph,
    datatype_factory,
    node_ids_to_serialized_nodes,
    edge_domain_node_ids_to_range_nodes,
):
    for associated_tile in node_ids_to_tiles_reference.get(
        input_node["nodeid"], [input_tile]
    ):
        parent_tile = associated_tile.parenttile

        if associated_tile == input_tile or parent_tile == input_tile:
            if (
                cls.is_valid_semantic_node(
                    node=input_node,
                    tile=associated_tile,
                    node_ids_to_tiles_reference=node_ids_to_tiles_reference,
                    edge_domain_node_ids_to_range_nodes=edge_domain_node_ids_to_range_nodes,
                )
                or input_node["nodeid"] in associated_tile.data
            ):

                label_based_node = LabelBasedNode(
                    name=input_node["name"],
                    node_id=input_node["nodeid"],
                    tile_id=str(associated_tile.pk),
                    value=cls._get_display_value(
                        tile=associated_tile,
                        serialized_node=input_node,
                        datatype_factory=datatype_factory,
                    ),
                    cardinality=nodegroup_cardinality_reference.get(
                        str(associated_tile.nodegroup_id)
                    ),
                    sortorder=associated_tile.sortorder,
                )

                if not parent_tree:  # if top node and
                    if not parent_tile:  # if not top node in separate card
                        parent_tree = label_based_node
                else:
                    # if not hasattr(parent_tree, "child_nodes"):
                    #    parent_tree.child_nodes = []
                    parent_tree.child_nodes.append(label_based_node)

                for child_node in edge_domain_node_ids_to_range_nodes.get(
                    input_node["nodeid"], []
                ):
                    cls._build_graph(
                        input_node=child_node,
                        input_tile=associated_tile,
                        parent_tree=label_based_node,
                        node_ids_to_tiles_reference=node_ids_to_tiles_reference,
                        nodegroup_cardinality_reference=nodegroup_cardinality_reference,
                        serialized_graph=serialized_graph,
                        datatype_factory=datatype_factory,
                        node_ids_to_serialized_nodes=node_ids_to_serialized_nodes,
                        edge_domain_node_ids_to_range_nodes=edge_domain_node_ids_to_range_nodes,
                    )

    return parent_tree


@classmethod
def patched_from_resource(
    cls,
    resource,
    datatype_factory=None,
    compact=False,
    hide_empty_nodes=False,
    as_json=True,
    user=None,
    perm=None,
    hide_hidden_nodes=False,
):
    """
    Generates a label-based graph from a given resource
    """
    if not datatype_factory:
        datatype_factory = DataTypeFactory()

    if not resource.tiles:
        resource.load_tiles(user, perm)

    (
        node_ids_to_tiles_reference,
        nodegroup_cardinality_reference,
    ) = cls.generate_node_ids_to_tiles_reference_and_nodegroup_cardinality_reference(
        resource=resource
    )

    user_language = translation.get_language()
    published_graph = models.PublishedGraph.objects.get(
        publication=resource.graph.publication, language=user_language
    )
    serialized_graph = published_graph.serialized_graph

    node_ids_to_serialized_nodes = {
        serialized_node["nodeid"]: serialized_node
        for serialized_node in serialized_graph["nodes"]
    }

    edge_domain_node_ids_to_range_nodes = {}
    for serialized_edge in serialized_graph["edges"]:
        if (
            edge_domain_node_ids_to_range_nodes.get(serialized_edge["domainnode_id"])
            is None
        ):
            edge_domain_node_ids_to_range_nodes[serialized_edge["domainnode_id"]] = []

        range_node = [
            serialized_node
            for serialized_node in serialized_graph["nodes"]
            if serialized_node["nodeid"] == serialized_edge["rangenode_id"]
        ][0]
        edge_domain_node_ids_to_range_nodes[serialized_edge["domainnode_id"]].append(
            range_node
        )

    root_label_based_node = LabelBasedNode(
        name=None, node_id=None, tile_id=None, value=None, cardinality=None, sortorder=0
    )
    root_label_based_node.child_nodes = []

    for tile in resource.tiles:
        label_based_graph = LabelBasedGraph.from_tile(
            tile=tile,
            node_ids_to_tiles_reference=node_ids_to_tiles_reference,
            nodegroup_cardinality_reference=nodegroup_cardinality_reference,
            datatype_factory=datatype_factory,
            node_ids_to_serialized_nodes=node_ids_to_serialized_nodes,
            edge_domain_node_ids_to_range_nodes=edge_domain_node_ids_to_range_nodes,
            hide_empty_nodes=hide_empty_nodes,
            serialized_graph=serialized_graph,
            as_json=False,
        )

        if label_based_graph:
            root_label_based_node.child_nodes.append(label_based_graph)

    if as_json:
        root_label_based_node_json = root_label_based_node.as_json(
            compact=compact,
            include_empty_nodes=bool(not hide_empty_nodes),
            include_hidden_nodes=bool(not hide_hidden_nodes),
        )

        _dummy_resource_name, resource_graph = root_label_based_node_json.popitem()

        # removes unneccesary ( None ) top-node values
        if resource_graph:
            for key in [NODE_ID_KEY, TILE_ID_KEY]:
                resource_graph.pop(key, None)

        # adds metadata that was previously only accessible via API
        return {
            "displaydescription": resource.displaydescription(),
            "displayname": resource.displayname(),
            "graph_id": resource.graph_id,
            "legacyid": resource.legacyid,
            "map_popup": resource.map_popup(),
            "resourceinstanceid": resource.resourceinstanceid,
            "resource": resource_graph,
        }
    else:  # pragma: no cover
        return root_label_based_node


class LabelBasedGraphPatch(BasePatch):
    def apply(self):
        print("Applying LabelBasedGraphPatch...")
        LabelBasedGraph._build_graph = classmethod(_patched_build_graph)
        # LabelBasedGraph.from_resource = classmethod(patched_from_resource)
