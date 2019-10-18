from mininet.topo import Topo as mininet_topo
from mininet.node import Node as mininet_node
from mininet.net  import Mininet as mininet_Mininet
from mininet.cli  import CLI as mininet_CLI
from mininet.link import TCLink as mininet_TCLink
import mininet.log
from namedlist import namedlist

class LinuxRouter( mininet_node ):
	"""A Node with IP forwarding enabled.
	Means that every packet that is in this node, comunicate freely with its interfaces."""

	def config( self, **params ):
		super( LinuxRouter, self).config( **params )
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )

	def terminate( self ):
		self.cmd( 'sysctl net.ipv4.ip_forward=0' )
		super( LinuxRouter, self ).terminate()

class Command(namedlist("Command",["node","cmd"])):
	pass
class Node():
	def __init__(self,name):
		self.name=name
		self.edges=[]
	def __iadd__(self,obj):
		self.edges.append(obj)
	def __str__(self):
		return self.name
	def __repr__(self):
		return str(self)
class Edge(namedlist("Edge",["ip","dest","delay"])):
	pass
class Topo( mininet_topo ):
	def __init__(self,virtual_topo,*args,**kwargs):
		self.virtual_topo=virtual_topo
		self.nodes_list=[]
		self.cmds=[]
		super(Topo,self).__init__(*args,**kwargs)
	def __add_node(self,name):
		self.addNode(name,cls=LinuxRouter,ip=None)
		self.nodes_list.append(Node(name))
	def __add_edge(self,l,r,i,delay):
		edge1=Edge(
			ip		  =f"10.0.{i}.1",
			dest      =r,
			delay	  =delay
		)
		edge2=Edge(
			ip		  =f"10.0.{i}.2",
			dest      =l,
			delay	  =delay
		)
		self.addLink(
			l.name,
			r.name,
			params1={"ip":f"{edge1.ip}/24"},
			params2={"ip":f"{edge2.ip}/24"},
			delay=f"{delay}ms"
		)
		print((l.name,r.name,edge1.ip,edge2.ip))
		if r.edges: # if already have edges
			self.cmds.append(Command(l.name,f"ip route add {r.edges[0].ip} via {edge2.ip}"))
		if l.edges:
			self.cmds.append(Command(r.name,f"ip route add {l.edges[0].ip} via {edge1.ip}"))
		l+=edge1
		r+=edge2
	def build( self, **kwargs ):
		for node in self.virtual_topo.nodes:
			self.__add_node(node.name.replace("v","r"))
		for i,(li,ri) in enumerate(self.virtual_topo.pairs):
			l=self.nodes_list[li]
			r=self.nodes_list[ri]
			weight=self.virtual_topo.nodes[li][self.virtual_topo.nodes[ri]].weight
			self.__add_edge(l,r,i,weight)

class Emulator():
	def __init__(self,virtual_topo):
		max_nodes=23
		if len(virtual_topo.nodes)>max_nodes:
			raise RuntimeError(f"Network cant have more than {max_nodes} nodes")
		#create all mininet stuff and configure route tables
		mininet.log.setLogLevel( 'info' )
		topo=Topo(virtual_topo)
		self.net = mininet_Mininet( topo=topo ,link=mininet_TCLink)
		self.net.start()
		for cmd in self.net.topo.cmds:
			print(cmd.node,cmd.cmd)
			self.net[cmd.node].cmd(cmd.cmd)
	def pingAll(self,timeout=10):
		self.net.pingAll(timeout)
	def start(self):
		mininet_CLI( self.net )
	def __del__(self):
		self.net.stop()
if __name__=="__main__":
	from VirtualTopo import VirtualTopo
	virtual_topo=VirtualTopo(4,volume=.75)
	virtual_topo.view()

	Emulator(virtual_topo).start()