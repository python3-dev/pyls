"""Unittest cases for Node class."""

import json
from pathlib import Path

import pytest

from src.core.node import Node

with Path("structure.json").open(mode="r+") as json_file:
    structure_data = json.load(json_file)


@pytest.fixture
def hidden_node_1() -> Node:
    """Fixture for hidden file Node class."""
    name = ".gitignore"
    size = 8911
    time_modified = 1699941437
    permissions = "drwxr-xr-x"

    return Node(
        name=name,
        time_modified_int=time_modified,
        size=size,
        permissions=permissions,
    )


@pytest.fixture
def node_1() -> Node:
    """Fixture for file Node class."""

    name = "LICENSE"
    size = 1071
    time_modified = 1699941437
    permissions = "drwxr-xr-x"

    return Node(
        name=name,
        time_modified_int=time_modified,
        size=size,
        permissions=permissions,
    )


@pytest.fixture
def node_2() -> Node:
    """Fixture for directory Node class."""

    name = "ast"
    size = 4096
    time_modified = 1699941437
    permissions = "drwxr-xr-x"

    return Node(
        name=name,
        time_modified_int=time_modified,
        size=size,
        permissions=permissions,
        is_directory=True,
    )


@pytest.fixture
def node_3() -> Node:
    """Fixture for directory Node class."""

    name = "bst"
    size = 4096
    time_modified = 1699941437
    permissions = "drwxr-xr-x"

    return Node(
        name=name,
        time_modified_int=time_modified,
        size=size,
        permissions=permissions,
        is_directory=True,
    )


def test_hidden_node(hidden_node_1: Node) -> None:
    """Test hidden node."""
    assert hidden_node_1.name == ".gitignore"
    assert hidden_node_1.is_directory is False
    assert hidden_node_1.size == 8911
    assert hidden_node_1.time_modified_int == 1699941437
    assert hidden_node_1.permissions == "drwxr-xr-x"
    assert hidden_node_1.children is None
    assert hidden_node_1.time_modified == "Nov 14 05:57"
    assert hidden_node_1.is_hidden
    assert hidden_node_1.human_readable_size == "8.7K"

def test_visible_node(node_1: Node) -> None:
    """Test visible node."""
    assert node_1.name == "LICENSE"
    assert node_1.is_directory is False
    assert node_1.size == 1071
    assert node_1.time_modified_int == 1699941437
    assert node_1.permissions == "drwxr-xr-x"
    assert node_1.children is None
    assert node_1.time_modified == "Nov 14 05:57"
    assert node_1.is_hidden is False
    assert node_1.human_readable_size == "1.0K"


def test_visible_directory_node(node_2: Node) -> None:
    """Test visible directory node."""
    assert node_2.name == "ast"
    assert node_2.is_directory is True
    assert node_2.size == 4096
    assert node_2.time_modified_int == 1699941437
    assert node_2.permissions == "drwxr-xr-x"
    assert node_2.children is not None
    assert node_2.time_modified == "Nov 14 05:57"
    assert node_2.is_hidden is False
    assert node_2.human_readable_size == "4.0K"

def test_add_child_valid(node_1: Node, node_2: Node) -> None:
    """Test add_child method of Node class."""
    node_2.add_child(node_1)
    assert node_2.children is not None
    assert node_2.children[node_1.name] == node_1

def test_add_child_invalid(node_1: Node, node_2: Node) -> None:
    """Test add_child method of Node class."""
    with pytest.raises(ValueError):
        node_1.add_child(node_2)

def test_get_child_valid(node_1: Node, node_2: Node) -> None:
    """Test get_child method of Node class."""
    node_2.add_child(node_1)
    child_node = node_2.get_child(node_1.name)
    assert child_node is not None
    assert child_node.name == node_1.name

def test_add_child_valid_path(node_1: Node, node_2: Node, node_3: Node,) -> None:
    """Test get_child method of Node class."""
    node_3.add_child(node_2)
    node_2.add_child(node_1)
    assert node_2.children is not None
    assert node_3.children is not None
    assert node_2.children[node_1.name] == node_1
    assert node_3.children[node_2.name] == node_2
    child_node = node_3.get_child(f"{node_2.name}/{node_1.name}")
    assert child_node is not None
    assert child_node.name == node_1.name

def test_node_get_child_invalid_name(node_2: Node) -> None:
    """Test get_child method of Node class with invalid name."""
    invalid_name = "invalid_name"
    child_node = node_2.get_child(invalid_name)
    assert child_node is None


def test_node_get_child_invalid_path(node_2) -> None:
    """Test get_child method of Node class with invalid path."""
    invalid_path = "invalid/path"
    child_node = node_2.get_child(invalid_path)
    assert child_node is None


@pytest.mark.parametrize(
        "size,expected",
        [
            ((0), "0"),
            ((1023), "1023"),
            ((1024), "1.0K"),
            ((1024 * 1024), "1.0M"),
            ((1024 * 1024 * 1024), "1.0G"), 
            ((1024 * 1024 * 1024 * 1024), "1.0T"),
            ((1024 * 1024 * 1024 * 1024 * 1024), "1.0P"),
            ((1024 * 1024 * 1024 * 1024 * 1024 * 1024), "1.0E"),
            ((1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024), "1.0Z"),
    ],
    )
def test_node_human_readable_size_large(size: int, expected: str) -> None:
    """Test human_readable_size property of Node class with large size."""
    node = Node(name="name", size=size, is_directory=False, permissions="drwxr-xr-x", time_modified_int=0,)
    assert node.human_readable_size == expected
