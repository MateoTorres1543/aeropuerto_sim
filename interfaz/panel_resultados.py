from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, 
    QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QGridLayout, QLabel
)
from PyQt6.QtCore import Qt
from .tarjeta_metrica import TarjetaMetrica
from .graficas import construir_histograma, construir_convergencia
from resultado import ResultadoEscenario

class PanelResultados(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self.historico: list[ResultadoEscenario] = []

    def _init_ui(self):
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        
        # Tab 1: Métricas Principales
        self.tab_metricas = QWidget()
        self.layout_grid = QGridLayout(self.tab_metricas)
        self.layout_grid.setSpacing(15)
        
        self.tarjetas = {
            "espera": TarjetaMetrica("ESPERA SEGURIDAD", "min"),
            "perdidos": TarjetaMetrica("% PIERDE VUELO", "%"),
            "utilizacion": TarjetaMetrica("UTILIZACIÓN ESCÁNER", ""),
            "total": TarjetaMetrica("TOTAL PROCESADOS", "pax"),
            "tiempo_sis": TarjetaMetrica("TIEMPO EN SISTEMA", "min")
        }
        
        posiciones = [(0,0), (0,1), (1,0), (1,1), (2,0)]
        for i, (clave, tarjeta) in enumerate(self.tarjetas.items()):
            self.layout_grid.addWidget(tarjeta, posiciones[i][0], posiciones[i][1])
            
        # Tabla de Colas por Etapa (Requisito 12.4)
        self.tabla_etapas = QTableWidget()
        self.tabla_etapas.setColumnCount(3)
        self.tabla_etapas.setHorizontalHeaderLabels(["Etapa", "Cola Prom.", "Cola Máx."])
        self.tabla_etapas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_etapas.setFixedHeight(180)
        self.layout_grid.addWidget(QLabel("<b>LONGITUD DE FILAS POR ETAPA:</b>"), 3, 0, 1, 2)
        self.layout_grid.addWidget(self.tabla_etapas, 4, 0, 1, 2)
        
        self.tabs.addTab(self.tab_metricas, "📊 Métricas")
        
        # Tab 2: Gráficas
        self.tab_graficas_scroll = QScrollArea()
        self.tab_graficas_scroll.setWidgetResizable(True)
        self.contenedor_graficas = QWidget()
        self.layout_graficas = QVBoxLayout(self.contenedor_graficas)
        self.tab_graficas_scroll.setWidget(self.contenedor_graficas)
        self.tabs.addTab(self.tab_graficas_scroll, "📈 Análisis Visual")
        
        # Tab 3: Comparar
        self.tab_comparar = QTableWidget()
        self.tab_comparar.setColumnCount(5)
        self.tab_comparar.setHorizontalHeaderLabels([
            "Escenario", "Espera (min)", "Perdidos %", "Utiliz.", "Procesados"
        ])
        self.tab_comparar.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabs.addTab(self.tab_comparar, "⚖️ Comparar")
        
        layout.addWidget(self.tabs)

    def mostrar_resultado(self, res: ResultadoEscenario):
        # 1. Actualizar tarjetas
        self.tarjetas["espera"].actualizar(res.media_espera, res.ic_espera, 
                                         "advertencia" if res.media_espera > 15 else "exito")
        self.tarjetas["perdidos"].actualizar(res.pct_perdidos, res.ic_perdidos,
                                           "peligro" if res.pct_perdidos > 5 else "exito")
        
        # Utilización de escáner (específico)
        util_esc = res.met_estaciones.get("Escáner", {}).get("utilizacion", 0)
        self.tarjetas["utilizacion"].actualizar(util_esc, color="purpura")
        
        self.tarjetas["total"].actualizar(int(res.total_pasajeros))
        media_sis = sum(res.todos_tiempos_sistema) / len(res.todos_tiempos_sistema) if res.todos_tiempos_sistema else 0
        self.tarjetas["tiempo_sis"].actualizar(media_sis)
        
        # 2. Actualizar Tabla de Etapas (Requisito 12.4)
        self.tabla_etapas.setRowCount(0)
        for nombre, mets in res.met_estaciones.items():
            row = self.tabla_etapas.rowCount()
            self.tabla_etapas.insertRow(row)
            self.tabla_etapas.setItem(row, 0, QTableWidgetItem(nombre))
            self.tabla_etapas.setItem(row, 1, QTableWidgetItem(f"{mets['prom_cola']:.2f}"))
            self.tabla_etapas.setItem(row, 2, QTableWidgetItem(f"{mets['max_cola']:.1f}"))

        # 3. Actualizar gráficas
        for i in reversed(range(self.layout_graficas.count())): 
            w = self.layout_graficas.itemAt(i).widget()
            if w: w.setParent(None)
        self.layout_graficas.addWidget(construir_histograma(res.todas_esperas, "Distribución de Esperas", "acento"))
        self.layout_graficas.addWidget(construir_convergencia(res.replicas, "Convergencia de la Media (Espera)"))
        
        # 4. Tabla comparativa
        self.historico.append(res)
        row_c = self.tab_comparar.rowCount()
        self.tab_comparar.insertRow(row_c)
        self.tab_comparar.setItem(row_c, 0, QTableWidgetItem(res.nombre))
        self.tab_comparar.setItem(row_c, 1, QTableWidgetItem(f"{res.media_espera:.2f}"))
        self.tab_comparar.setItem(row_c, 2, QTableWidgetItem(f"{res.pct_perdidos:.2f}%"))
        self.tab_comparar.setItem(row_c, 3, QTableWidgetItem(f"{util_esc:.2f}"))
        self.tab_comparar.setItem(row_c, 4, QTableWidgetItem(f"{int(res.total_pasajeros)}"))
        
        self.tabs.setCurrentIndex(0)
