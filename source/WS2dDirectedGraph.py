#----------------------------------------------------------------------
# WS2dDirectedGraph
#
# Contains the class which implements a Watts-Strogats 2d Directed Graph
# 
# Author: Emanuele Pesce
#----------------------------------------------------------------------
import NaiveDirectedGraph as dg
import random 
import math

class WS2dDirectedGraph(dg.NaiveDirectedGraph):
    """ Watts-Strogats 2d Directed Graph class. Extends NaiveDirected Class.
    """
    
    '''========= constructor ========='''    
    def __init__(self, n=16, r=4, k=2, e_inf = 0, e_sup = 0, graphDict={}):
        """ Constructor
            
            @type n: integer
            @param n: number of nodes
            @type r: integer
            @param r: radius of each node: a node u is connected with each other node at distance at most r (strong ties)
            @type k: integer
            @param k: number of random edges for each node u (weak ties)
            @type graphDict: graph            
            @param graphDict: if graphDict is not passed, it will be generated
        """
        self.r = r
        self.k = k
        if e_sup > 0:
            self.n = n
            self.graphDict = self.genWS2dGraph_control(self.n,self.r, self.k, e_inf, e_sup)
        elif len(graphDict) < 1:
            self.n = n
            self.graphDict = self.genWS2dGraph(self.n,self.r, self.k)
        else:
            self.n = len(graphDict)
            self.graphDict = graphDict

   
    def genWS2dGraph(self, n, r, k):
        """ 
            Generates a WS-2D-graph. This method is called by the constructors.
            
            @type n: integer
            @param n: number of nodes
            @type r: integer
            @param r: radius of each node: a node u is connected with each other node at distance at most r (strong ties)
            @type k: integer
            @param k: number of random edges for each node u (weak ties)
            
            @return: a WS 2d graph
        """
        line = int(math.sqrt(n))
        graph = dict()
        ''' Initialization '''
        for i in range(n):
            x = random.random()
            y = random.random()
            graph[i] = dict()
            graph[i]["x"] = x*line
            graph[i]["y"] = y*line
            graph[i]["list"] = set()
            
        ''' build SW 2d Graph '''
        for i in range(n):
            ''' 
                set strong ties:
                for each node u we set edge with all neighbors i a radious of r
            '''
            for j in range(i+1,n):               
                dist=math.sqrt((graph[i]["x"]-graph[j]["x"])**2 +       (graph[i]["y"]-graph[j]["y"])**2) # Eclidean distance between i and j
                if dist <= r:
                    graph[i]["list"].add(j)               
                    graph[j]["list"].add(i)
            ''' 
                set weak ties:
                for each node u we set k edges to random nodes 
            '''
            for h in range(k):
                s = random.randint(0,n-1)
                if s != i:
                    graph[i]["list"].add(s)                  
        return graph
        

    def genWS2dGraph_control(self, n, r, vk, e_inf, e_sup):
        """ 
            Generates a WS-2D-graph with a limited number of edges.
            
            @type n: integer
            @param n: number of nodes
            @type r: integer
            @param r: radius of each node: a node u is connected with each other node at distance at most r (strong ties)
            @type vk: list
            @param vk: list of number of possible weak ties for each node
            @type e_inf: integer
            @param e_inf: inferior limit of edges
            @type e_sup: integer            
            @param e_sup: superior limit of edges 
            
            @return: a WS 2d graph
        """
        line = int(math.sqrt(n))
        graph = dict()
        n_edges = random.randint(e_inf, e_sup)
        ''' Initialization '''
        for i in range(n):
            x = random.random()
            y = random.random()
            graph[i] = dict()
            graph[i]["x"] = x*line
            graph[i]["y"] = y*line
            graph[i]["list"] = set()
        
        times = 0
        ''' build SW 2d Graph '''
        while n_edges > 0:
            for i in range(n):
                ''' 
                    set strong ties:
                    for each node u we set edge with all neighbors i a radious of r
                '''
                for j in range(i+1,n):               
                    dist=math.sqrt((graph[i]["x"]-graph[j]["x"])**2 + (graph[i]["y"]-graph[j]["y"])**2) # Eclidean distance between i and j
                    if dist <= r:
                        if j not in graph[i]["list"]:
                            graph[i]["list"].add(j)
                            n_edges -= 1
                            if n_edges <= 0:
                                print times
                                return graph
                        if i not in graph[j]["list"]:
                            graph[j]["list"].add(i)
                            n_edges -= 1
                            if n_edges <= 0:
                                print times
                                return graph
                ''' 
                    set weak ties:
                    for each node u we set k edges to random nodes 
                '''
                times +=1
                r1 = random.randint(0,len(vk)-1)
                for h in range(vk[r1]):
                    valid = False
                    while valid == False:
                        s = random.randint(0,n-1)
                        if s != i and s not in graph[i]["list"]:
                            valid = True
                    graph[i]["list"].add(s) 
                    n_edges -= 1
                    if n_edges <= 0:
                        print times
                        return graph
        return graph


    
    def getGraph(self):
        """ 
            Overwrite method plot of the superclass
            
            @type widthEdge: integer
            @param widthEdge: Width of the edges to plot
        """
        g = {}
        graph = self.graphDict
        for v in graph.keys():
#            print v
#            print graph[v]["list"]
            g[v] = graph[v]["list"]      
        gr = dg.NaiveDirectedGraph(graphDict=g)
        return gr.getGraph()
    
    def plot(self, widthEdge=1):
        """ 
            Overwrite method plot of the superclass
            
            @type widthEdge: integer
            @param widthEdge: Width of the edges to plot
        """
        g = {}
        graph = self.graphDict
        for v in graph.keys():
#            print v
#            print graph[v]["list"]
            g[v] = graph[v]["list"]      
        gToPlot = dg.NaiveDirectedGraph(graphDict=g)
        gToPlot.plot(widthEdge=1)
        
        
        
    
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

    graph = WS2dDirectedGraph(7115, 2, [5,10,25], 75000, 125000)
    print "Graph"

            
