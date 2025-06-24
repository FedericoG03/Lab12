import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestPath = None
        self._bestScore = 0

    def getCountry(self):
        return DAO.getAllCountry()

    def buildGraph(self,country,year):
        retailer = DAO.getRetailersCountry(country)
        for i in retailer:
            self._idMap[i.Retailer_code] = i
        self._graph.clear()
        self._graph.add_nodes_from(retailer)
        for e in DAO.getEdges(country,year, self._idMap):
            self._graph.add_edge(e[0],e[1],weight=e[2])

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getVolume(self):
        volumi = {}
        for e in self._graph.edges():
            if e[0].Retailer_name not in volumi.keys():
                volumi[e[0].Retailer_name] = self._graph[e[0]][e[1]]['weight']
            else:
                volumi[e[0].Retailer_name] += self._graph[e[0]][e[1]]['weight']
            if e[1].Retailer_name not in volumi.keys():
                volumi[e[1].Retailer_name] = self._graph[e[0]][e[1]]['weight']
            else:
                volumi[e[1].Retailer_name] += self._graph[e[0]][e[1]]['weight']
        return volumi

    def getPath(self,lung):
        parziale = []

        for n in self._graph.nodes():
            parziale.append(n)
            self._ricorsione(parziale,lung)
            parziale.pop()

        return self._bestPath,self._bestScore


    def _ricorsione(self,parziale,lung):
        if len(parziale) == (lung+1) and parziale[0] == parziale[-1]:
            if self.calcolaPeso(parziale) > self._bestScore:
                self._bestPath = copy.deepcopy(parziale)
                self._bestScore = self.calcolaPeso(parziale)
        if len(parziale) < lung:
            for i in self._graph.neighbors(parziale[-1]):
                if i not in parziale:
                    parziale.append(i)
                    self._ricorsione(parziale, lung)
                    parziale.pop()

        if len(parziale) == lung:
            if parziale[0] in self._graph.neighbors(parziale[-1]):
                parziale.append(parziale[0])
                self._ricorsione(parziale, lung)
                parziale.pop()

    def calcolaPeso(self,parziale):
        peso = 0
        for e in range(len(parziale)-1):
            if self._graph.has_edge(parziale[e],parziale[e+1]):
                peso += self._graph[parziale[e]][parziale[e+1]]['weight']
        return peso


