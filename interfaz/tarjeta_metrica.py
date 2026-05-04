from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .estilos import COLORES

class TarjetaMetrica(QFrame):
    """
    Muestra una métrica clave con su etiqueta y valor.
    Incluye colores semáforo opcionales.
    """
    def __init__(self, titulo: str, unidad: str = "", parent=None):
        super().__init__(parent)
        self.unidad = unidad
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            TarjetaMetrica {{
                background-color: {COLORES['tarjeta']};
                border: 1px solid {COLORES['borde']};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        
        self.lbl_titulo = QLabel(titulo)
        self.lbl_titulo.setStyleSheet(f"color: {COLORES['muted']}; font-weight: bold; font-size: 11px;")
        
        self.lbl_valor = QLabel("--")
        self.lbl_valor.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.lbl_valor.setStyleSheet(f"color: {COLORES['texto']};")
        
        self.lbl_ic = QLabel("")
        self.lbl_ic.setStyleSheet(f"color: {COLORES['muted']}; font-size: 10px;")
        
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.lbl_valor)
        layout.addWidget(self.lbl_ic)

    def actualizar(self, valor: float, ic: tuple[float, float] = None, color: str = None):
        if isinstance(valor, (int, float)):
            texto_valor = f"{valor:.2f}"
        else:
            texto_valor = str(valor)
            
        if self.unidad:
            texto_valor += f" {self.unidad}"
            
        self.lbl_valor.setText(texto_valor)
        
        if color in COLORES:
            self.lbl_valor.setStyleSheet(f"color: {COLORES[color]}; font-weight: bold; font-size: 16px;")
        else:
            self.lbl_valor.setStyleSheet(f"color: {COLORES['texto']}; font-weight: bold; font-size: 16px;")
            
        if ic:
            self.lbl_ic.setText(f"IC 95%: [{ic[0]:.2f}, {ic[1]:.2f}]")
        else:
            self.lbl_ic.setText("")
