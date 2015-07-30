#----------------------------------------------------------------------
# RandomDirectedGraph
#
# Contains the class which implements a directed random graph graph
# 
# Author: Emanuele Pesce
#----------------------------------------------------------------------
import NaiveDirectedGraph as dg
import random 

class RandomDirectedGraph(dg.NaiveDirectedGraph):
    """ Directed Random Graph class. Extends Naive Directed Graph class.
        A p-random graph is a graph in which an edge between two vertices exist
        with a probability p.
    """
    
    '''========= constructor ========='''    
    def __init__(self, n=5, p=0.5, e_inf = 0, e_sup = 0, graphDict={}):
        """ Constructor
            
            @type n: integer
            @param n: number of nodes
            @type p: real[0,1]
            @param p: probability to have and edge between a pair of nodes 
            @type graphDict: graph            
            @param graphDict: if graphDict is not passed, it will be generated
         """
        self.p = p
        if  e_sup > 0:
            self.n  = n
            self.graphDict = self.genRandomGraph_control(self.n, self.p, e_inf, e_sup)
        elif len(graphDict) < 1:
            self.n = n           
            self.graphDict = self.genRandomGraph(self.n,self.p)
        else:
            self.graphDict = graphDict
            self.n = len(self.graphDict)


   
    def genRandomGraph(self,n,p):
        """ Generate a random graph 
            
            @type n: integer
            @param n: number of nodes
            @type p: real[0,1]
            @param p: probability to have and edge between a pair of nodes
            
            @rtype: graph
            @return: a random graph with probability p
        """
        graph={}
        for i in range(n):
            graph[i] = []
        for i in range(n):
            for j in range(i+1,n):
                #edge i-j
                r = random.random();
                if r <= p:
                    graph[i].append(j)
                #edge j-i
                r = random.random();
                if r <= p:
                    graph[j].append(i)
        return graph    
    
    def genRandomGraph_unbalanced(self,n,p, e_inf, e_sup):
        """ Generate a random graph with a limited number of edges. If the number
            of the edges is too little then the graph will be unbalanced.
            
            @type n: integer
            @param n: number of nodes
            @type p: real[0,1]
            @param p: probability to have and edge between a pair of nodes
            @type e_inf: integer
            @param e_inf: inferior limit of edges
            @type e_sup: integer            
            @param e_sup: superior limit of edges            
            
            @rtype: graph
            @return: a random graph with probability p
        """
        ''' Inizialization''' 
        n_edges = random.randint(e_inf, e_sup)       
        graph={}
        for i in range(n):
            graph[i] = set()
        
        while n_edges > 0:
            for i in range(n):
                for j in range(n):
                    if j not in graph[i] and j != i:
                        r = random.random()
                        if r <= p:
                            graph[i].add(j)
                            n_edges -= 1
                            if n_edges <= 0:
                                return graph
        return graph    

   
    def genRandomGraph_control(self,n,p, e_inf, e_sup):
        """ Generate a random graph with a limited number of edges
            
            @type n: integer
            @param n: number of nodes
            @type p: real[0,1]
            @param p: probability to have and edge between a pair of nodes
            @type e_inf: integer
            @param e_inf: inferior limit of edges
            @type e_sup: integer            
            @param e_sup: superior limit of edges            
            
            @rtype: graph
            @return: a random graph with probability p
        """
        ''' Inizialization''' 
        n_edges = random.randint(e_inf, e_sup)       
        graph={}
        for i in range(n):
            graph[i] = []
        
        ''' Generating graph '''
        while n_edges > 0: # create n_edges edges
            find_pair = False
            while find_pair == False: # generate a valid pair
                v1 = random.randint(0, n-1)
                v2 = random.randint(0, n-1)
                if (v1 != v2) and v2 not in graph[v1]:
                    find_pair = True;                    
            # random graph property
            r = random.random()
            if r <= p:
                graph[v1].append(v2)
                n_edges -= 1
        
        return graph
   
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

    g = {"a" : ["b"],
         "b" : []
    }

    graph = RandomDirectedGraph(graphDict= g)
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
    
    graph = RandomDirectedGraph(7100, 0.01)
    print "edges:"
    print graph.numOfEdges()

