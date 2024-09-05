"""Unit tests for FileSystem class."""

import pytest
from pathlib import Path
from src.core import FileSystem
from src.core.node import Node

def test_file_system_init() -> None:
    file_system = FileSystem("structure.json")
    assert file_system.json_path == Path("structure.json")

def test_file_system_load_json() -> None:
    file_system = FileSystem("structure.json")
    assert isinstance(file_system.json_data, dict)

def test_file_system_build_tree() -> None:
    file_system = FileSystem("structure.json")
    assert isinstance(file_system.root, Node)

def test_file_system_ls() -> None:
    file_system = FileSystem("structure.json")
    contents = file_system.ls(
        include_all_details=True,
        show_hidden_files=True,
        sort_in_reverse=True,
        sort_by_last_modified_time=True,
        display_sizes_in_human_readable_format=True,
        filter_by_type=None,
        name_or_path_to_node="parser",
    )
    assert isinstance(contents, str)
    assert contents == "drwxr-xr-x\t1.3K\tNov 17 07:21\tparser_test.go\n-rw-r--r--\t1.6K\tNov 17 06:35\tparser.go\ndrwxr-xr-x\t533\tNov 14 10:33\tgo.mod"

def test_file_system_fetch_node() -> None:
    file_system = FileSystem("structure.json")
    node = file_system.fetch_node("path/to/node")
    assert isinstance(node, Node) or node is None

def test_file_system_get_child_nodes() -> None:
    file_system = FileSystem("structure.json")
    node = file_system.fetch_node("parser")
    assert node is not None
    child_nodes = file_system.get_child_nodes(node)
    assert isinstance(child_nodes, list)

def test_file_system_sort_nodes() -> None:
    file_system = FileSystem("structure.json")
    node = file_system.fetch_node("parser")
    assert node is not None
    child_nodes = file_system.get_child_nodes(node)
    sort_key = file_system.get_sort_key(sort_by_time=True)
    sorted_nodes = file_system.sort_nodes(child_nodes, sort_key=sort_key, reverse=True)
    assert isinstance(sorted_nodes, list)

def test_file_system_get_sort_key() -> None:
    file_system = FileSystem("structure.json")
    sort_key = file_system.get_sort_key(sort_by_time=True)
    assert callable(sort_key)

def test_file_system_invalid_json_path() -> None:
    with pytest.raises(FileNotFoundError):
        FileSystem("invalid.json")

def test_file_system_invalid_node_path() -> None:
    file_system = FileSystem("structure.json")
    assert file_system.fetch_node("invalid/path") is None