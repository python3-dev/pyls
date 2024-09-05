"""FileSystem definitions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from src.core.node import Node

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable


class FileSystem:
    """Represents a file system.

    This class represents a file system and provides methods to list the
    contents of the file system.

    Parameters
    ----------
    json_path : str
        The path to the JSON file containing the file system data.

    Attributes
    ----------
    json_path : Path
        The path to the JSON file.
    json_data : dict
        The parsed JSON data.
    root : Node
        The root node of the file system.

    Methods
    -------
    __load_json()
        Load the JSON file.
    __build_tree(data)
        Build the tree from the JSON data.
    ls(directory=None)
        List the contents of the file system.

    """

    def __init__(self, json_path: str = "structure.json") -> None:
        """Initialize the file system."""
        self.json_path: Path = Path(json_path)
        self.json_data = self.__load_json()
        self.root: Node = self.__build_tree(self.json_data)

    def __load_json(self) -> dict:
        """Load json file.

        Returns
        -------
        dict
            The parsed JSON data.

        """
        with self.json_path.open(mode="r+") as json_file:
            return json.load(json_file)

    def __build_tree(self, data: dict, parent_node: Node | None = None) -> Node:
        """Build the tree from the JSON data.

        Parameters
        ----------
        data : dict
            The JSON data to build the tree from.
        parent_node : Node, optional
            The parent node of the current node, by default None

        Returns
        -------
        Node
            The root node of the tree.

        """
        node = Node(
            name=data["name"],
            size=data["size"],
            time_modified_int=data["time_modified"],
            permissions=data["permissions"],
            is_directory="contents" in data,
            parent_node=parent_node,
        )
        if node.is_directory:
            for child in data["contents"]:
                node.add_child(self.__build_tree(child, parent_node=node))
        return node

    def ls(
        self,
        *,
        include_all_details: bool | None,
        show_hidden_files: bool | None,
        sort_in_reverse: bool | None,
        sort_by_last_modified_time: bool | None,
        display_sizes_in_human_readable_format: bool | None,
        filter_by_type: str | None,
        name_or_path_to_node: str | None,
    ) -> str:
        """List the contents of the file system.

        Parameters
        ----------
        include_all_details : bool, optional
            Whether to list in long format, by default False
        show_hidden_files : bool, optional
            Whether to list all files, by default False
        sort_in_reverse : bool, optional
            Whether to list in reverse order, by default False
        sort_by_last_modified_time : bool, optional
            Whether to sort by time, by default False
        display_sizes_in_human_readable_format : bool, optional
            Whether to print the size in human-readable format, by default False
        filter_by_type : str, optional
            Whether to filter by directory or file, by default None
        name_or_path_to_node : Node, optional
            Name or tath to the directory to list or file, by default None

        Returns
        -------
        list[str]
            The list of contents of the directory

        """
        child_nodes: list[Node] = []
        nodes: list[Node] = []
        node_: Node | None = self.fetch_node(name_or_path_to_node)

        if node_ is None:
            return f"error: cannot access {name_or_path_to_node}: \
                No such file or directory"

        if node_.is_directory:
            child_nodes = self.get_child_nodes(node_)
            sort_key: Callable[..., int] | Callable[..., str] = self.get_sort_key(
                sort_by_time=bool(sort_by_last_modified_time),
            )
            nodes = self.sort_nodes(
                nodes=child_nodes,
                sort_key=sort_key,
                reverse=bool(sort_in_reverse),
            )
            if not show_hidden_files:
                nodes = [child for child in nodes if not child.is_hidden]
        else:
            nodes = [node_]

        if filter_by_type is not None:
            nodes = self.filter_nodes(
                nodes=nodes,
                filter_by=filter_by_type,
            )

        return self.build_output(
            nodes=nodes,
            include_all_details=bool(include_all_details),
            display_sizes_in_human_readable_format=bool(
                display_sizes_in_human_readable_format,
            ),
        )

    def fetch_node(self, name_or_path_to_node: str | None) -> Node | None:
        """Fetch a node from the file system.

        Parameters
        ----------
        name_or_path_to_node : str | None
            The path to the node.

        Returns
        -------
        Node | None
            The node at the specified path.

        """
        return (
            self.root
            if name_or_path_to_node == "." or name_or_path_to_node is None
            else self.root.get_child(name_or_path_to_node)
        )

    def get_child_nodes(self, node: Node) -> list[Node]:
        """Get the child nodes of a node.

        Parameters
        ----------
        node : Node
            The node to get the child nodes of.

        Returns
        -------
        list[Node]
            The list of child nodes.

        """
        return list(node.children.values()) if node.children else []

    def sort_nodes(
        self,
        nodes: list[Node],
        sort_key: Callable[..., int] | Callable[..., str],
        *,
        reverse: bool,
    ) -> list[Node]:
        """Sort a list of nodes.

        Parameters
        ----------
        nodes : list[Node]
            The list of nodes to sort.
        sort_key : Callable[..., int] | Callable[..., str]
            The sort key function.
        reverse : bool
            Whether to sort in reverse order.

        Returns
        -------
        list[Node]
            The sorted list of nodes.

        """
        return sorted(nodes, key=sort_key, reverse=reverse)

    def get_sort_key(
        self,
        *,
        sort_by_time: bool,
    ) -> Callable[..., int] | Callable[..., str]:
        """Get the sort key function.

        Parameters
        ----------
        sort_by_time : bool
            Whether to sort by time.

        Returns
        -------
        Callable[..., int] | Callable[..., str]
            The sort key function.

        """

        def sort_key_by_time(child: Node) -> int:
            return child.time_modified_int

        def sort_key_by_name(child: Node) -> str:
            return child.name

        return sort_key_by_time if sort_by_time else sort_key_by_name

    def filter_nodes(
        self,
        nodes: list[Node],
        filter_by: str,
    ) -> list[Node]:
        """Filter a list of nodes.

        Parameters
        ----------
        nodes : list[Node]
            The list of nodes to filter.
        filter_by : str
            The filter type.

        Returns
        -------
        list[Node]
            The filtered list of nodes.

        """
        if filter_by == "dir":
            return [child for child in nodes if child.is_directory]
        if filter_by == "file":
            return [child for child in nodes if not child.is_directory]
        return nodes

    def build_output(
        self,
        nodes: list[Node],
        *,
        include_all_details: bool,
        display_sizes_in_human_readable_format: bool,
    ) -> str:
        """Build the output of the file system.

        Parameters
        ----------
        nodes : list[Node]
            The list of nodes to build the output for.
        include_all_details : bool
            Whether to use long format.
        display_sizes_in_human_readable_format : bool
            Whether to use human readable format.

        Returns
        -------
        str
            The output of the file system.

        """
        node_length = len(nodes)
        if include_all_details:
            return "\n".join(
                [
                    "\t".join(
                        [
                            child.permissions,
                            child.human_readable_size
                            if display_sizes_in_human_readable_format
                            else str(child.size),
                            child.time_modified,
                            child.relative_path if node_length == 1 else child.name,
                        ],
                    )
                    for child in nodes
                ],
            )
        return "\t".join(
            [
                child.relative_path if node_length == 1 else child.name
                for child in nodes
            ],
        )
