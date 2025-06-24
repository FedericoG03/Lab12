import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = list(range(2015,2019))
        self._listCountry = self._model.getCountry()

    def fillDD(self):
        for c in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))
        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(y))

    def handle_graph(self, e):
        county = self._view.ddcountry.value
        if county == None or county == '':
            self._view.create_alert("Scegliere una nazione")
            return
        year = self._view.ddyear.value
        if year == None or year == "":
            self._view.create_alert("Scegliere una anno")
            return
        self._view.update_page()

        self._model.buildGraph(county,year)
        vertici,archi = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {vertici}\nNumero di archi: {archi}"))
        self._view.update_page()


    def handle_volume(self, e):
        volumi = self._model.getVolume()
        self._view.txtOut2.controls.clear()
        for v in sorted(volumi.items(),key=lambda x:x[1],reverse=True):
            self._view.txtOut2.controls.append(ft.Text(f"{v[0]} : {v[1]}"))
        self._view.update_page()

    def handle_path(self, e):
        n = int(self._view.txtN.value)
        if n < 2:
            self._view.create_alert("Inserire un valore maggiore di 2")
            return
        path,score = self._model.getPath(n)
        self._view.txtOut3.controls.clear()
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {score}"))
        for p in range(len(path)-1):
            self._view.txtOut3.controls.append(ft.Text(f"{path[p].Retailer_name} --> {path[p+1].Retailer_name} : {self._model._graph[path[p]][path[p+1]]['weight']}"))
        self._view.update_page()


