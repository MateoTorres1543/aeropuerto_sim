from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QSplitter, QProgressBar, QStatusBar
)
from PyQt6.QtCore import Qt
from .panel_parametros import PanelParametros
from .panel_resultados import PanelResultados
from .diagrama_flujo import DiagramaFlujo
from .hilo_simulacion import HiloSimulacion
from configuracion import ParametrosEjecucion

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulación de Seguridad Aeroportuaria")
        self.resize(1200, 800)
        self._init_ui()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Panel Izquierdo: Parámetros
        self.panel_params = PanelParametros()
        self.panel_params.solicitar_simulacion.connect(self._iniciar_simulacion)
        self.panel_params.parametros_cambiados.connect(self._actualizar_diagrama)
        main_layout.addWidget(self.panel_params)

        # Divisor Central
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Parte superior: Diagrama de Flujo
        self.diagrama = DiagramaFlujo()
        splitter.addWidget(self.diagrama)
        
        # Parte inferior: Resultados
        self.panel_resultados = PanelResultados()
        splitter.addWidget(self.panel_resultados)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        main_layout.addWidget(splitter)

        # Barra de Estado con Progreso
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

    def _actualizar_diagrama(self, m, e, a):
        self.diagrama.actualizar(m, e, a)

    def _iniciar_simulacion(self, cfg):
        self.panel_params.bloquear(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_bar.showMessage(f"Ejecutando escenario: {cfg.nombre}...")

        params = ParametrosEjecucion() # 30 réplicas por defecto
        self.hilo = HiloSimulacion(cfg, params)
        self.hilo.progreso.connect(self._actualizar_progreso)
        self.hilo.terminado.connect(self._finalizar_simulacion)
        self.hilo.error.connect(self._manejar_error)
        self.hilo.start()

    def _actualizar_progreso(self, actual, total):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(actual)

    def _finalizar_simulacion(self, resultado):
        self.panel_params.bloquear(False)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Simulación completada con éxito.", 5000)
        self.panel_resultados.mostrar_resultado(resultado)

    def _manejar_error(self, mensaje):
        self.panel_params.bloquear(False)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage(f"ERROR: {mensaje}")
