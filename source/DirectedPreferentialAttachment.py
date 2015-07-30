#----------------------------------------------------------------------
# DirectedPrefentialAttachment
#
# Contains the class which implements a directed prefential attachment graph
# 
# Author: Emanuele Pesce
#----------------------------------------------------------------------
import NaiveDirectedGraph as dg
import random
import numpy as np

class DirectedPreferentialAttachment(dg.NaiveDirectedGraph):
    """ Directed Prefential Attachment Graph class. Extends Naive Directed Graph class.
    In a Prefential Attachment Graph when a node j is created, its out-links are produced in the following way:
    - with a probability p, choose a node i uniformly at random and creates an edge from j to i
    - with a probability 1-p, choose a node l with a proability that is proportional to the l's current in-degree and creates an edge from j to l.
    
    This is the idea behind the 'Rich get Richer' phenomen
    """
    
    '''========= constructor ========='''    
    def __init__(self, n, d, p, e_inf = 0, e_sup = 0):
        """ Constructor
            
            @type n: integer
            @param n: number of nodes
            @type d: integer
            @param d: max out-degree
            @type p: real[0,1]
            @param p: probability to have and edge between a pair of nodes             
         """
        self.n = n
        self.d = d
        self.p = p
        if e_sup > 0:
            self.graphDict = self.genPrefAttachmentGraph_controlOrder(self.n,self.d,self.p, e_inf, e_sup)
        else:
            self.graphDict = self.genPrefAttachmentGraph(self.n,self.d,self.p)

   
    def genPrefAttachmentGraph(self,n,d,p):
        """ Generate a preferential attachment graph.
            
            @type n: integer
            @param n: number of nodes
            @type d: integer
            @param d: max out-degree
            @type p: real[0,1]
            @param p: probability to have and edge between a pair of nodes
            
            @rtype: graph
            @return: a preferential attachment graph
        """
        ''' inizialization '''
        L = [] #each element is a vertex of the graph, the number of the times an element appear in L is the number of indegree(element)
        graph={}
        for i in range(n):
            graph[i] = set()
        ''' create edges for each node according with the prefential attachment rule '''
        for i in range(n):
            for j in range(d):
                #with probability p create an edge outgoing from i
                r = np.random.uniform()
                if p > r:
                    vToAdd =  random.randint(0,n-1)
                    if vToAdd != i:
                        graph[i].add(vToAdd) 
                        L.append(vToAdd)                      
                # with probability 1-p create an edge to a popular node
                # the more indegree(vertex) is high, the more vertex is popular
                elif len(L) > 0:                      
                    vToAdd =  random.randint(0,len(L)-1) # probability proportional to a popularity of a node
                    graph[i].add(L[vToAdd])
                    L.append(L[vToAdd])
        return graph

    def genPrefAttachmentGraph_controlOrder(self,n,d,p, e_inf, e_sup):
        """ Generate a preferential attachment graph with a limited number of 
            edges.
            
            @type n: integer
            @param n: number of nodes
            @type d: integer
            @param d: max out-degree
            @type p: real[0,1]
            @param p: probability to have and edge between a pair of nodes
            @type e_inf: integer
            @param e_inf: inferior limit of edges
            @type e_sup: integer            
            @param e_sup: superior limit of edges 
            
            @rtype: graph
            @return: a preferential attachment graph
        """
        ''' inizialization '''
        L = [] #each element is a vertex of the graph, the number of the times an element appear in L is the number of indegree(element)
        graph={}
        n_edges = random.randint(e_inf, e_sup)
        print n_edges
        ''' create edges for each node according with the prefential attachment rule '''
        graph[1] = set()
        for i in range(2, n):
            graph[i] = set()
            for j in range(d):
                #with probability p create an edge outgoing from i
                r = np.random.uniform()
                if r <= p:
                    # pick a node already created
                    pn = random.randint(1,i-1)
                    if pn not in graph[i]:
                        graph[i].add(pn)
                        L.append(pn)
                        n_edges -= 1
                # with probability 1 - p create an edge to a popular node
                elif (len(L) > 0):
                    k = random.randint(0,len(L)-1)
                    if L[k] != i and L[k] not in graph[i]:
                        graph[i].add(L[k])
                        L.append(L[k])
                        n_edges -= 1
                if n_edges <= 0:
                    return graph
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

    graph = DirectedPreferentialAttachment(9, 3, 0.5)
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
    
    graph = DirectedPreferentialAttachment(10, 3, 0.5, 10, 20)
    print graph.numOfEdges()