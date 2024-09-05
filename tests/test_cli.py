"""Unit tests for command-line interface."""

import pytest
import sys
from src.cli.main import create_argument_parser, execute_parser

def test_default_behavior(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls."""
    monkeypatch.setattr(sys, "argv", ["pyls"])
    args = create_argument_parser()
    assert args.path == "."
    assert not args.all_files
    assert not args.long_format
    assert not args.reverse
    assert not args.sort_by_time
    assert not args.human_readable
    assert args.filter is None
    execute_parser()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "LICENSE\tREADME.md\tast\tgo.mod\tlexer\tmain.go\tparser\ttoken\n"

def test_list_all_files(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls -A."""
    monkeypatch.setattr(sys, "argv", ["pyls", "-A"])
    args = create_argument_parser()
    assert args.all_files
    assert args.path == "."
    assert not args.long_format
    assert not args.reverse
    assert not args.sort_by_time
    execute_parser()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == ".gitignore\tLICENSE\tREADME.md\tast\tgo.mod\tlexer\tmain.go\tparser\ttoken\n"

def test_human_readable(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls -h."""
    monkeypatch.setattr(sys, "argv", ["pyls", "-h"])
    args = create_argument_parser()
    assert args.human_readable
    assert args.path == "."
    assert not args.long_format
    assert not args.reverse
    assert not args.sort_by_time
    execute_parser()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "LICENSE\tREADME.md\tast\tgo.mod\tlexer\tmain.go\tparser\ttoken\n"

def test_long_listing_format(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls -l."""
    monkeypatch.setattr(sys, "argv", ["pyls", "-l"])
    args = create_argument_parser()
    assert args.long_format
    assert args.path == "."
    execute_parser()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "drwxr-xr-x\t1071\tNov 14 05:57\tLICENSE\ndrwxr-xr-x\t83\tNov 14 05:57\tREADME.md\n-rw-r--r--\t4096\tNov 14 10:28\tast\ndrwxr-xr-x\t60\tNov 14 08:21\tgo.mod\ndrwxr-xr-x\t4096\tNov 14 09:51\tlexer\n-rw-r--r--\t74\tNov 14 08:27\tmain.go\ndrwxr-xr-x\t4096\tNov 17 07:21\tparser\n-rw-r--r--\t4096\tNov 14 09:27\ttoken\n"

def test_reverse_order(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls -r."""
    monkeypatch.setattr(sys, "argv", ["pyls", "-r"])
    args = create_argument_parser()
    assert args.reverse
    assert args.path == "."
    execute_parser()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "token\tparser\tmain.go\tlexer\tgo.mod\tast\tREADME.md\tLICENSE\n"

def test_sort_by_time_and_filter_files(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls -t --filter=file."""
    monkeypatch.setattr(sys, "argv", ["pyls", "-t", "--filter", "file"])
    args = create_argument_parser()
    assert args.sort_by_time
    assert args.filter == "file"
    execute_parser()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "LICENSE\tREADME.md\tgo.mod\tmain.go\n"

def test_invalid_filter_option(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls --filter=invalid."""
    with pytest.raises(SystemExit):
        monkeypatch.setattr(sys, "argv", ["pyls", "--filter=invalid"])
        create_argument_parser()
    captured = capsys.readouterr()
    assert "invalid choice" in captured.err

def test_with_path_argument_1(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls parser."""
    monkeypatch.setattr(sys, "argv", ["pyls", "parser"])
    args = create_argument_parser()
    assert args.path == "parser"
    execute_parser()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "go.mod\tparser.go\tparser_test.go\n"

def test_with_path_argument_2(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls parser/parser.go."""
    monkeypatch.setattr(sys, "argv", ["pyls", "parser/parser.go"])
    args = create_argument_parser()
    assert args.path == "parser/parser.go"
    execute_parser()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "./parser/parser.go\n"

def test_multiple_arguments_1(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls -l -r -t."""
    monkeypatch.setattr(sys, "argv", ["pyls", "-l", "-r", "-t"])
    args = create_argument_parser()
    assert args.long_format
    assert args.reverse
    assert args.sort_by_time
    assert args.path == "."
    execute_parser()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "drwxr-xr-x\t4096\tNov 17 07:21\tparser\n-rw-r--r--\t4096\tNov 14 10:28\tast\ndrwxr-xr-x\t4096\tNov 14 09:51\tlexer\n-rw-r--r--\t4096\tNov 14 09:27\ttoken\n-rw-r--r--\t74\tNov 14 08:27\tmain.go\ndrwxr-xr-x\t60\tNov 14 08:21\tgo.mod\ndrwxr-xr-x\t1071\tNov 14 05:57\tLICENSE\ndrwxr-xr-x\t83\tNov 14 05:57\tREADME.md\n"

def test_multiple_arguments_2(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls -l -r -t parser."""
    monkeypatch.setattr(sys, "argv", ["pyls", "-l", "-r", "-t", "parser"])
    args = create_argument_parser()
    assert args.long_format
    assert args.reverse
    assert args.sort_by_time
    assert args.path == "parser"
    execute_parser()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "drwxr-xr-x\t1342\tNov 17 07:21\tparser_test.go\n-rw-r--r--\t1622\tNov 17 06:35\tparser.go\ndrwxr-xr-x\t533\tNov 14 10:33\tgo.mod\n"

def test_multiple_arguments_3(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls -l parser -r -t."""
    monkeypatch.setattr(sys, "argv", ["pyls", "-l", "parser", "-r", "-t"])
    args = create_argument_parser()
    assert args.long_format
    assert args.reverse
    assert args.sort_by_time
    assert args.path == "parser"
    execute_parser()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "drwxr-xr-x\t1342\tNov 17 07:21\tparser_test.go\n-rw-r--r--\t1622\tNov 17 06:35\tparser.go\ndrwxr-xr-x\t533\tNov 14 10:33\tgo.mod\n"

def test_help(monkeypatch, capsys) -> None:
    """Test running the command: python -m pyls --help."""
    monkeypatch.setattr(sys, "argv", ["pyls", "--help"])
    with pytest.raises(SystemExit):
        args = create_argument_parser()
        execute_parser()

    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "usage: pyls [OPTION]... [PATH]...\n\npyls: Python implementation of 'ls'.        \n\nList information about the PATHs (the current directory by default).\n        \n\npositional arguments:\n  path                  path to list\n\noptions:\n  -A                    do not ignore entries starting with .\n  -l                    use a long listing format\n  -r                    reverse order while sorting\n  -t                    sort by time, newest first\n  -h                    with -l, print sizes like 1K 234M 2G etc.\n  --filter [{dir,file}]\n                        filter results by type: 'dir' or 'file'\n  --help                Show this help message and exit\n\nGPLv3, Pratheesh Prakash\n"