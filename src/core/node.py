"""Node class for the file system."""

from __future__ import annotations

from datetime import UTC, datetime

BYTE_LENGTH: int = 1024


class Node:
    """Node class represents a node in the file system.

    This class represents a node in the file system and provides attributes for
    the node's properties.

    Parameters
    ----------
    name : str
        The name of the node.
    size : int
        The size of the node in bytes.
    time_modified : int
        The time the node was last modified in seconds from epoch.
    permissions : str
        The permissions of the node.
    is_directory : bool, optional
        Whether the node is a directory (default is False).
    parent_node : Node | None, optional
        The parent node of the current node (default is None).

    """

    def __init__(
        self,
        name: str,
        size: int,
        time_modified_int: int,
        permissions: str,
        *,
        is_directory: bool = False,
        parent_node: Node | None = None,
    ) -> None:
        """Initialise a node."""
        self.name: str = name
        self.size: int = size
        self.time_modified_int: int = time_modified_int
        self.time_modified_datetime: datetime = datetime.fromtimestamp(
            self.time_modified_int,
            tz=UTC,
        )
        self.time_modified: str = self.time_modified_datetime.strftime(
            format="%b %d %H:%M",
        )
        self.permissions: str = permissions
        self.is_directory: bool = is_directory
        self.depth: int = 0 if parent_node is None else parent_node.depth + 1
        self.parent_node: Node | None = parent_node
        self.is_hidden: bool = self.name.startswith(".")
        self.children: dict[str, Node] | None = {} if is_directory else None
        self.relative_path: str = f"{parent_node.relative_path if parent_node and \
                                     parent_node.depth > 0 else '.'}/{name}"

    def __repr__(self) -> str:  # pragma: no cover
        """Return a string representation of the node."""
        return self.name

    def __str__(self) -> str:  # pragma: no cover
        """Return a string representation of the node."""
        return self.name

    def add_child(self, node: Node) -> None:
        """Add a child node to the current node.

        This method appends the child node to the list of children if the current
        node is a directory.

        If the current node is not a directory, it raises a ValueError.

        Parameters
        ----------
        node : Node
            The child node to add.

        Raises
        ------
        ValueError
            If the current node is not a directory.

        """
        if self.is_directory and self.children is not None:
            self.children[node.name] = node
        else:
            error_message: str = "Cannot add child to a non-directory node."
            raise ValueError(error_message)

    def get_child(self, name_or_path: str) -> Node | None:
        """Get a child node from the current node.

        This method searches for a child node with the specified name and returns
        it if found.

        If the current node is not a directory or the child node is not
        found, it returns the current node.

        Parameters
        ----------
        name_or_path : str
            The name or path of the child node to retrieve.

        Returns
        -------
        Node
            The child node with the specified name.

        """
        if "/" not in name_or_path:
            if self.is_directory and self.children is not None:
                return self.children.get(name_or_path, None)
            return None

        parts: list[str] = name_or_path.split("/")
        current_node: Node = self
        for part in parts:
            if not current_node.is_directory:
                if current_node.name == part:
                    return current_node
                return None
            child_node: Node | None = (
                current_node.children.get(part, None)
                if current_node.children is not None
                else None
            )
            if child_node is None:
                return child_node
            current_node = child_node
        return current_node

    @property
    def human_readable_size(self) -> str:
        """Get human readable size."""
        units: list[str] = [
            "K",
            "M",
            "G",
            "T",
            "P",
            "E",
            "Z",
        ]
        if self.size < BYTE_LENGTH:
            return str(self.size)

        size_: float = self.size
        for unit in units:
            size_ /= BYTE_LENGTH
            if size_ < BYTE_LENGTH:
                return f"{round(size_, 1)}{unit}"
        return f"{self.size}B"
