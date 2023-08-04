from _decimal import Decimal

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi

from src.models.models import Model, Receta, Ingrediente


class MainController(QMainWindow):
    def __init__(self, application, name="Main Window"):
        super(MainController, self).__init__()
        self.name = name
        self._application = application
        self.connector = Model()
        self.recetas = []
        self.selected_row = None
        self.inicializar()

    def inicializar(self):
        loadUi('src/views/MainView.ui', self)
        self.__setupUi()
        self.__setupUiComponents()

    def __setupUi(self):
        self.cargar_datos()

    def __setupUiComponents(self):
        self.btn_exit.clicked.connect(self.close)
        # self.btn_search.clicked.connect(self.__buscar)
        self.btn_new.clicked.connect(self.__nueva_receta)
        self.btn_edit.clicked.connect(self.__actualizar_receta)
        self.btn_remove.clicked.connect(self.__nueva_receta)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Salir", "¿Realmente quieres salir?", QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def __find(self):
        self.__clean()
        self.label_2.setPixmap(self._application.svg_recolor(f"assets/icons/book-bookmark.svg", '#0098DA'))
        self.horizontalLayout_11.setContentsMargins(5, 2, 5, 2)
        self.lbl_title.setText(" RESULTADO DE LA BUSQUEDA")

        _translate = QtCore.QCoreApplication.translate

        actions = [self.__new_recipe, self.__actualizar_receta, self.__remove_recipe]
        for index, name in enumerate(['Añadir', 'Modificar', 'Eliminar']):
            button = QtWidgets.QPushButton(self.frame_3)
            button.setObjectName(f"btn_item_var_{index}")
            button.clicked.connect(actions[index])
            button.setText(_translate("MainWindow", name))

            self.horizontalLayout_10.addWidget(button)

        self.__qtable(['ID', 'Nombre', 'Timepo de preparación', 'Tiempo de cocción'], [])
        recipes = self.connector.find_by_name(self.tfd_input.text())

        self.recipes = recipes
        for recipe in recipes:
            self.add_element_to_table(recipe)

        self.favorite = False

    def __nueva_receta(self):
        self._application.ui_config("nueva receta", parent=self)

    def ver_receta(self):
        recipe = self.recetas[self.selected_row]
        self._application.ui_config("ver receta", parent=self, data=recipe)

    def __actualizar_receta(self):
        if not self.selected_row == None:
            recipe = self.recetas[self.selected_row].to_dict()
            recipe['row'] = self.selected_row
            recipe['index'] = self.selected_row
            self._application.ui_config("nueva receta", parent=self, data=recipe)

    def __qtable(self, header, data, layout=None, table=None):
        _translate = QtCore.QCoreApplication.translate

        if not table:
            table = QtWidgets.QTableWidget()
            self.tableWidget = table
            self.tableWidget.clicked.connect(lambda item: setattr(self, 'selected_row', item.row()))
            self.tableWidget.itemDoubleClicked.connect(self.ver_receta)

        if not layout:
            layout = self.verticalLayout_task

        table.setStyleSheet("""QTableView {
            background-color: transparent;
            font-size:13px;
        }

        QHeaderView::section:horizontal {
            color: #fff;
            border-style: solid;
            background-color: #0098DA;
         }

        QTableWidget {
            border: 2px solid #0098DA;
            border-top-color: #0098DA;
            gridline-color: #616161;
            selection-background-color: #616161;
            color:#333;
            font-size:12px;
         }""")
        # table.setGeometry(QtCore.QRect(130, 150, 256, 192))
        table.setObjectName("tableWidget")
        layout.addWidget(table)

        table.setEnabled(True)
        table.setAcceptDrops(True)
        table.setAutoFillBackground(True)
        table.setFrameShape(QtWidgets.QFrame.StyledPanel)
        table.setFrameShadow(QtWidgets.QFrame.Sunken)
        table.setLineWidth(1)
        table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        table.setDragEnabled(True)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        table.setShowGrid(True)
        table.setGridStyle(QtCore.Qt.SolidLine)
        table.setCornerButtonEnabled(True)
        table.setRowCount(0)
        table.setColumnCount(len(header))
        table.setObjectName("tableWidget")

        table.setColumnWidth(0, 250)
        table.setColumnWidth(1, 200)
        table.setColumnWidth(2, 200)

        for i in range(len(header)):
            table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())

        table.horizontalHeader().setVisible(True)
        table.horizontalHeader().setCascadingSectionResizes(False)
        table.horizontalHeader().setHighlightSections(False)
        table.horizontalHeader().setSortIndicatorShown(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(True)
        table.verticalHeader().setCascadingSectionResizes(False)
        table.verticalHeader().setHighlightSections(True)
        table.verticalHeader().setSortIndicatorShown(False)
        table.verticalHeader().setStretchLastSection(False)

        table.setSortingEnabled(False)

        for i in range(len(header)):
            table.horizontalHeaderItem(i).setText(_translate("MainWindow", header[i]))

        table.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(len(data[i])):
                item = QTableWidgetItem(str(data[i][j]))
                table.setItem(i, j, item)

    def agregar_elemento_a_la_tabla(self, receta):
        elements = [
            str(receta.id),
            str(receta.nombre),
            f"{str(receta.tiempo_preparacion)} minutos",
            f"{str(receta.tiempo_coccion)} minutos"
        ]
        if len(elements) > 0:
            row_index = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row_index + 1)
            for column_index, elemento in enumerate(elements):
                item = QTableWidgetItem(elemento)
                self.tableWidget.setItem(row_index, column_index, item)

            self.tableWidget.viewport().update()

    def actualizar_elemento_en_la_tabla(self, row, receta):
        elements = [
            str(receta.id),
            str(receta.nombre),
            f"{str(receta.tiempo_preparacion)} minutos",
            f"{str(receta.tiempo_coccion)} minutos"
        ]
        if row >= 0 and row < self.tableWidget.rowCount():
            for column_index, elemento in enumerate(elements):
                item = self.tableWidget.item(row, column_index)
                if item is not None:
                    item.setText(elemento)
                else:
                    item = QTableWidgetItem(elemento)
                    self.tableWidget.setItem(row, column_index, item)

            self.tableWidget.viewport().update()

    def cargar_datos(self):
        self.__qtable(['ID', 'Nombre', 'Timepo de preparación', 'Tiempo de cocción'], [])
        recetas = self.connector.obtener_todas_recetas()

        self.recetas = recetas
        for receta in recetas:
            self.agregar_elemento_a_la_tabla(receta)


