import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        self._model.creaGrafo()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato!\n"
                    f"Composto da {self._model.getNNodi()} nodi e {self._model.getNArchi()} archi")
        )
        self._view.update_page()

    def handleVisualizzaVelivoli(self, e):
        self._view.txt_result.controls.clear()
        if self._view._ddStati.value is None:
            self._view.txt_result.controls.append(
                ft.Text(f"Selezionare uno stato di partenza!", color="red")
            )
            self._view.update_page()
            return
        if self._model.getNNodi()==0:
            self._view.txt_result.controls.append(
                ft.Text(f"Creare prima il grafo!", color="red")
            )
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Elenco stati direttamente collegati a {self._view._ddStati.value}", color="red")
        )
        listaStati=self._model.statiVicini(self._view._ddStati.value)
        for s, peso in listaStati:
            self._view.txt_result.controls.append(
                ft.Text(f"{s}: {peso} velivoli"))
        self._view.update_page()

    def handleCerca(self, e):
        pass

    def fillDDStato(self):
        stati=self._model.getAllStates()
        statiOpt=list(map(lambda x:ft.dropdown.Option(x), stati))
        self._view._ddStati.options=statiOpt