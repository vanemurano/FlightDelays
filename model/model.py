import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.DiGraph() # grafo semplice orientato

    def getAllStates(self):
        return DAO.getAllStates()

    def getEdges(self):
        return DAO.getEdges()

    def creaGrafo(self):
        self._graph.clear()
        self._graph.add_nodes_from(self.getAllStates())
        for a1, a2, peso in self.getEdges():
            if a1 in self._graph.nodes and a2 in self._graph.nodes:
                self._graph.add_edge(a1, a2, weight=peso) # aggiunge l'arco con il peso

    def statiVicini(self, source):
        stati=nx.neighbors(self._graph, source) # lista di nodi direttamente collegati a src
        statiPeso=[] # lista di tuple
        for s in stati:
            tupla=(s, self._graph.get_edge_data(source, s)["weight"])
            # tupla stato raggiunto, peso dell'arco
            statiPeso.append(tupla)
        statiPeso.sort(key=lambda x: x[1], reverse=True)
        return statiPeso

    def getNNodi(self):
        return len(self._graph.nodes)

    def getNArchi(self):
        return len(self._graph.edges)