class NewRecipeController(QDialog):
    def __init__(self, application, owner, receta=None, name="New Recipe Dialog"):
        super(NewRecipeController, self).__init__(parent=owner)
        self.name = name
        self._application = application
        self.owner = owner
        self.ingredients = []
        self.receta = receta

        loadUi('src/views/NewRecipeView.ui', self)
        self.__setupUi()
        self.__setupUiComponents()

        if self.receta:
            self.tfd_name.setText(self.receta['nombre'])
            self.tfd_time1.setText(str(self.receta['tiempo_preparacion']))
            self.tfd_time2.setText(str(self.receta['tiempo_coccion']))
            self.ingredients = self.receta['ingredientes']
            self.text_area.setText(self.receta['instrucciones'])

    def __setupUi(self):
        if self.receta:
            self.setWindowTitle("Modificar Receta")

        validator = QtGui.QIntValidator()
        self.tfd_time1.setValidator(validator)
        self.tfd_time2.setValidator(validator)

    def __setupUiComponents(self):
        self.btn_cancel.clicked.connect(self.__cancel)
        self.btn_ingredients.clicked.connect(self.__ingredients)
        self.btn_accept.clicked.connect(lambda: self.__accept(close=True))
        self.btn_accept_and_new.clicked.connect(lambda: self.__accept(close=False))

    def show(self, command=None):
        self.setModal(True)
        super().show()

    def __cancel(self):
        self.close()

    def __accept(self, close=True):
        receta = Receta(
            nombre=self.tfd_name.text().title(),
            tiempo_preparacion=self.tfd_time1.text().title(),
            tiempo_coccion=self.tfd_time2.text().title(),
            ingredientes=self.ingredients,
            instrucciones=self.text_area.toPlainText(),
        )

        if self.receta:
            self.owner.connector.actualizar_receta(self.receta['id'],
                                                   receta.nombre,
                                                   receta.tiempo_preparacion,
                                                   receta.tiempo_coccion,
                                                   receta.instrucciones,
                                                   receta.ingredientes,
                                                   )
            receta.id = self.receta['id']
            receta.ingredientes = [Ingrediente(
                nombre=ingrediente['nombre'],
                cantidad=ingrediente['cantidad'],
                unidad=ingrediente['unidad']
            ) for ingrediente in receta.ingredientes]
            self.owner.recetas[self.receta['index']] = receta
            self.owner.actualizar_elemento_en_la_tabla(self.receta['row'], receta)
        else:
            receta.ingredientes = [Ingrediente(
                nombre=ingrediente['nombre'],
                cantidad=ingrediente['cantidad'],
                unidad=ingrediente['unidad']
            ) if not isinstance(ingrediente, Ingrediente) else ingrediente for ingrediente in receta.ingredientes]
            receta.id = self.owner.connector.nueva_receta(receta=receta)
            self.owner.recetas.append(receta)
            self.owner.agregar_elemento_a_la_tabla(receta)

        if close:
            self._application.ui_config(remove=True)
        else:
            self.tfd_name.clear()
            self.tfd_time1.clear()
            self.tfd_time2.clear()
            self.text_area.clear()
            self.ingredients = []

    def __ingredients(self):
        self._application.ui_config('ingredientes', parent=self)


