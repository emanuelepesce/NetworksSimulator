#----------------------------------------------------------------------
# NaiveDirectedGraph
#
# Contains the class which implements a directed naive graph
# 
# Author: Emanuele Pesce
#----------------------------------------------------------------------
import drawGraph as dg

class NaiveDirectedGraph:
    """ Simple Graph class which contains basics graph methods """
    
    '''========= constructor ========='''    
    def __init__(self, graphDict={}, filename=""):
        """ constructor
        
            @type graphDict: graph
            @param graphDict: a graph in a dictionary structure
        """
        if len(filename) > 0:
            self.graphDict = self.readGraph(filename)
        else:
            self.graphDict = graphDict
    
    '''========= graph get methods ========='''
    def getGraph(self):
        """ return the dictionary structure containing the graph """
        return self.graphDict
    
    def vertices(self):
        """ Return the vertices of a graph """
        return list(self.graphDict.keys())

    def edges(self):
        """ Return a list of the edges of the graph 
            (Edges need to be generated).
            Useful for visualization.
        """
        edges = []
        for vertex in self.graphDict:
            for neighbour in self.graphDict[vertex]:
                edges.append({vertex, neighbour})
        return edges        
        
    def numOfEdges(self):
        """ Return the number of the edges of a graph """
        return len(self.edges())
 
    def numOfVertices(self):
        """ Return the number of the edges of a graph """
        return len(self.vertices())
     
    def readGraph(self, filename):
        """ Read filename and return the graph in a dictionary structure
        
            @type filename: string        
            @param filename: name of the file coitaining the graph
            
            @rtype: graph
            @return: graph 
    
        """
        infile = open(filename,"r")
        graph = {}
        for line in infile:
          if "#" not in line: # commented line
            u,v = line.split()
            if u not in graph:
              graph[u] = set()
            graph[u].add(v)
            if v not in graph:
              graph[v] = set()
        return graph     
     
    ''' ========= graph add methods ========='''
    def addVertex(self, vertex):
        """ Add a vertex to the graph.
            If vertex is already in graph it doeas nothing
            
            @type vertex: vertex
            @param vertex: vertex to add
        """
        if vertex not in self.graphDict:
            self.graphDict[vertex] = []
    
    def addEdge(self, vertex1, vertex2):
        """ Add an edge to the graph between the pair "vertex1-vertex2"s
            
            @type vertex1: vertex
            @param vertex1 -- vertex of the graph
            @type vertex2: vertex
            @param vertex2 -- vertex of the graph
        """
        if vertex1 in self.graphDict and vertex2 in self.graphDict:
            self.graphDict[vertex1].append(vertex2)
    
    '''========= graph utility methods =========''' 
    def plot(self, layout = "circular", nodeSize= 600, widthEdge=2):
        """ plot the graph 
            
            @type nodeSize: integer
            @param nodeSize: integer
            @type widthEdge: integer
            @param widthEdge: integer
        """
        dg.simplePlot(self.graphDict, layout, nodeSize, widthEdge)

    '''========= to string ========='''
    def __str__(self):
        res = "vertices: "
        for k in self.graphDict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.edges():
            res += str(edge) + " "
        return res
       
       
if __name__ == "__main__":
    
#    g = { "a" : ["b", "c"],
#          "b" : ["a", "c", "d"],
#          "c" : ["a", "b", "e"],
#          "d" : ["b", "e", "f"],
#          "e" : ["c", "d", "f"],
#          "f" : ["d", "e"],
#          "h" :  ["l"],
#          "l" : ["a"]
#        }
     
#    g = {"a" : ["b", "c"],
#         "b" : ["c"],
#         "c" : []
#    }
    
    g = {"a" : ["b"],
         "b" : ["a"]
    }
    
    graph = NaiveDirectedGraph(graphDict=g)
    print "--> Graph"
    print graph   

    print "--> number of vertices:"     
    print graph.numOfVertices()
 
    print "--> number of edges:"     
    print graph.numOfEdges()
 
    print "--> adding vertex z"       
    graph.addVertex("z")
    graph.addEdge("a","z")
    graph.addEdge("z","a")
    
    print "--> Graph"
    print graph   

    print "--> number of vertices:"     
    print graph.numOfVertices()
 
    print "--> number of edges:"     
    print graph.numOfEdges()   

    
    graph.plot(widthEdge=1)
    
    ''' ====== TEST IMPORT ===== '''
    fb_graph = NaiveDirectedGraph(filename = "./../data/Facebook.txt")
    
    wikivote = NaiveDirectedGraph(filename = "./../data/Wiki_Vote.txt")
        
