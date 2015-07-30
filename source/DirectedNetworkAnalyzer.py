#----------------------------------------------------------------------
# DirectedNetworkAnalyzer
#
# Contains the class which implements methods for analyzing graphs
# 
# Author: Emanuele Pesce
#----------------------------------------------------------------------
import NaiveDirectedGraph as ng
import sys

class DirectedNetworkAnalyzer(ng.NaiveDirectedGraph):
    """ Director Network analyzer class which contains methods for analyzing a 
        graph.
        Extends NaiveDirectedGraph.
    """

    '''========= constructor ========='''
    def __init__(self, filename = "", graphDict={}):
        """ Constructor
                    
            @type filename: string
            @param filename: name of the file
            @type graphDict: graph dictionary
            @param graphDict: graph 
        """
        if len(filename) > 0:
            self.graphDict = self.readGraph(filename)
        else:
            self.graphDict = graphDict
     
    def getGraph(self):
      """ Return the graph dictionary 

          @rtype: graph
          @return: graph
      """
      return self.graphDict
  
  
    def diameter(self, graph={}):
      """ Return the largest shortest path and the number of nodes and edges of the largest component
      """
      if len(graph)<1:
        graph = self.graph
      nodes = 0
      edges = 0
      diameter = 0
      
      for i in graph.keys():
        ''' inizialize variables in each iteration'''
        visited = []
        max_distance = 0
        tmp_edge = 0
        queue = [i]
        distance = dict()
        for j in graph.keys():
          distance[j] = -1
        distance[i] = 0
        ''' BFS for counting the number of edges and nodes and for calculating diameter '''
        while queue != []:
          s = queue.pop(0)
          visited.append(s)
          tmp_edge += len(graph[s])
          for j in graph[s]:
            if distance[j] < 0: #not visited
              queue.append(j)
              distance[j] = distance[s] + 1
              if distance[j] > max_distance:
                max_distance = distance[j]
        ''' save only information about the largest component '''
        if len(visited) > nodes:
          nodes = len(visited)
          edges = tmp_edge/2
        '''  save max diameter '''
        if max_distance > diameter:
          diameter = max_distance
          
      return nodes,edges,diameter


    def counterUtility(self, graph ={}):
      """  Return the number of edges, the number of triangles, length-2 paths and the average clustering
      """
      if len(graph)<1:
        graph = self.graph
      edges=0
      triangles = 0
      paths = 0
      total=0
      
      for i in graph.keys():
        edges += len(graph[i])
        neigh_pairs = (len(graph[i])*(len(graph[i])-1))/2
        closed_pairs = 0
        for j in graph[i]:
          for k in graph[j]:
            if k != i:
              paths += 1
            if k in graph[i]:
              closed_pairs += 1
        triangles += closed_pairs
        if neigh_pairs > 0:
          total += float(closed_pairs)/(2*neigh_pairs)
          
      return int(edges/2), int(triangles/6), int(paths/2), float(total)/len(graph)
    
    ''' ============== Generic analysis methods ============== '''
    def averageClustering(self):
        """
            Return the average clustering of the graph           
            (Clustering index of a node is the number of his neghbors that are
            connected among themselves)
        """
        total = 0
        for i in self.graphDict:
            ''' calculate the number of the pairs of neighbors of node i which are adiacents '''
            neighs = len(self.graphDict[i])
            pairsNeigh = ( neighs * (neighs-1) )/2 # all pairs
            ''' check how many nehgbors of node i have a connection '''
            triangles = 0
            for j in self.graphDict[i]:
                for k in self.graphDict[i]:
                    if k in self.graphDict[j]:
                        triangles += 1
                if pairsNeigh > 0:
                    total += float(triangles)/pairsNeigh
            
        return float(total)/self.numOfVertices()
    
    
    def averageClusteringUndirected(self):
        """
            Return the average clustering of the graph           
            (Clustering index of a node is the number of his neghbors that are
            connected among themselves)
        """
        graph = self.getGraph()
        dirGraph = {}
        
        for i in graph.keys():
            dirGraph[i] = set()
        for i in graph.keys():
            for j in graph[i]:
                dirGraph[i].add(j)
                dirGraph[j].add(i)
                        
        total = 0       
        for i in dirGraph:
            ''' calculate the number of the pairs of neighbors of node i 
                which are adiacents
            '''        
            neighs = len(dirGraph[i])
            pairsNeigh = ( neighs * (neighs-1) )/2 # all pairs
            ''' check how many nehgbors of node i have a connection '''
            triangles = 0
            for j in dirGraph[i]:
                for k in dirGraph[i]:
                    if k in dirGraph[j]:
                        triangles += 1
            if pairsNeigh > 0:
                total += float(triangles)/(2*pairsNeigh)
        return float(total)/len(dirGraph)  
    
    ''' ============== Centralities measures ============== '''
    def betweenness(self):
      """ Compute betweenness centrality for each node of the graph
          
          Girman-Newman algorithm 
      """
      ''' inizialize graph '''
      graph = self.getGraph()
      
      ''' betweenness of each node is 0  '''
      betweenness = {}
      for i in graph.keys():
        betweenness[i] = 0
      
      for s in graph.keys():
        ''' Initialization for any root '''
        #BFS tree
        tree = []
        
        #queue for bfs
        queue = [s]
        
        #parents
        parents = {}
        for i in graph.keys():
          parents[i] = []
        
        #number of parents for calculate the amount of flow
        spnum = {}
        for i in graph.keys():
          spnum[i] = 0
          
        spnum[s] = 1
        
        #distances from s
        distance = {}
        for i in graph.keys():
          distance[i] = -1
          
        distance[s] = 0
        
        #flow
        flow = {}
        for i in graph.keys():
          flow[i] = 0
          
        ''' BFS ''' 
        while queue != []:
          c = queue.pop(0)
          tree.append(c)
          for i in graph[c]:
            if distance[i] == -1:
              queue.append(i)
              distance[i] = distance[c] + 1
            if distance[i] == distance[c] + 1:
              spnum[i] += spnum[c]
              parents[i].append(c)
            
        ''' BOTTOM-UP PHASE ''' 
        while tree != []:
          c = tree.pop()
          for i in parents[c]:
            flow[i] += (float(spnum[i])/spnum[c])*(1 + flow[c])
          if c != s:
            betweenness[c] += flow[c]
    
      return betweenness


    def eigenvector(self, confidence=0.01):
      """ Compute eigenvector centrality for each node of the graph
          
          Method: left dominant eigenvector
          
          @type confidence: number
          @param  confidence: trueshold for convergence
      """
      graph = self.getGraph()
      
      nodes = graph.keys()
      done = 0
      
      ''' Inizialization '''
      eigen = {}
      for i in nodes:
        eigen[i] = 1/float(len(nodes))
      
      # first compute this temporary value for eigenvector centrality. The real value consists of a normalization of this temporary value
      tmp = {}
      ''' Repeat the process until the centrality vector does not change anymore'''
      while not done: 
        max_tmp = 0
        for i in nodes:
          tmp[i] = eigen[i] # Even if this is not standard, this is necessary in order that the algorithm converge for any graph
          for j in graph[i]:
            tmp[i] += eigen[j]        
          if tmp[i] > max_tmp:
            max_tmp = tmp[i]
            
        diff = 0
        for i in nodes:
          diff += abs(eigen[i]-float(tmp[i])/float(max_tmp)) # Distance between old and new centrality vector
          eigen[i] = float(tmp[i])/max_tmp
        
        if diff < confidence:
          done = 1
          
      return eigen


    def katz(self, alpha = 0.125, confidence = 1.0e-6, max_iter = 1000):
        """ Computes katz centrality
            K(u) = sum_(n in neighbors(u)) ( k(n)+1)            
            
            @type alpha: real
            @param alpha: attenuation factor
            @type confidence: real
            @param  confidence: trueshold for convergence
            @type max_iter: integer
            @param max_iter: max number of iterations
            
            Note: this centrality is implemented considering outgoing edges.
        """
        katz = dict()
        tmp = dict()
        graph = graph = self.getGraph() 
        max_value = sys.float_info.min
        
        ''' inizialization '''
        for i in graph.keys():
            katz[i] = 0
        
        ''' computes katz centrality '''
        while max_iter > 0:
            for v in graph.keys():
                tmp[v] = 0
                for nbr in graph[v]:
                    tmp[v] = tmp[v] + katz[nbr] + 1
                tmp[v] = alpha*tmp[v]
                if tmp[v] > max_value:
                    max_value = tmp[v]
                
            diff = 0
            for v in katz.keys():
      		    diff = diff + abs(katz[v] - float(tmp[v])/max_value)	
      		    katz[v] = float(tmp[v])/max_value
            if diff < confidence:
      		    return katz
            max_iter -= 1
        return katz


    def katzTrue(self, alpha = 0.125, confidence = 1.0e-6, max_iter = 1000):
        """ Computes katz centrality
            K(u) = sum_(n in neighbors(u)) ( k(n)+1)            
            
            @type alpha: real
            @param alpha: attenuation factor
            @type confidence: real
            @param  confidence: trueshold for convergence
            @type max_iter: integer
            @param max_iter: max number of iterations
      """
        graph = self.getGraph()        
        nodes = graph.keys()
        
        ''' Inizialization '''
        katz = {}
        last = {}
        for i in nodes:
            katz[i] = 1
        
        ''' computes katz centrality '''
        done = 0
        mi = 0
        while mi <= max_iter or done == 0:
            last = katz
            max_value = 0
            for i in nodes:
                katz[i] = 0
            ''' computes new katz centralities'''
            for v in nodes: #for each node v
                for nbr in graph[v]: #for each neighbour of v
                    katz[nbr] += last[v] + 1 # node v spreads his centrality 
                                             # to his neighbors
            ''' attenuation and normalization'''
            for i in nodes:
                katz[i] = katz[i]*alpha
                if katz[i] > max_value:
                    max_value = katz[i]
            for i in nodes:
                katz[i] = float(katz[i])/max_value
            ''' check confidence '''
            diff = 0
            for v in katz.keys():
                diff += abs(katz[v]-last[v])
            if diff < confidence:
                done = 1
            mi += 1

        # return 
        return katz
        
        
    def topCenters(self, k=1, centrality = "e", confidence = 0.01, alpha=0.125,
        max_iter=1000):
      """ Return the k nodes with highest centrality 
          
          @type k: integer
          @type centrality: char
          @param centrality: centrality measure to select. 
                             centrality values available:
                             'b': betweenness
                             'e': left dominant eigenvector
                             'k': katz centrality
          @type confidence: real
          @param confidence: confidence value
          
      """
      if centrality == "b":
          centers = self.betweenness()
      elif centrality == "e":
          centers = self.eigenvector(float(confidence))
      elif centrality == "k":
          centers = self.katz(alpha = alpha, confidence = confidence, max_iter = max_iter)
            
      top = []
      top_values = []
      for i in centers.keys():
        added = 0
        for j in range(min(len(top),int(k))):
          if centers[top[j]] < centers[i]:
            top.insert(j,i)
            added = 1
            break
        if added == 0:
          top.append(i)
        if len(top) > int(k):
          top.pop()
      for i in range(len(top)):
        top_values.append(centers[top[i]])
      return top, top_values


   
if __name__ == "__main__":
 
    ''' ====== TEST IMPORT ===== '''
    an = DirectedNetworkAnalyzer(filename = "./../data/Wiki_Vote.txt")
#    an = DirectedNetworkAnalyzer(filename = "./../data/facebook/facebook_combined.txt")
    print "Number of edges"
    print an.numOfEdges()
    print "Number of vertices"    
    print an.numOfVertices()   
    
    print "Top centers eigenvector"
    print an.topCenters(15, 'e')
    print "Top centers katz"
    print an.topCenters(15, 'k', confidence=1.0e-6)
    print "Top centers betweenneess"
    print an.topCenters(15, 'b')

    print "Average clustering"
    print an.averageClusteringUndirected()
    