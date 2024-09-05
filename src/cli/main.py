"""CLI definitions."""

import argparse

from src.core import FileSystem


def create_argument_parser() -> argparse.Namespace:
    """Return the ArgumentParser instance.

    Parses the command line arguments and returns the parser instance.

    Returns
    -------
    parser : ArgumentParser
        The ArgumentParser instance.

    """
    parser = argparse.ArgumentParser(
        prog="pyls",
        description="""pyls: Python implementation of 'ls'.\
        \n\nList information about the PATHs (the current directory by default).
        """,
        formatter_class=argparse.RawTextHelpFormatter,
        usage="pyls [OPTION]... [PATH]...",
        epilog="GPLv3, Pratheesh Prakash",
        add_help=False,
    )

    parser.add_argument(
        "-A",
        dest="all_files",
        action="store_true",
        help="do not ignore entries starting with .",
    )

    parser.add_argument(
        "-l",
        dest="long_format",
        action="store_true",
        help="use a long listing format",
    )

    parser.add_argument(
        "-r",
        dest="reverse",
        action="store_true",
        help="reverse order while sorting",
    )

    parser.add_argument(
        "-t",
        dest="sort_by_time",
        action="store_true",
        help="sort by time, newest first",
    )

    parser.add_argument(
        "-h",
        dest="human_readable",
        action="store_true",
        help="with -l, print sizes like 1K 234M 2G etc.",
    )

    parser.add_argument(
        "--filter",
        dest="filter",
        choices=["dir", "file"],
        help="filter results by type: 'dir' or 'file'",
        nargs="?",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="path to list",
    )

    parser.add_argument(
        "--help",
        action="help",
        help="Show this help message and exit",
    )

    return parser.parse_args()


def execute_parser() -> None:
    """Execute the 'pyls' application.

    Entry point of the 'pyls' application.

    Parses the command line arguments, initialises the file system,
    and calls the 'ls' function to list the files and directories.

    See Also
    --------
    get_parser : Function to generate parser for command line arguments.
    FileSystem : Class representing the file system.

    """
    args: argparse.Namespace = create_argument_parser()
    file_system = FileSystem()

    results: str = file_system.ls(
        include_all_details=args.long_format,
        name_or_path_to_node=args.path,
        show_hidden_files=args.all_files,
        sort_in_reverse=args.reverse,
        sort_by_last_modified_time=args.sort_by_time,
        display_sizes_in_human_readable_format=args.human_readable,
        filter_by_type=args.filter,
    )
    print(results)
