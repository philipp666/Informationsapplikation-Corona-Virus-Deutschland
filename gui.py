from PyQt5 import QtWidgets as QW
from PyQt5 import uic, QtCore, QtGui
import corona as co
import sys
import requests
import json
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureC
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from numpy import arange


service_ulr = "https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.geojson"
r = requests.get(service_ulr)
packages_json = r.json()

with open("Data_RKI", "w") as Data_RKI:
    json.dump(packages_json, Data_RKI, ensure_ascii=False, indent=4)

with open("Data_RKI", "r") as Data_RKI:
    packages_json = json.load(Data_RKI)


class PlotCanvas(FigureC):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.data = co.Data(packages_json)
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor("#343434")
        self.axes = fig.add_subplot(111)
        FigureC.__init__(self, fig)
        self.setParent(parent)
        FigureC.setSizePolicy(self, QW.QSizePolicy.Expanding,
                              QW.QSizePolicy.Expanding)
        FigureC.updateGeometry(self)
        self.setWindowIcon(QtGui.QIcon('corona.png'))
        self.plot1()

    def plot1(self):
        female, male = self.data.sex_age_death()
        ticks = female.keys()
        x = arange(len(ticks))
        ax = self.figure.add_subplot(111)
        ax.bar(x - 0.2, female.values(), width=0.4, label="weiblich")
        ax.bar(x + 0.2, male.values(), width=0.4, label="männlich")
        ax.set_xticks(x)
        ax.set_xticklabels(female.keys())
        ax.set_xlabel("Altersgruppe")
        ax.set_facecolor("#343434")
        ax.xaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='y', colors='white')
        l = ax.legend(facecolor="#343434")
        for text in l.get_texts():
            text.set_color("white")
        plt.tight_layout()
        self.draw()


class MainWindow(QW.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui.ui", self)
        self.data = co.Data(packages_json)
        self.setWindowIcon(QtGui.QIcon("corona.png"))
        self.display_bund_info()
        self.scroll_bundesland()
        self.scroll_stadt()
        self.line_edit()
        self.plot = PlotCanvas(self, width=5, height=5)
        self.hintergrund_grid.setWidget(4, QW.QFormLayout.LabelRole, self.plot)
        self.show()

    """displays information of cov19 from republic"""
    def display_bund_info(self):
        death_total = self.data.total_death_number()
        recov_total = self.data.total_recov_number()
        infec_total = self.data.total_infections_number()
        table = self.gesamt_data
        table.setColumnCount(2)
        table.setRowCount(3)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setItem(0, 0, QW.QTableWidgetItem("Todeszahl"))
        table.setItem(1, 0, QW.QTableWidgetItem("Anzahl der Genesenen"))
        table.setItem(2, 0, QW.QTableWidgetItem("Anzahl der Infizierten"))
        table.setItem(0, 1, QW.QTableWidgetItem(str(death_total)))
        table.setItem(1, 1, QW.QTableWidgetItem(str(recov_total)))
        table.setItem(2, 1, QW.QTableWidgetItem(str(infec_total)))
        table.resizeColumnsToContents()
        table.setEditTriggers(QW.QTreeView.NoEditTriggers)

    """you can choose your federal state from list"""
    def scroll_bundesland(self):
        choose = self.bundesland_wahl
        choose.addItems(self.data.list_of_fed)
        choose.itemClicked.connect(self.bundesland_info)

    """you can choose your county from list"""
    def scroll_stadt(self):
        choose = self.stadt_wahl
        choose.addItems(self.data.list_of_county)
        choose.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        choose.itemClicked.connect(self.stadt_info)

    """Allows search for specific county"""
    def line_edit(self):
        county_input = self.county_input
        county_input.setPlaceholderText("SK/LK Regensburg")
        completer = QW.QCompleter(self.data.list_of_county)
        county_input.setCompleter(completer)
        county_input.returnPressed.connect(self.stadt_info_spezifisch)

    """returns information of whole federalstate"""
    def bundesland_info(self, bundesland):
        bundesland = str(bundesland.text())
        death_total = self.data.death_number_fed(bundesland)
        recov_total = self.data.recov_number_fed(bundesland)
        infec_total = self.data.infections_number_fed(bundesland)
        table = self.data_bundesland
        table.setColumnCount(2)
        table.setRowCount(3)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setItem(0, 0, QW.QTableWidgetItem("Todeszahl"))
        table.setItem(1, 0, QW.QTableWidgetItem("Anzahl der Genesenen"))
        table.setItem(2, 0, QW.QTableWidgetItem("Anzahl der Infizierten"))
        table.setItem(0, 1, QW.QTableWidgetItem(str(death_total)))
        table.setItem(1, 1, QW.QTableWidgetItem(str(recov_total)))
        table.setItem(2, 1, QW.QTableWidgetItem(str(infec_total)))
        table.resizeColumnsToContents()
        table.setEditTriggers(QW.QTreeView.NoEditTriggers)

    """returns information of specific county from list"""
    def stadt_info(self, stadt):
        stadt = str(stadt.text())
        death_total = self.data.death_number_county(stadt)
        recov_total = self.data.recov_number_county(stadt)
        infec_total = self.data.infections_number_county(stadt)
        table = self.data_stadt
        table.setColumnCount(2)
        table.setRowCount(3)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setItem(0, 0, QW.QTableWidgetItem("Todeszahl"))
        table.setItem(1, 0, QW.QTableWidgetItem("Anzahl der Genesenen"))
        table.setItem(2, 0, QW.QTableWidgetItem("Anzahl der Infizierten"))
        table.setItem(0, 1, QW.QTableWidgetItem(str(death_total)))
        table.setItem(1, 1, QW.QTableWidgetItem(str(recov_total)))
        table.setItem(2, 1, QW.QTableWidgetItem(str(infec_total)))
        table.resizeColumnsToContents()
        table.setEditTriggers(QW.QTreeView.NoEditTriggers)

    """returns information of specific county via specific search"""
    def stadt_info_spezifisch(self):
        stadt = self.county_input.text()
        death_total = self.data.death_number_county(stadt)
        recov_total = self.data.recov_number_county(stadt)
        infec_total = self.data.infections_number_county(stadt)
        table = self.data_stadt
        table.setColumnCount(2)
        table.setRowCount(3)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setItem(0, 0, QW.QTableWidgetItem("Todeszahl"))
        table.setItem(1, 0, QW.QTableWidgetItem("Anzahl der Genesenen"))
        table.setItem(2, 0, QW.QTableWidgetItem("Anzahl der Infizierten"))
        table.setItem(0, 1, QW.QTableWidgetItem(str(death_total)))
        table.setItem(1, 1, QW.QTableWidgetItem(str(recov_total)))
        table.setItem(2, 1, QW.QTableWidgetItem(str(infec_total)))
        table.resizeColumnsToContents()
        table.setEditTriggers(QW.QTreeView.NoEditTriggers)


app = QW.QApplication(sys.argv)
window = MainWindow()
app.exec_()
