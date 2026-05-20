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

    def handleTestConnessione(self, e):
        if self._choicePartenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione! Per usare questo metodo occorre selezionare un aeroporto di partenza", color="red")
            )
            self._view.update_page()
            return
        if self._choiceArrivo is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione! Per usare questo metodo occorre selezionare un aeroporto di arrivo", color="red")
            )
            self._view.update_page()
            return
        if not self._model.hasPath(self._choicePartenza, self._choiceArrivo):
            # se non esiste un qualsiasi cammino tra questi due nodi
            self._view.txt_result.controls.append(
                ft.Text(f"Non ho trovato nessun cammino tra {self._choicePartenza}"
                        f"e {self._choiceArrivo}", color="orange"))
            self._view.update_page()
            return
        path=self._model.getPath(self._choicePartenza, self._choiceArrivo)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ho trovato un cammino tra {self._choicePartenza}"
                        f"e {self._choiceArrivo}\n"
                    f"Di seguito i nodi che lo compongono:", color="green"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.update_page()

    def handleCerca(self, e):
        t=self._view._txtInNTratteMax.value
        try:
            tInt=int(t)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Il valore di t deve essere un numero intero!", color="red")
            )
            return
        path, score=self._model.getCamminoOttimo(self._choicePartenza, self._choiceArrivo, tInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino tra {self._choicePartenza} e {self._choiceArrivo} trovato", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Il cammino ha uno score complessivo pari a {score} e contiene i seguenti nodi:", color="green")
        )
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p, color="green"))
        self._view.update_page()

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

