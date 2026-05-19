import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choicePartenza=None
        self._choiceArrivo=None

    def handleAnalizza(self, e):
        cMintxt=self._view._txtInCMin.value
        if cMintxt=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numerico per numero minimo compagnie",
                        color="red"))
            self._view.update_page()
            return
        try:
            cMin=int(cMintxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore intero per numero minimo compagnie",
                        color="red"))
            self._view.update_page()
            return
        # dopo aver passato questi controlli, cMin è un intero, ma può anche essere 0 o negativo
        if cMin<=0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore intero positivo",
                        color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(cMin)
        nNodes, nEdges=self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato!",
                    color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {nNodes} nodi e {nEdges} archi",
                    color="green"))

        allNodes=self._model.getAllNodes() #dopo aver creato il grafo
        #recupero tutti i nodi e li inserisco nel dd
        self._fillDropdown(allNodes)

        self._view.update_page()

    def handleConnessi(self, e):
        if self._choicePartenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione! Per usare questo metodo occorre selezionare un aeroporto di partenza", color="red")
            )
            self._view.update_page()
            return
        viciniT=self._model.getViciniOrdinati(self._choicePartenza)
        self._view.txt_result.controls.clear()
        for v in viciniT:
            self._view.txt_result.controls.append(
                ft.Text(f"{v[0]} - peso: {v[1]}")
            )
            self._view.update_page()

    def handleCerca(self, e):
        pass

    def handleTestConnessione(self, e):
        pass

    def _fillDropdown(self, allNodes):
        for n in allNodes:
            self._view._ddAeroportoPartenza.options.append(
                ft.dropdown.Option(data=n, #l'oggetto selezionato
                                   key=n.IATA_CODE, #la stringa visualizzata
                                   on_click=self._choiceDDPartenza))
            self._view._ddAeroportoArrivo.options.append(
                ft.dropdown.Option(data=n,  # l'oggetto selezionato
                                   key=n.IATA_CODE,  # la stringa visualizzata
                                   on_click=self._choiceDDArrivo))

    def _choiceDDPartenza(self, e):
        self._choicePartenza=e.control.data #salva la scelta input in una variabile
        print(f"Hai selezionato come aeroporto di partenza {self._choicePartenza}")

    def _choiceDDArrivo(self, e):
        self._choiceArrivo=e.control.data #salva la scelta input in una variabile
        print(f"Hai selezionato come aeroporto di arrivo {self._choiceArrivo}")

