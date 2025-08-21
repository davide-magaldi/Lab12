from datetime import datetime

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listCountry = []

    def fillDD(self):
        self._listCountry = DAO.getAllCountries()
        for n in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(n))

    def handle_graph(self, e):
        year = self._view.ddyear.value
        if year is None:
            self._view.create_alert("Selezionare un anno!")
            return
        country = self._view.ddcountry.value
        if country is None:
            self._view.create_alert("Selezionare una Nazione!")
            return
        self._model.buildGraph(year, country)
        self._view.txtOut2.controls.clear()
        self._view.txtOut3.controls.clear()
        self._view.btn_volume.disabled = False
        self._view.btn_path.disabled = False
        nnodes, nedges = self._model.getInfoGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato contiene {nnodes} nodi e {nedges} archi"))
        self._view.update_page()

    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        volumes = self._model.findVolumes()
        for t in volumes:
            self._view.txtOut2.controls.append(ft.Text(f"{t[0].Retailer_name} -->{t[1]}"))
        self._view.update_page()

    def handle_path(self, e):
        n = self._view.txtN.value
        if n is None or n == "":
            self._view.create_alert("Inserire un numero di archi")
            return
        try:
            n = int(n)
            if n < 2:
                self._view.create_alert("I numero di archi selezionato deve essere almeno 2!")
                return
        except ValueError:
            self._view.create_alert("Inserire un valore numerico")
        time = datetime.now()
        path, score = self._model.getBestPath(n)
        self._view.txtOut3.controls.clear()
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {score}"))
        self._view.txtOut3.controls.append(ft.Text("Percorso trovato con i seguenti archi:"))
        for i in range(0, len(path)-1):
            self._view.txtOut3.controls.append(ft.Text(f"{path[i].Retailer_name} --> {path[i+1].Retailer_name}: {self._model._graph.get_edge_data(path[i],path[i+1])['weight']}"))
        self._view.txtOut3.controls.append(ft.Text(f"Tempo impiegato: {datetime.now()-time}"))
        self._view.update_page()

