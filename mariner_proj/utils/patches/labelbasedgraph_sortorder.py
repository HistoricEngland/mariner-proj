## This patch modifies the LabelBasedNode and LabelBasedGraph classes to include a sort order
## for the nodes. This is useful for ensuring a consistent order when rendering the graph, especially
## when dealing with multiple nodes of the same type.

## AzDevOps WorkItem: AB#93480
## Arches modules updated (file path): arches/app/utils/label_based_graph_v2.py
## Arches git commit: f66af6b0dfd75b2632aef6952aad411467143c11
## GitHub handle: @aj-he

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
    # Monkey patch start
    if sortorder is None:
        sortorder = 0
    self.sortorder = sortorder
    # Monkey patch end


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
                    # Monkey patch start
                    if should_create_new_array:
                        formatted_node_value["@sortorder"] = child_node.sortorder
                    # Monkey patch end
                    display_data[formatted_node_name] = (
                        [formatted_node_value]
                        if should_create_new_array
                        else formatted_node_value
                    )
                elif isinstance(previous_val, list):
                    # Monkey patch start
                    formatted_node_value["@sortorder"] = child_node.sortorder
                    # Monkey patch end
                    display_data[formatted_node_name].append(formatted_node_value)
                    # Monkey patch start
                    # sort the list
                    display_data[formatted_node_name] = sorted(
                        display_data[formatted_node_name],
                        key=lambda x: x["@sortorder"],
                    )
                    # Monkey patch end
                else:
                    # Monkey patch start
                    formatted_node_value["@sortorder"] = child_node.sortorder
                    # Monkey patch end
                    display_data[formatted_node_name] = [
                        previous_val,
                        formatted_node_value,
                    ]
                    # Monkey patch start
                    # sort the list
                    display_data[formatted_node_name] = sorted(
                        display_data[formatted_node_name],
                        key=lambda x: x["@sortorder"],
                    )
                    # Monkey patch end

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
def patched_build_graph(
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
                    # Monkey patch start
                    sortorder=associated_tile.sortorder,
                    # Monkey patch end
                )

                if not parent_tree:  # if top node and
                    if not parent_tile:  # if not top node in separate card
                        parent_tree = label_based_node
                else:
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


class LabelBasedGraphPatch(BasePatch):
    def apply(self):
        print("Applying LabelBasedGraphPatch...")
        LabelBasedGraph._build_graph = classmethod(patched_build_graph)
