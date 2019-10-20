# Dijkstra based routing in mininet

Creates a random topology in mininet with random edge weights applied to links delay, and use dijikstra 
algorithm to create minimal cost routes to every node.

## Prerequisites

* python 3.7 (3.5 won't work, some source files have literal string interpolation)
* pip
* mininet

## Installing

Install all dependecies described in `requirements.txt` using pip

```bash
pip install -r requirements.txt
```

## Usage
cd to the src directory 

```bash
cd src
```
and run `main.py` with root priveleges
```bash
sudo ./main.py
```
see `./main.py --help` for more options
after executing, you will have a mininet CLI, and the program will save in the same folder the following files

* `virtual_topo.pdf` : the graph
* `map.pdf`: the network topology
* `diji.pdf`: being i the node index, the minimal cost tree for each node

