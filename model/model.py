import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._airports=DAO.getAllAirports()
        self._idMapAirports={}
        for a in self._airports:
            self._idMapAirports[a.ID]=a
        self._bestCammino = []
        self._bestScore = 0

    def getCamminoOttimo(self, v0, v1, t):
        #gestisce il punto 2:
        #trova un cammino da v0 a v1 con massimo t tratte e di costo massimo
        self._bestCammino=[]
        self._bestScore=0
        parziale=[v0] #metto già v0 perché è l'aeroporto di partenza
        self._ricorsione(parziale, v1, t)
        return self._bestCammino, self._bestScore

    def _ricorsione(self, parziale, v1, t):
        #verifico se parziale è una soluzione valida
        #condizione di ottimalità: costo ottimo
        if parziale[-1]==v1: #arrivo all'aeroporto di destinazione: soluzione accettabile
            if self._getScore(parziale)>self._bestScore:
                self._bestCammino=copy.deepcopy(parziale)
                self._bestScore=self._getScore(parziale)
        #verifico se ha senso continuare ad aggiungere elementi in parziale, oppure esco
        #condizione di terminazione: lunghezza t (non obbligatorio raggiungerla)
        if len(parziale)==t+1:
            return
        #espando parziale e ripeto la ricorsione
        for n in self._graph.neighbors(parziale[-1]): #i vicini dell'ultimo nodo inserito
            if n not in parziale: #se non l'ho già aggiunto nella soluzione
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop() # BACKTRACKING

    def _getScore(self, parziale):
        sumPesi=0
        for i in range (0, len(parziale)-1):
            sumPesi+=self._graph[parziale[i]][parziale[i+1]]["weight"]
        return sumPesi

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

    def hasPath(self, v0, v1):
        #restituisce True se esiste un cammino tra i due nodi, altrimenti False
        #ci calcoliamo la componente connessa del nostro nodo e verifichiamo se l'altro è presente
        return v1 in nx.node_connected_component(self._graph, v0) #passo il grafo e il nodo di partenza
        # nx.node_connected_components invece ci dà la lista di componenti connesse

    def getPath(self, v0, v1):
        #restituisce un cammino tra v0 e v1
        # MODO 4
        path = nx.dijkstra_path(self._graph, v0, v1, weight=None)  # cammino di dijkstra tra v0 e v1
        #parametro weight inserito per ignorare i pesi degli archi nel calcolo del cammino
        return path
        # MODO 1
        """dictOfPredecessors=dict(nx.bfs_predecessors(self._graph, v0)) #esplorazione breadth-first """
        #cercherà i cammini minimi
        #potremmo fare anche depth first ma il cammino sarebbe più lungo
        #per ogni chiave del dizionario (nodo) il valore è il nodo precedente
        """path=[v1]""" #perché è il nodo di arrivo, quindi l'ultimo del cammino
        """while path[0]!=v0:
            #finché path non inizia con v0, che è il nodo source
            #continuiamo a inserire predecessori del primo nodo presente
            path.insert(0, dictOfPredecessors[path[0]])"""
            # [v0, ... ... , v1]
        # MODO 2
    """ dictOfPredecessors = dict(nx.dfs_predecessors(self._graph, v0))  # esplorazione breadth-first
        path = [v1]  # perché è il nodo di arrivo, quindi l'ultimo del cammino
        while path[0] != v0:
            path.insert(0, dictOfPredecessors[path[0]])
        # MODO 3
        path=nx.shortest_path(v0, v1) #metodo più veloce"""

    def getAllNodes(self):
        nodes = list(self._graph.nodes())
        nodes.sort(key=lambda x:x.IATA_CODE) #ordiniamo gli aeroporti per codice iata
        return nodes