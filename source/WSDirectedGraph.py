#----------------------------------------------------------------------
# WSDirectedGraph
#
# Contains the class which implements a Watts-Strogats Directed Graph
# 
# Author: Emanuele Pesce
#----------------------------------------------------------------------
import NaiveDirectedGraph as dg
import random 
import math

class WSDirectedGraph(dg.NaiveDirectedGraph):
    """ Watts-Strogats Directed Graph class. Extends NaiveDirected Class.
    """
    
    '''========= constructor ========='''    
    def __init__(self, n=16, r=4, k=2, graphDict={}):
        """ Constructor
        
            @type n: integer
            @param n: number of nodes
            @type r: integer
            @param r: radius of each node: a node u is connected with each other node at distance at most r (strong ties)
            @type k: integer
            @param k: number of random edges for each node u (weak ties)
            @type graphDict: graph            
            @param graphDict: if graphDict is not passed, it will be generated
            Keyword arguments:
        """
        self.r = r
        self.k = k
        if len(graphDict) < 1:
            self.n = n           
            self.graphDict = self.genWSGraph(self.n,self.r, self.k)
        else:
            self.n = len(self.graphDict)
            self.graphDict = graphDict

   
    def genWSGraph(self, n, r, k):
        """ Generate a Watts-Strogats graph
            
            @type n: integer
            @param n: number of nodes
            @type r: integer
            @param r: radius of each node: a node u is connected with each other node at distance at most r (strong ties)
            @type k: integer
            @param k: number of random edges for each node u (weak ties)
            
            @return: a WS graph
            Keyword arguments:
        """
        line = int(math.sqrt(n))
        graph = {}
        ''' Inizialization: 
            we can see the graph as a grid where each node is identified 
            by a number in range [0,n-1]
        '''
        for i in range(line):
            for j in range(line):
                graph[i*line+j] = set()      
        ''' build WS graph '''
        for i in range(line):
            ''' set strong ties:
                for each node u we set edge with all neighbors i a radious of r
            '''
            for j in range(line):
                for x in range(r+1):
                    for y in range(r+1):
                        if x+y > 0: # the sum of offsets must be at least 1
                            if i+x < line: # check for not going out the grid
                                if   j+y < line:
                                    graph[i*line+j].add((i+x)*line+(j+y))
                                if  j-y >= 0:
                                    graph[i*line+j].add((i+x)*line+(j-y))                      
                            if i-x >= 0:
                                if j+y < line:
                                    graph[i*line+j].add((i-x)*line+(j+y))
                                if j-y >= 0:
                                    graph[i*line+j].add((i-x)*line+(j-y))
                ''' weak ties:
                    for each node u we set k edges to random nodes 
                '''
                for h in range(k):
                    s = random.randint(0,n-1)
                    if s != i*line+j: # s is not the current node
                        graph[i*line+j].add(s)
                
#                        graph[s].add(i*line+j)              
        return graph   

     
if __name__ == "__main__":
    
    g = { "a" : ["b", "c"],
          "b" : ["a", "c", "d"],
          "c" : ["a", "b", "e"],
          "d" : ["b", "e", "f"],
          "e" : ["c", "d", "f"],
          "f" : ["d", "e"],
#          "h" :  ["l"],
#          "l" : ["a"]
        }

    graph = WSDirectedGraph(9, 1, 0)
    print "Graph"
    print graph    
    
    graph.plot(widthEdge=1)  
    

        
