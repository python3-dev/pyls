<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="docs/pyls.png" alt="pyls logo"></a>
</p>

<h3 align="center">pyls</h3>

---

<p align="center"> 
Python implementation of 'ls'. </br>
List information about the FILEs (the current directory by default).
</p>


## About

pyls is a Python implementation of 'ls'. It can be used to list information about the PATHs (the current directory by default).

pyls uses a tree structure - directories being the nodes (unless it is an empty directory) and files being the leaf nodes - in the backend to represent the filesystem, making it flexible and easy to use.

pyls has no dependencies other than Python 3.12 or higher.

Furthermore, pyls has a time-complexity of O(1) to fetch information from the immediate children of a node, and O(n) to fetch information from the entire tree. For very large and complex filesystem trees, the time-complexity could further be improved using a breadth-first or depth-first search (not yet implemented).

### Prerequisites

pyls can be installed on any system with python 3.12 or higher.


### Installing

```shell
git clone https://github.com/python3-dev/pyls.git
pip install .
```

## Running the tests

```shell
git clone https://github.com/python3-dev/pyls.git
pip install pytest
pytest
```

## Usage

After the installation, pyls could be used just like ls.

The following options are currently available.

```
usage: pyls [OPTION]... [PATH]...

pyls -l -r -t -h --filter=[dir, file] <path> --help

positional arguments:
  path                  path to list

options:
  -A                    do not ignore entries starting with .
  -l                    use a long listing format
  -r                    reverse order while sorting
  -t                    sort by time, newest first
  -h                    with -l, print sizes like 1K 234M 2G etc.
  --filter [{dir,file}] filter results by type: 'dir' or 'file'
  --help                Show this help message and exit
```


## Built Using

- [Python](https://www.python.org/)
- [Pytest](https://pytest.org/)


## Authors

- [Pratheesh Prakash](https://github.com/python3-dev)

## License

[GNU General Public License](https://fsf.org/licensing/licenses/gpl-3.0.html)