class AddIngredientsController(QDialog):
    def __init__(self, application, owner, name="Ingredients Dialog"):
        super(AddIngredientsController, self).__init__(parent=owner)
        self.name = name
        self._application = application
        self.owner = owner
        self.ingredients = []
        self.remove_ingredients = []

        loadUi('src/views/AddIngredientsView.ui', self)
        self.__setupUi()
        self.__setupUiComponents()

    def __setupUi(self):
        validator = QtGui.QDoubleValidator()
        self.tft_cnt.setValidator(validator)

        aux = []
        for ingrediente in self.owner.ingredients:
            aux.append([ingrediente['nombre'], ingrediente['cantidad'], ingrediente['unidad']])

        self.__qtable(['Ingrediente', 'Cantidad', 'Unidad'], aux)

    def __setupUiComponents(self):
        self.btn_cancel.clicked.connect(self.__cancel)
        self.btn_add.clicked.connect(self.__add_element)
        self.btn_accept.clicked.connect(self.__accept)

        self.tableWidget.itemDoubleClicked.connect(lambda item: self.delete_row(item.row()))

    def show(self, command=None):
        self.setModal(True)
        super().show()

    def __cancel(self):
        self.close()

    def __qtable(self, header, data, layout=None, table=None):
        _translate = QtCore.QCoreApplication.translate

        if not table:
            table = QtWidgets.QTableWidget()
            self.tableWidget = table

        if not layout:
            layout = self.verticalLayout_task

        table.setStyleSheet("""QTableView {
        background-color: transparent;
        font-size:13px;
    }

    QHeaderView::section:horizontal {
        color: #fff;
        border-style: solid;
        background-color: #0098DA;
     }

    QTableWidget {
        border: 2px solid #0098DA;
        border-top-color: #0098DA;
        gridline-color: #616161;
        selection-background-color: #616161;
        color:#333;
        font-size:12px;
     }""")
        # table.setGeometry(QtCore.QRect(130, 150, 256, 192))
        table.setObjectName("tableWidget")
        layout.addWidget(table)

        table.setEnabled(True)
        table.setAcceptDrops(True)
        table.setAutoFillBackground(True)
        table.setFrameShape(QtWidgets.QFrame.StyledPanel)
        table.setFrameShadow(QtWidgets.QFrame.Sunken)
        table.setLineWidth(1)
        table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        table.setDragEnabled(True)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        table.setShowGrid(True)
        table.setGridStyle(QtCore.Qt.SolidLine)
        table.setCornerButtonEnabled(True)
        table.setRowCount(0)
        table.setColumnCount(len(header))
        table.setObjectName("tableWidget")

        for i in range(len(header)):
            table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())

        table.horizontalHeader().setVisible(True)
        table.horizontalHeader().setCascadingSectionResizes(False)
        table.horizontalHeader().setHighlightSections(False)
        table.horizontalHeader().setSortIndicatorShown(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(True)
        table.verticalHeader().setCascadingSectionResizes(False)
        table.verticalHeader().setHighlightSections(True)
        table.verticalHeader().setSortIndicatorShown(False)
        table.verticalHeader().setStretchLastSection(False)

        table.setSortingEnabled(False)

        for i in range(len(header)):
            table.horizontalHeaderItem(i).setText(_translate("MainWindow", header[i]))

        table.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(len(data[i])):
                item = QTableWidgetItem(str(data[i][j]))
                table.setItem(i, j, item)

    def __accept(self):
        if len(self.ingredients) > 0:
            self.owner.ingredients.extend(self.ingredients)

        if len(self.remove_ingredients) > 0:
            for to_remove in self.remove_ingredients:
                to_remove = {
                    'nombre': to_remove[0],
                    'unidad': to_remove[2],
                    'cantidad': Decimal(to_remove[1])
                }
                for elemento in self.owner.ingredients:
                    if str(elemento['nombre']) == str(to_remove['nombre']):
                        if str(elemento['unidad']) == str(to_remove['unidad']):
                            if Decimal(elemento['cantidad']) == to_remove['cantidad']:
                                self.owner.ingredients.remove(elemento)

        self._application.ui_config(remove=True)

    def __add_element(self):
        if not self.tft_name.text() == "" and not self.tft_cnt.text() == "" and not self.tft_unit.text() == "":
            element = Ingrediente(
                nombre=self.tft_name.text(),
                cantidad=self.tft_cnt.text(),
                unidad=self.tft_unit.text()
            )
            self.add_element_to_table(element)
            self.ingredients.append(element)

    def add_element_to_table(self, elements):
        elements = elements.to_list()
        if len(elements) > 0:
            row_index = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row_index + 1)
            for column_index, elemento in enumerate(elements):
                item = QTableWidgetItem(elemento)
                self.tableWidget.setItem(row_index, column_index, item)

            self.tableWidget.viewport().update()

    def delete_row(self, row):
        row_data = []
        for column in range(self.tableWidget.model().columnCount()):
            column_data = self.tableWidget.model().data(self.tableWidget.model().index(row, column))
            row_data.append(column_data)

        reply = QMessageBox.question(
            self, "Eliminar Ingrediente",
            f"¿Quiere eliminar el Ingrediente: {row_data}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.remove_ingredients.append(row_data)
            self.tableWidget.removeRow(row)
