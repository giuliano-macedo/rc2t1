#!/usr/bin/env python3
from core import Emulator,VirtualTopo
import os
import argparse

if os.geteuid()!=0:
	print("You must be root to run this program")
	exit()
parser=argparse.ArgumentParser()
parser.add_argument("-n","--nodes",nargs="?",dafault=5,type=int)
parser.add_argument("-v","--volume",nargs="?",dafault=.5,type=float)
args=parser.parse_args()

assert 1  <=args.n     <=23
assert 0.0<=args.volume<=1.0

virtual_topo=VirtualTopo(args.nodes,volume=args.volume)
virtual_topo.savefig("virtual_topo.pdf")
emu=Emulator(virtual_topo)
emu.savefig("map.pdf")
emu.start()