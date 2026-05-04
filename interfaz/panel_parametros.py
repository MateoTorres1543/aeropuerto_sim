from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, 
    QDoubleSpinBox, QSpinBox, QPushButton, QComboBox, QScrollArea
)
from PyQt6.QtCore import pyqtSignal
from configuracion import ConfiguracionEscenario

class PanelParametros(QWidget):
    solicitar_simulacion = pyqtSignal(ConfiguracionEscenario)
    parametros_cambiados = pyqtSignal(int, int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(320)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        content = QWidget()
        layout = QVBoxLayout(content)
        
        # --- SECCIÓN: PRESETS DE ESCENARIO ---
        grupo_presets = QGroupBox("Presets de Escenario")
        layout_presets = QVBoxLayout(grupo_presets)
        self.combo_presets = QComboBox()
        self.combo_presets.addItems(["Personalizado", "Normal", "Crítico", "Colapsado"])
        self.combo_presets.currentIndexChanged.connect(self._aplicar_preset)
        layout_presets.addWidget(self.combo_presets)
        layout.addWidget(grupo_presets)

        # --- SECCIÓN: LLEGADAS Y CHEQUEO ---
        grupo_llegada = QGroupBox("1. Llegadas y Chequeo")
        grid1 = QGridLayout(grupo_llegada)
        
        grid1.addWidget(QLabel("λ (Llegadas/h):"), 0, 0)
        self.sp_lambda = QDoubleSpinBox()
        self.sp_lambda.setRange(5, 300); self.sp_lambda.setValue(40)
        grid1.addWidget(self.sp_lambda, 0, 1)
        
        grid1.addWidget(QLabel("Mostradores:"), 1, 0)
        self.sp_most = QSpinBox()
        self.sp_most.setRange(1, 20); self.sp_most.setValue(3)
        grid1.addWidget(self.sp_most, 1, 1)
        
        grid1.addWidget(QLabel("Chequeo (a, m, b):"), 2, 0)
        self.sp_ca = QDoubleSpinBox(); self.sp_ca.setValue(2.0)
        self.sp_cm = QDoubleSpinBox(); self.sp_cm.setValue(4.0)
        self.sp_cb = QDoubleSpinBox(); self.sp_cb.setValue(7.0)
        grid1.addWidget(self.sp_ca, 2, 1)
        grid1.addWidget(self.sp_cm, 3, 1)
        grid1.addWidget(self.sp_cb, 4, 1)
        layout.addWidget(grupo_llegada)

        # --- SECCIÓN: SEGURIDAD (μ1, p, μ2) ---
        grupo_seg = QGroupBox("2. Control Seguridad")
        grid2 = QGridLayout(grupo_seg)
        
        grid2.addWidget(QLabel("Escáneres (N):"), 0, 0)
        self.sp_esc = QSpinBox()
        self.sp_esc.setRange(1, 20); self.sp_esc.setValue(3)
        grid2.addWidget(self.sp_esc, 0, 1)
        
        grid2.addWidget(QLabel("μ1 (Servicio min):"), 1, 0)
        self.sp_mu1 = QDoubleSpinBox()
        self.sp_mu1.setValue(1.5)
        grid2.addWidget(self.sp_mu1, 1, 1)
        
        grid2.addWidget(QLabel("p (Prob. Revisión):"), 2, 0)
        self.sp_p = QDoubleSpinBox()
        self.sp_p.setRange(0, 1); self.sp_p.setSingleStep(0.05); self.sp_p.setValue(0.15)
        grid2.addWidget(self.sp_p, 2, 1)
        
        grid2.addWidget(QLabel("μ2 (Revisión min):"), 3, 0)
        self.sp_mu2 = QDoubleSpinBox()
        self.sp_mu2.setValue(4.0)
        grid2.addWidget(self.sp_mu2, 3, 1)
        layout.addWidget(grupo_seg)

        # --- SECCIÓN: SALA Y EMBARQUE (μ3) ---
        grupo_sala = QGroupBox("3. Sala y Puertas")
        grid3 = QGridLayout(grupo_sala)
        
        grid3.addWidget(QLabel("Sala (min-max):"), 0, 0)
        self.sp_smin = QDoubleSpinBox(); self.sp_smin.setValue(10.0)
        self.sp_smax = QDoubleSpinBox(); self.sp_smax.setValue(30.0)
        grid3.addWidget(self.sp_smin, 0, 1)
        grid3.addWidget(self.sp_smax, 1, 1)
        
        grid3.addWidget(QLabel("μ3 (Embarque min):"), 2, 0)
        self.sp_mu3 = QDoubleSpinBox()
        self.sp_mu3.setValue(3.0)
        grid3.addWidget(self.sp_mu3, 2, 1)
        layout.addWidget(grupo_sala)

        # --- SECCIÓN: CONTROL (T) ---
        grupo_t = QGroupBox("4. Límite de Tiempo")
        grid4 = QGridLayout(grupo_t)
        grid4.addWidget(QLabel("T (Límite vuelo):"), 0, 0)
        self.sp_t = QDoubleSpinBox()
        self.sp_t.setRange(10, 500); self.sp_t.setValue(60.0)
        grid4.addWidget(self.sp_t, 0, 1)
        layout.addWidget(grupo_t)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        self.btn_simular = QPushButton("EJECUTAR MODELO")
        self.btn_simular.setMinimumHeight(50)
        self.btn_simular.clicked.connect(self._preparar_configuracion)
        main_layout.addWidget(self.btn_simular)

        # Conectar cambios para el diagrama y para poner el combo en "Personalizado"
        self.sp_most.valueChanged.connect(self._al_cambiar_valor)
        self.sp_esc.valueChanged.connect(self._al_cambiar_valor)
        self.sp_lambda.valueChanged.connect(self._al_cambiar_valor)
        self.sp_ca.valueChanged.connect(self._al_cambiar_valor)
        self.sp_cm.valueChanged.connect(self._al_cambiar_valor)
        self.sp_cb.valueChanged.connect(self._al_cambiar_valor)
        self.sp_mu1.valueChanged.connect(self._al_cambiar_valor)
        self.sp_p.valueChanged.connect(self._al_cambiar_valor)
        self.sp_mu2.valueChanged.connect(self._al_cambiar_valor)
        self.sp_t.valueChanged.connect(self._al_cambiar_valor)

    def _al_cambiar_valor(self):
        """Si el usuario toca un valor, el combo pasa a Personalizado."""
        if hasattr(self, 'combo_presets') and self.combo_presets.currentIndex() != 0:
            self.combo_presets.blockSignals(True)
            self.combo_presets.setCurrentIndex(0)
            self.combo_presets.blockSignals(False)
        self.parametros_cambiados.emit(self.sp_most.value(), self.sp_esc.value(), 1)

    def _aplicar_preset(self, index):
        if index == 0: return # Personalizado

        # Definición de presets
        presets = {
            1: { # Normal
                "lambda": 40.0, "most": 4, "esc": 3, "mu1": 1.5, "p": 0.10, "t": 90.0, "ca": 2.0, "cm": 4.0, "cb": 7.0
            },
            2: { # Crítico
                "lambda": 80.0, "most": 3, "esc": 2, "mu1": 1.8, "p": 0.20, "t": 45.0, "ca": 3.0, "cm": 5.0, "cb": 8.0
            },
            3: { # Colapsado
                "lambda": 150.0, "most": 2, "esc": 1, "mu1": 2.5, "p": 0.35, "t": 30.0, "ca": 4.0, "cm": 6.0, "cb": 10.0
            }
        }
        
        p = presets[index]
        self.blockSignals(True)
        self.sp_lambda.setValue(p["lambda"])
        self.sp_most.setValue(p["most"])
        self.sp_esc.setValue(p["esc"])
        self.sp_mu1.setValue(p["mu1"])
        self.sp_p.setValue(p["p"])
        self.sp_t.setValue(p["t"])
        self.sp_ca.setValue(p["ca"])
        self.sp_cm.setValue(p["cm"])
        self.sp_cb.setValue(p["cb"])
        self.blockSignals(False)
        self.parametros_cambiados.emit(self.sp_most.value(), self.sp_esc.value(), 1)

    def _preparar_configuracion(self):
        # Crear un perfil de llegada simple basado en el valor actual de λ
        perfil = [(0, self.sp_lambda.value())]
        
        cfg = ConfiguracionEscenario(
            nombre=f"Esc-{int(self.sp_lambda.value())}pax",
            perfil_llegada=perfil,
            num_mostradores_chequeo=self.sp_most.value(),
            chequeo_a=self.sp_ca.value(),
            chequeo_m=self.sp_cm.value(),
            chequeo_b=self.sp_cb.value(),
            num_escaneres=self.sp_esc.value(),
            media_escaneo=self.sp_mu1.value(),
            prob_revision=self.sp_p.value(),
            num_agentes_revision=2,
            media_revision=self.sp_mu2.value(),
            espera_sala_min=self.sp_smin.value(),
            espera_sala_max=self.sp_smax.value(),
            media_embarque=self.sp_mu3.value(),
            tiempo_limite=self.sp_t.value(),
            tiempo_avion_listo=0.0, # Por defecto 0 en la interfaz simple
            duracion_simulacion=480.0,
            semilla_base=42
        )
        self.solicitar_simulacion.emit(cfg)

    def bloquear(self, b):
        self.setEnabled(not b)
