import json
import networkx as nx
import matplotlib.pyplot as plt
import os
import socket
import sys
import pickle

# Developed by Dimitris Mendrinos

class TopologyManager:

    """
    This is a Topology Manager for Software Defined Networks.
    From this Python Program we can extract from a JSON Configuration file
    the topology of a Software Defined Network, collect information and manage
    the network. The basic functionality of this component is to calculate and
    return path(s) from a source to a destination(s) based on a tag.
    """

    #Dictionaries with information from JSON file

    ips = {}
    macs = {}
    switches = []
    links= {}

    # Create a NetworkX Graph
    Graph = nx.Graph()

    #Initialize the Class
    def __init__(self):
        #At the begging call loadConfig method
        self.loadConfig(self.Graph)


    # In this method we read the Topology from Json file and
    # create a Graph from it.
    def loadConfig(self,Graph):
        with open(os.path.expanduser('~/PycharmProjects/SDN_Topology_Management/Configuration')) as data_file:
            data = json.load(data_file)
        for i in data['hosts']:
            self.ips[i] = data['hosts'][i]['ip']
            self.macs[i] = data['hosts'][i]['mac']
            Graph.add_node(i,color = data['hosts'][i]['color'])
        for j in data['switches']['names']:
            Graph.add_node(j)
            self.switches.append(j)
        for k,v in data['link'].items():
            Graph.add_edge(v[0],v[1],name = k)
            self.links[k] = v

    #We can add tag to a Node
    def add_tag(self,G,fnode,attr,value):
        for node in G.nodes():
            if node == fnode:
               attrs = {node: {attr: value}}
               nx.set_node_attributes(G,attrs)
    #We can remove a tag from a Node
    def remove_tag(self,G,fnode,attr):
        G.node[fnode].pop(attr,None)

    # Given a source and a destination node
    # We found the shortest path and return all the links
    # of the shortest path from the Graph.
    def get_shortest_path(self,G,src,dst):
        nodes = nx.shortest_path(G, source=src, target=dst)
        attr = nx.get_edge_attributes(G,'name')
        path = []
        for n in range(0,len(nodes)-1):
            try:
                path.append(attr[(nodes[n],nodes[n+1])])
            except:
                path.append(attr[(nodes[n+1],nodes[n])])

        return path

    # Given an attribute and a value we return all nodes
    # where satisfy that rule. E.g return wich nodes have 'color = red' or bandwidth >10
    def get_dest_by_eq_attribute(self,G,attr,value):
        dest = []
        for node in G:
            if node not in self.switches:
                if G.node[node][attr] == value:
                    dest.append(node)
        return dest

    def get_dest_by_geq_attribute(self,G,attr,value):
        dest = []
        for node in G:
            if node not in self.switches:
                if G.node[node][attr] >= value:
                    dest.append(node)
        return dest

    def get_dest_by_leq_attribute(self,G,attr,value):
        dest = []
        for node in G:
            if node not in self.switches:
                if G.node[node][attr] <= value:
                    dest.append(node)
        return dest


    # Calculate the Forwarding Identifier (FID) of the
    # requested path or paths (multicast?)
    def get_FID(self, path):
        bf = '0000000000'
        for i in path:
            bf = bin(int(bf,2) | int(i,2))
        return bf[2:]
    #In this method we can plot the Graph if we want to.
    def printGraph(self,Graph):
        color_map = []
        for node in Graph:
            if node in self.switches:
                color_map.append('grey')
            else:
                color_map.append(Graph.node[node]['color'])


        edge_labels = nx.get_edge_attributes(Graph, 'name')
        pos = nx.spring_layout(Graph, k=0.5, iterations=50)
        color_map.append('green')
        nx.draw(Graph, pos, node_size=800, node_color=color_map, with_labels=True)
        nx.draw_networkx_edge_labels(Graph, pos, edge_labels=edge_labels)
        plt.savefig("simple_path.png")  # save as png
        plt.show()  # display
TopologyManager()