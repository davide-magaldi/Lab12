import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self.bestSol = []
        self.bestScore = 0

    def buildGraph(self, year, country):
        self._graph.clear()
        nodes = DAO.getNodes(country)
        for n in nodes:
            self._idMap[n.Retailer_code] = n
        self._graph.add_nodes_from(nodes)
        edges = DAO.getEdges(year, country)
        for e in edges:
            self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=e[2])

    def getInfoGraph(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def findVolumes(self):
        volumes = {}
        for n in self._graph.nodes:
            vol = 0
            neighbors = self._graph.neighbors(n)
            for ne in neighbors:
                vol += self._graph.get_edge_data(n, ne)['weight']
            volumes[n] = vol
        lista = list(volumes.items())
        lista.sort(key=lambda item: item[1], reverse=True)
        return lista

    def getBestPath(self, n):
        self.bestSol = []
        self.bestScore = 0
        parziale = []
        max_weight = max(d['weight'] for u, v, d in self._graph.edges(data=True))
        for node in self._graph.nodes:
            parziale = [node]
            self.findNext(n, parziale, max_weight)
        return self.bestSol, self.bestScore

    def findNext(self, n, parziale, max_weight):
        if len(parziale) == n:
            neighbors_last = self._graph.neighbors(parziale[-1])
            if parziale[0] in neighbors_last:
                parziale.append(parziale[0])
                score = self.getScore(parziale)
                if score > self.bestScore:
                    self.bestSol = copy.deepcopy(parziale)
                    self.bestScore = score
                parziale.pop()
            return
        upper_bound = self.getScore(parziale) + (n - len(parziale) +1) * max_weight
        if upper_bound <= self.bestScore:
            return
        else:
            for ne in self._graph.neighbors(parziale[-1]):
                if ne not in parziale:
                    parziale.append(ne)
                    self.findNext(n, parziale, max_weight)
                    parziale.pop()

    def getScore(self, sol):
        score = 0
        for i in range(0, len(sol)-1):
            score += self._graph.get_edge_data(sol[i], sol[i+1])['weight']
        return score


    def getBestPath2(self, n):
        self.bestSol = []
        self.bestScore = 0

        # Calcola il peso massimo tra tutti gli archi (serve per pruning)
        self.max_weight = max(
            d['weight'] for u, v, d in self._graph.edges(data=True)
        )

        nodes = sorted(self._graph.nodes, key=lambda x: x.Retailer_code)

        for node in nodes:
            parziale = [node]
            parziale_set = {node}
            self.findNext2(n, parziale, parziale_set, node)

        return self.bestSol, self.bestScore

    def findNext2(self, n, parziale, parziale_set, start_node):
        if len(parziale) == n:
            # Controlla se può formare un ciclo
            if start_node in self._graph.neighbors(parziale[-1]):
                parziale.append(start_node)  # chiude il ciclo
                score = self.getScore2(parziale)
                if score > self.bestScore:
                    self.bestSol = copy.deepcopy(parziale)  # copia sicura
                    self.bestScore = score
                parziale.pop()  # rimuove la chiusura
            return

        # Stima pruning: score attuale + massimo ottenibile nei passi restanti
        potential_score = self.getScore2(parziale) + (n - len(parziale) +1) * self.max_weight
        if potential_score <= self.bestScore:
            return

        for ne in self._graph.neighbors(parziale[-1]):
            if ne not in parziale_set:
                parziale.append(ne)
                parziale_set.add(ne)
                self.findNext2(n, parziale, parziale_set, start_node)
                parziale.pop()
                parziale_set.remove(ne)

    def getScore2(self, sol):
        score = 0
        for i in range(0, len(sol) - 1):
            score += self._graph.get_edge_data(sol[i], sol[i + 1])['weight']
        return score



