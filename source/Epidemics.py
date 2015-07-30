#----------------------------------------------------------------------
# DirectedEpidemics
#
# Contains the class which implements methods which simulates epidemics/diffusion
# spreading
# 
# Author: Emanuele Pesce
#----------------------------------------------------------------------
import numpy as np
import DirectedNetworkAnalyzer as da # for testing
class Epidemics():
    """ Epidemics class which contains methods for simulating epidemics spreading
    """

    '''========= constructor ========='''
    def __init__(self, graphDict={}):
        """ Constructor
                    
            @type filename: string
            @param filename: name of the file
            @type graphDict: graph dictionary
            @param graphDict: graph 
        """
        self.graph = graphDict
        
    
    def linearThreshold(self, seeds=set(), toPrint  = 0):
        
        graph = self.graph
        infected = set()

            
        ''' Inizialization ''' 
        #set threshold
        t = {}
        for n in graph.keys():
            t[n] = np.random.uniform()
        
        # add seeds in infected
        if len(seeds) > 0:
            for seed in seeds:
                infected.add(seed)
               
        ''' Epidemics spreading '''
        toSpread = True
        while toSpread == True:
            if toPrint == 1:
                print len(infected)
            ''' round of spreading''' 
            toInfect = set()
            for n in graph.keys():
                if n not in infected:
                    # calculates fraction of infected neighbors
                    f = 0
                    if len(graph[n]) > 0:
                        for nv in graph[n]:
                            if nv in infected:
                                f += 1
                        f = f/float(len(graph[n]))
                        # add n to toInfect eventually
                        if f > t[n]:
                            toInfect.add(n)
            ''' check convergence  '''
            if len(toInfect) > 0: # add infected node to infected set
                infected = infected.union(toInfect)
            else: # there no more nodes to infect
                toSpread = False
            
        #return 
        return infected
     
 

   
if __name__ == "__main__":
  
    ''' ====== TEST ===== '''
    an = da.DirectedNetworkAnalyzer(filename = "./../data/Wiki_Vote.txt")
    
    epi = Epidemics(an.getGraph())
    sv = an.topCenters(centrality='k', k=100)
    sn = sv[0]
    
    infected = epi.linearThreshold(seeds = sn, toPrint = 1)
