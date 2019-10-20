#!/usr/bin/env python3
from core import Emulator,VirtualTopo
import os
import argparse

if os.geteuid()!=0:
	print("You must be root to run this program")
	exit()
parser=argparse.ArgumentParser()
parser.add_argument("-n","--nodes",nargs="?",default=5,type=int)
parser.add_argument("-v","--volume",nargs="?",default=.5,type=float)
parser.add_argument("--min-weight",nargs="?",default=1,type=int)
parser.add_argument("--max-weight",nargs="?",default=20,type=int)
args=parser.parse_args()

assert 1  <=args.nodes <=23
assert 0.0<=args.volume<=1.0

virtual_topo=VirtualTopo(args.nodes,volume=args.volume,min_weight=args.min_weight,max_weight=args.max_weight)
virtual_topo.savefig("virtual_topo")
emu=Emulator(virtual_topo)
emu.savefig("map")
emu.net.pingAll()
emu.start()