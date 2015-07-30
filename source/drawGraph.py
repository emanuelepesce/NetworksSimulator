#----------------------------------------------------------------------
# drawDirectedGraph
#
# Contains a function for drawing a directed graph using igraph library
# 
# Author: Emanuele Pesce
#----------------------------------------------------------------------
import networkx as nx
import matplotlib.pyplot as plt

def simplePlot(graph, layout = "shell", nodeSize= 600, widthEdge=2):
    """ Plot a directed graph using igraph library.
        
        @type graph: graph
        @param graph: a graph to plot
        @type layout: string
        @param layout: node position method (shell, circular, random, spring, spectral)

    """
    G=nx.DiGraph()
    for node in graph.keys():
        G.add_node(node)
  
    #add edges
    for v1 in graph.keys():
       for v2 in graph[v1]:
          G.add_edge(v1, v2)
  
    # draw graph
    if layout == 'circular':
      pos = nx.circular_layout(G)
    elif layout == 'random':
      pos = nx.random_layout(G)
    elif layout == 'spring':
      pos = nx.random_layout(G)
    elif layout == 'spectral':
      pos = nx.spectral_layout(G)
    else:
      pos = nx.shell_layout(G)
  
    nx.draw(G, pos, edge_color='#796d54', alpha=1, node_color='#4370D8',cmap=plt.cm.Blues, node_size=nodeSize, width=widthEdge)
  
    plt.show()

if __name__ == "__main__":
  
  simple = dict()
  simple[0] = {1,2}
  simple[1] = {2}
  simple[2] = {3,0}
  simple[3] = {4}
  simple[4] = {0}
  
  simplePlot(simple, "circular")
  



  
  
