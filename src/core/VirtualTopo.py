import random
from namedlist import namedlist
import graphviz
Connection=namedlist("Connection",["node","weight"])
class Node:
	def __init__(self,name):
		self.name=name
		self.children={}
	def __iadd__(self,node):
		assert isinstance(node,Node)

		self.children[node]=Connection(node=node,weight=-1)
		return self
	def __getitem__(self,node):
		return self.children[node]
	def __iter__(self):
		return iter(self.children.values())
	def __str__(self):
		return self.name
	def __hash__(self):
		return hash(str(self))
	def has_children(self):
		return bool(self.children)
class VirtualTopo:
	def __init__(self,n,nodes_prefix="v",min_weight=1,max_weight=1000):
		self.nodes=[Node(f"{nodes_prefix}{i+1}") for i in range(n)]
		max_connections=(n*(n-1))//2
		no_connections=random.randint(1,max_connections)
		pairs=set()
		random_index=lambda :random.randrange(n)
		while len(pairs)!=no_connections:
			i,j=random_index(),random_index()
			if i==j:
				continue
			pairs.add(frozenset((i,j)))
		for i,j in pairs:
			u,v=self.nodes[i],self.nodes[j]
			print(u,v)
			u+=v
			v+=u
		#connect outliers
		not_outlier_index,not_outlier=next(((i,u) for i,u in enumerate(self.nodes) if u.has_children()))
		for i,u in enumerate(self.nodes):
			if not u.has_children():
				pairs.add(frozenset((i,not_outlier_index)))
				u+=not_outlier
				not_outlier+=u
		#set random weights
		for node in self.nodes:
			for conn in node:
				if conn.weight==-1:
					a=random.randint(min_weight,max_weight)
					conn.weight=a
					conn.node[node].weight=a
	def to_graphviz(self,*args,**kwargs):
		graph=graphviz.Graph(*args,**kwargs)
		sid=lambda obj:str(id(obj))
		for node in self.nodes:
			graph.node(sid(node),label=node.name)
			for conn in node:
				graph.edge(sid(node),sid(conn.node),label=str(conn.weight))
		return graph
if __name__=="__main__":
	topo=VirtualTopo(5)
	topo.to_graphviz(format="pdf").render("tree.dot")
