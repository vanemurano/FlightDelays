import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._airports=DAO.getAllAirports()
        self._idMapAirports={}
        for a in self._airports:
            self._idMapAirports[a.ID]=a

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        #print(f"N nodi:{len(self._graph.nodes)}, n archi:{len(self._graph.edges)}")
        #self.addEdges()
        #print(f"N nodi:{len(self._graph.nodes)}, n archi:{len(self._graph.edges)}")
        self.addEdgesV2()
        #print(f"N nodi:{len(self._graph.nodes)}, n archi:{len(self._graph.edges)}")

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def addEdges(self):
        allTratte=DAO.getAllEdgesV1(self._idMapAirports)
        # queste tratte hanno aeroporti che non sappiamo se sono nodi del grafo,
        # (che avevamo precedentemente filtrato)
        # abbiamo archi sia diretti che inversi
        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                #verifico se entrambi gli aeroporti sono nodi del grafo
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):
                    #controllo se questo arco esiste già nel grafo
                    self._graph[t.aeroportoP][t.aeroportoA]["weight"]+=t.peso
                    # se l'arco esiste già, vado solo a incrementarne il peso
                self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)
                #altrimenti creo il nuovo arco

    def addEdgesV2(self):
        allTratte=DAO.getAllEdgesV2(self._idMapAirports)
        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)

    def getViciniOrdinati(self, source):
        #vuole trovare gli aeroporti raggiungibili da un nodo di partenza
        #ordinati per peso dell'arco che li collega
        vicini=self._graph.neighbors(source)
        viciniT=[]
        for v in vicini:
            viciniT.append((v, self._graph[source][v]["weight"]))
        viciniT.sort(key=lambda x:x[1], reverse=True)
        return viciniT

    def getAllNodes(self):
        nodes = list(self._graph.nodes())
        nodes.sort(key=lambda x:x.IATA_CODE) #ordiniamo gli aeroporti per codice iata
        return nodes